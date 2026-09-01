"""High-performance Native Haskell (GHC 9.2 - 9.10+ / Haskell2010 / Haskell2021) AST & CST Parser Adapter implementing ParserPort."""

from __future__ import annotations

import os
import re
from pathlib import Path

from pattern_detector.domain.code_model import (
    CodeModel,
    ConstructorModel,
    FunctionModel,
    ModuleModel,
    TypeClassInstanceModel,
    TypeClassModel,
    TypeDeclarationModel,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


class NativeHaskellParserAdapter(ParserPort):
    """High-performance native Haskell parser supporting GHC extensions, GADTs, typeclasses, and monad stacks."""

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_text in sources.items():
            mod = self.parse_file(file_path, source_text)
            model.modules[mod.name] = mod
        return model

    def parse_file(self, file_path: str, source_text: str) -> ModuleModel:
        clean_text = self._strip_comments_and_strings(source_text)
        mod_name = self._parse_module_name(source_text, file_path)
        loc = SourceLocation(file_path=file_path, line=1, column=1)

        module = ModuleModel(
            name=mod_name,
            file_path=file_path,
            raw_source=source_text,
            clean_source=clean_text,
            location=loc,
        )

        # 1. Pragmas
        module.pragmas = self._parse_pragmas(source_text)

        # 2. Imports
        module.imports = self._parse_imports(clean_text)

        # 3. Type Declarations (data, newtype, type, GADT)
        module.types = self._parse_types(clean_text, file_path)

        # 4. TypeClasses & Instances
        module.typeclasses = self._parse_typeclasses(clean_text, file_path)
        module.instances = self._parse_instances(clean_text, file_path)

        # 5. Functions & Bindings
        module.functions = self._parse_functions(clean_text, file_path)

        return module

    # -------------------------------------------------------------------------
    # Parsing Helpers
    # -------------------------------------------------------------------------

    def _strip_comments_and_strings(self, text: str) -> str:
        i = 0
        n = len(text)
        out: list[str] = []

        while i < n:
            # Check for LANGUAGE / OPTIONS pragma {-# ... #-} -> preserve
            if text[i:i+3] == "{-#":
                end = text.find("#-}", i + 3)
                if end != -1:
                    out.append(text[i:end+3])
                    i = end + 3
                else:
                    out.append(text[i:])
                    break
            # Check for block comment {- ... -} (supports nested comments)
            elif text[i:i+2] == "{-":
                depth = 1
                i += 2
                while i < n and depth > 0:
                    if text[i:i+2] == "{-":
                        depth += 1
                        i += 2
                    elif text[i:i+2] == "-}":
                        depth -= 1
                        i += 2
                    elif text[i] == "\n":
                        out.append("\n")
                        i += 1
                    else:
                        i += 1
                out.append(" ")
            # Check for line comment --
            elif text[i:i+2] == "--":
                while i < n and text[i] != "\n":
                    i += 1
            # Check for string literal "..."
            elif text[i] == '"':
                i += 1
                out.append('""')
                while i < n:
                    if text[i] == '\\' and i + 1 < n:
                        if text[i+1] == "\n":
                            out.append("\n")
                        i += 2
                    elif text[i] == '"':
                        i += 1
                        break
                    elif text[i] == "\n":
                        out.append("\n")
                        i += 1
                    else:
                        i += 1
            # Check for character literal 'c'
            elif text[i] == "'":
                if i + 2 < n and text[i+1] != "'" and text[i+2] == "'":
                    i += 3
                    out.append(" ' ' ")
                elif i + 3 < n and text[i+1] == "\\" and text[i+3] == "'":
                    i += 4
                    out.append(" ' ' ")
                else:
                    out.append(text[i])
                    i += 1
            else:
                out.append(text[i])
                i += 1

        return "".join(out)

    def _parse_module_name(self, text: str, file_path: str) -> str:
        m = re.search(r"^\s*module\s+([A-Z][a-zA-Z0-9_.]*)", text, re.MULTILINE)
        if m:
            return m.group(1)
        return Path(file_path).stem.capitalize()

    def _parse_pragmas(self, text: str) -> list[str]:
        pragmas = []
        for m in re.finditer(r"\{-#\s*LANGUAGE\s+([^#]+)#-\}", text):
            for ext in m.group(1).split(","):
                clean_ext = ext.strip()
                if clean_ext:
                    pragmas.append(clean_ext)
        return pragmas

    def _parse_imports(self, text: str) -> list[str]:
        imports = []
        for m in re.finditer(r"^\s*import\s+(?:qualified\s+)?([A-Z][a-zA-Z0-9_.]*)", text, re.MULTILINE):
            imports.append(m.group(1))
        return imports

    def _parse_types(self, text: str, file_path: str) -> dict[str, TypeDeclarationModel]:
        types: dict[str, TypeDeclarationModel] = {}

        # In Haskell layout, top-level type declarations start at column 1 (no leading whitespace)
        # or minimal whitespace, terminated by next column 1 declaration
        pattern = re.compile(
            r"^(data|newtype|type)\s+(family\s+)?([A-Z][a-zA-Z0-9_]*)([\s\S]*?)(?=^[a-zA-Z0-9_']|\Z)",
            re.MULTILINE,
        )

        for m in pattern.finditer(text):
            kind = m.group(1)
            is_family = bool(m.group(2))
            name = m.group(3)
            rest = m.group(4) or ""
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            is_newtype = (kind == "newtype")
            is_type_alias = (kind == "type")
            is_gadt = " where" in rest and ("::" in rest or "->" in rest)

            deriving = []
            strategies = []
            if "deriving" in rest:
                deriv_m = re.findall(r"deriving\s+(?:(stock|newtype|anyclass)\s+)?\(?([^)\n]+)\)?", rest)
                for strat, d_clause in deriv_m:
                    if strat:
                        strategies.append(strat)
                    for d_item in d_clause.split(","):
                        d_clean = d_item.strip()
                        if d_clean:
                            deriving.append(d_clean)

            types[name] = TypeDeclarationModel(
                name=name,
                is_data=(kind == "data"),
                is_newtype=is_newtype,
                is_type_alias=is_type_alias,
                is_gadt=is_gadt,
                is_type_family=is_family,
                deriving=deriving,
                deriving_strategies=strategies,
                location=loc,
            )

        return types

    def _parse_typeclasses(self, text: str, file_path: str) -> dict[str, TypeClassModel]:
        typeclasses: dict[str, TypeClassModel] = {}

        pattern = re.compile(
            r"^class\s+(?:([^=]+)=>\s*)?([A-Z][a-zA-Z0-9_]*)\s+([^w\n]+)?where\b([\s\S]*?)(?=^[a-zA-Z0-9_']|\Z)",
            re.MULTILINE,
        )

        for m in pattern.finditer(text):
            superclasses_raw = m.group(1) or ""
            name = m.group(2)
            params_raw = m.group(3) or ""
            body = m.group(4) or ""
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            methods = re.findall(r"^\s+([a-z_][a-zA-Z0-9_']*)\s*::\s*([^\n]+)", body, re.MULTILINE)
            method_strs = [f"{m_name} :: {m_type.strip()}" for m_name, m_type in methods]
            assoc_types = re.findall(r"^\s+(?:type|data)\s+([A-Z][a-zA-Z0-9_]*)", body, re.MULTILINE)

            typeclasses[name] = TypeClassModel(
                name=name,
                params=params_raw.split(),
                superclasses=[s.strip() for s in superclasses_raw.split(",") if s.strip()],
                methods=method_strs,
                associated_types=assoc_types,
                location=loc,
            )

        return typeclasses

    def _parse_instances(self, text: str, file_path: str) -> list[TypeClassInstanceModel]:
        instances = []
        for m in re.finditer(r"^instance\s+(?:[^\n]+=>\s*)?([A-Z][a-zA-Z0-9_]*)\s+([^\n=]+)\s+where", text, re.MULTILINE):
            c_name = m.group(1)
            t_name = m.group(2).strip()
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)
            instances.append(TypeClassInstanceModel(class_name=c_name, target_type=t_name, location=loc))
        return instances

    def _parse_functions(self, text: str, file_path: str) -> dict[str, FunctionModel]:
        functions: dict[str, FunctionModel] = {}

        # 1. Type signatures at column 1: funcName :: Type -> Type
        signatures: dict[str, tuple[str, int]] = {}
        for m in re.finditer(r"^([a-z_][a-zA-Z0-9_']*)\s*::\s*([^\n]+)", text, re.MULTILINE):
            fn_name = m.group(1)
            sig_type = m.group(2).strip()
            line_no = text[:m.start()].count("\n") + 1
            signatures[fn_name] = (sig_type, line_no)

        # 2. Function bindings at column 1: funcName p1 p2 = ...
        pattern = re.compile(
            r"^([a-z_][a-zA-Z0-9_']*)\s*([^=\n]*)=\s*([\s\S]*?)(?=^[a-zA-Z0-9_']|\Z)",
            re.MULTILINE,
        )

        for m in pattern.finditer(text):
            name = m.group(1)
            params_raw = m.group(2).strip()
            body = m.group(3).strip()

            if name in ("where", "let", "in", "do", "case", "of", "if", "then", "else", "type", "data", "newtype", "class", "instance", "module", "import"):
                continue

            line_no = signatures.get(name, ("", text[:m.start()].count("\n") + 1))[1]
            sig = signatures.get(name, ("", 1))[0]
            loc = SourceLocation(file_path=file_path, line=line_no)

            calls = re.findall(r"\b([a-zA-Z0-9_.]+)\b", body)
            complexity = 1 + body.count("case ") + body.count("if ") + body.count(" | ") + body.count("->") // 2

            functions[name] = FunctionModel(
                name=name,
                type_signature=sig,
                params=params_raw.split(),
                body=body,
                cyclomatic_complexity=complexity,
                calls=calls,
                has_error=bool(re.search(r"\berror\b", body)),
                has_undefined=bool(re.search(r"\bundefined\b", body)),
                has_from_just=bool(re.search(r"\bfromJust\b", body)),
                has_lazy_foldl=bool(re.search(r"\bfoldl\s+[^\'\s]", body)),
                has_catch_all=bool(re.search(r"catch[\s\S]*?\\(?:_|\(SomeException\s+[^)]+\)\))\s*->", body)),
                has_do=(" do\n" in body or " do " in body or body.startswith("do\n") or body.startswith("do ")),
                location=loc,
            )

        return functions
