"""ANTLR4 CST/AST Visitor building domain Haskell CodeModel."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pattern_detector.adapters.outbound.parsers.antlr.generated.HaskellParser import HaskellParser
from pattern_detector.adapters.outbound.parsers.antlr.generated.HaskellVisitor import HaskellVisitor
from pattern_detector.domain.code_model import (
    ConstructorModel,
    FunctionModel,
    ModuleModel,
    TypeClassInstanceModel,
    TypeClassModel,
    TypeDeclarationModel,
)
from pattern_detector.domain.value_objects import SourceLocation


class HaskellCstVisitor(HaskellVisitor):
    """Visits the ANTLR4 parse tree to construct a rich domain ModuleModel."""

    def __init__(self, file_path: str, raw_source: str, clean_source: str = "") -> None:
        super().__init__()
        self.file_path = file_path
        self.raw_source = raw_source
        self.clean_source = clean_source or raw_source

        default_mod_name = Path(file_path).stem.capitalize()
        self.module = ModuleModel(
            name=default_mod_name,
            file_path=file_path,
            raw_source=raw_source,
            clean_source=self.clean_source,
            location=SourceLocation(file_path=file_path, line=1, column=1),
        )

        self._signatures: dict[str, tuple[str, int]] = {}

    def visitHaskellModule(self, ctx: HaskellParser.HaskellModuleContext) -> ModuleModel:
        # 1. Visit module header if present
        if ctx.moduleHeader():
            self.visit(ctx.moduleHeader())

        # 2. Visit pragmas
        for p in ctx.pragma():
            self.visit(p)

        # 3. Visit top declarations
        for top_decl in ctx.topDeclaration():
            self.visit(top_decl)

        return self.module

    def visitModuleHeader(self, ctx: HaskellParser.ModuleHeaderContext) -> Any:
        if ctx.modId():
            self.module.name = ctx.modId().getText()
            line = ctx.start.line if ctx.start else 1
            col = (ctx.start.column + 1) if ctx.start else 1
            self.module.location = SourceLocation(file_path=self.file_path, line=line, column=col)
        return self.visitChildren(ctx)

    def visitPragma(self, ctx: HaskellParser.PragmaContext) -> Any:
        txt = ctx.getText()
        m = re.search(r"\{-#\s*LANGUAGE\s+([^#]+)#-\}", txt)
        if m:
            for ext in m.group(1).split(","):
                clean_ext = ext.strip()
                if clean_ext and clean_ext not in self.module.pragmas:
                    self.module.pragmas.append(clean_ext)
        return None

    def visitImportDeclaration(self, ctx: HaskellParser.ImportDeclarationContext) -> Any:
        if ctx.modId():
            mod_name = ctx.modId(0).getText()
            if mod_name not in self.module.imports:
                self.module.imports.append(mod_name)
        return None

    def visitDataDeclaration(self, ctx: HaskellParser.DataDeclarationContext) -> Any:
        type_name = ""
        params: list[str] = []
        if ctx.simpleType():
            st = ctx.simpleType()
            if st.CONID():
                type_name = st.CONID().getText()
            for tv in st.typeVar():
                params.append(tv.getText())

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        is_family = bool(ctx.FAMILY())
        is_gadt = bool(ctx.gadtConstructors()) or (bool(ctx.WHERE()) and bool(ctx.gadtConstructors()))

        deriving: list[str] = []
        strategies: list[str] = []
        for dc in ctx.derivingClause():
            if dc.derivingStrategy():
                strategies.append(dc.derivingStrategy().getText())
            for dt in dc.derivingTarget():
                deriving.append(dt.getText())

        constructors: list[ConstructorModel] = []
        if ctx.constructors():
            for c in ctx.constructors().constructor():
                c_name = c.CONID().getText() if c.CONID() else ""
                constructors.append(ConstructorModel(name=c_name, is_gadt=False))

        if ctx.gadtConstructors():
            for gc in ctx.gadtConstructors().gadtConstructor():
                gc_name = gc.CONID().getText() if gc.CONID() else ""
                gc_ret = gc.typeExpr().getText() if gc.typeExpr() else ""
                constructors.append(ConstructorModel(name=gc_name, return_type=gc_ret, is_gadt=True))
                is_gadt = True

        if type_name:
            self.module.types[type_name] = TypeDeclarationModel(
                name=type_name,
                params=params,
                is_data=True,
                is_newtype=False,
                is_type_alias=False,
                is_gadt=is_gadt,
                is_type_family=is_family,
                constructors=constructors,
                deriving=deriving,
                deriving_strategies=strategies,
                location=loc,
            )

        return None

    def visitNewtypeDeclaration(self, ctx: HaskellParser.NewtypeDeclarationContext) -> Any:
        type_name = ""
        params: list[str] = []
        if ctx.simpleType():
            st = ctx.simpleType()
            if st.CONID():
                type_name = st.CONID().getText()
            for tv in st.typeVar():
                params.append(tv.getText())

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        deriving: list[str] = []
        strategies: list[str] = []
        for dc in ctx.derivingClause():
            if dc.derivingStrategy():
                strategies.append(dc.derivingStrategy().getText())
            for dt in dc.derivingTarget():
                deriving.append(dt.getText())

        constructors: list[ConstructorModel] = []
        if ctx.constructor():
            c = ctx.constructor()
            c_name = c.CONID().getText() if c.CONID() else ""
            constructors.append(ConstructorModel(name=c_name, is_gadt=False))

        if type_name:
            self.module.types[type_name] = TypeDeclarationModel(
                name=type_name,
                params=params,
                is_data=False,
                is_newtype=True,
                is_type_alias=False,
                is_gadt=False,
                is_type_family=False,
                constructors=constructors,
                deriving=deriving,
                deriving_strategies=strategies,
                location=loc,
            )

        return None

    def visitTypeSynonymDeclaration(self, ctx: HaskellParser.TypeSynonymDeclarationContext) -> Any:
        type_name = ""
        params: list[str] = []
        if ctx.simpleType():
            st = ctx.simpleType()
            if st.CONID():
                type_name = st.CONID().getText()
            for tv in st.typeVar():
                params.append(tv.getText())

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        if type_name:
            self.module.types[type_name] = TypeDeclarationModel(
                name=type_name,
                params=params,
                is_data=False,
                is_newtype=False,
                is_type_alias=True,
                is_gadt=False,
                is_type_family=False,
                location=loc,
            )

        return None

    def visitTypeFamilyDeclaration(self, ctx: HaskellParser.TypeFamilyDeclarationContext) -> Any:
        type_name = ""
        params: list[str] = []
        if ctx.simpleType():
            st = ctx.simpleType()
            if st.CONID():
                type_name = st.CONID().getText()
            for tv in st.typeVar():
                params.append(tv.getText())

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        if type_name:
            self.module.types[type_name] = TypeDeclarationModel(
                name=type_name,
                params=params,
                is_data=False,
                is_newtype=False,
                is_type_alias=False,
                is_gadt=False,
                is_type_family=True,
                location=loc,
            )

        return None

    def visitTypeClassDeclaration(self, ctx: HaskellParser.TypeClassDeclarationContext) -> Any:
        tc_name = ctx.CONID().getText() if ctx.CONID() else ""
        params = [tv.getText() for tv in ctx.typeVar()]
        superclasses: list[str] = []
        if ctx.context():
            superclasses = [c.getText() for c in ctx.context().classConstraint()]

        methods: list[str] = []
        assoc_types: list[str] = []

        if ctx.classBody():
            for m in ctx.classBody().classMember():
                if m.functionSignature():
                    methods.append(m.functionSignature().getText())
                if m.typeFamilyDeclaration():
                    if m.typeFamilyDeclaration().simpleType() and m.typeFamilyDeclaration().simpleType().CONID():
                        assoc_types.append(m.typeFamilyDeclaration().simpleType().CONID().getText())

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        if tc_name:
            self.module.typeclasses[tc_name] = TypeClassModel(
                name=tc_name,
                params=params,
                superclasses=superclasses,
                methods=methods,
                associated_types=assoc_types,
                location=loc,
            )

        return self.visitChildren(ctx)

    def visitInstanceDeclaration(self, ctx: HaskellParser.InstanceDeclarationContext) -> Any:
        c_name = ctx.CONID().getText() if ctx.CONID() else ""
        target_types = [t.getText() for t in ctx.atype()]
        target_str = " ".join(target_types)

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        if c_name:
            self.module.instances.append(
                TypeClassInstanceModel(
                    class_name=c_name,
                    target_type=target_str,
                    location=loc,
                )
            )

        return self.visitChildren(ctx)

    def visitFunctionSignature(self, ctx: HaskellParser.FunctionSignatureContext) -> Any:
        sig_text = ctx.typeExpr().getText() if ctx.typeExpr() else ""
        line = ctx.start.line if ctx.start else 1

        if ctx.varIdList():
            for qv in ctx.varIdList().qvar():
                fn_name = qv.getText()
                self._signatures[fn_name] = (sig_text, line)

        return None

    def visitFunctionBinding(self, ctx: HaskellParser.FunctionBindingContext) -> Any:
        fn_name = ctx.qvar().getText() if ctx.qvar() else ""
        if not fn_name or fn_name in ("where", "let", "in", "do", "case", "of", "if", "then", "else"):
            return None

        line = ctx.start.line if ctx.start else 1
        col = (ctx.start.column + 1) if ctx.start else 1
        loc = SourceLocation(file_path=self.file_path, line=line, column=col)

        sig, sig_line = self._signatures.get(fn_name, ("", line))
        if sig_line:
            loc = SourceLocation(file_path=self.file_path, line=sig_line, column=col)

        body = ctx.getText()
        params = [p.getText() for p in ctx.pattern()]

        calls = re.findall(r"\b([a-zA-Z0-9_.]+)\b", body)
        complexity = 1 + body.count("case") + body.count("if") + body.count("|") + body.count("->") // 2

        self.module.functions[fn_name] = FunctionModel(
            name=fn_name,
            type_signature=sig,
            params=params,
            body=body,
            cyclomatic_complexity=complexity,
            calls=calls,
            has_error=bool(re.search(r"\berror\b", body)),
            has_undefined=bool(re.search(r"\bundefined\b", body)),
            has_from_just=bool(re.search(r"\bfromJust\b", body)),
            has_lazy_foldl=bool(re.search(r"\bfoldl\s+[^\'\s]", body)),
            has_catch_all=bool(re.search(r"catch[\s\S]*?\\(?:_|\(SomeException\s+[^)]+\)\))\s*->", body)),
            has_do=("do" in body),
            location=loc,
        )

        return None
