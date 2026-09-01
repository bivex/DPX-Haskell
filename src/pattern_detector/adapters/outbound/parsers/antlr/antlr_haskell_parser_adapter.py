"""ANTLR4 Haskell Parser Adapter implementing ParserPort."""

from __future__ import annotations

import re
from pathlib import Path
from antlr4 import CommonTokenStream, InputStream, PredictionMode
from antlr4.error.ErrorListener import ErrorListener

from pattern_detector.adapters.outbound.parsers.antlr.generated.HaskellLexer import HaskellLexer
from pattern_detector.adapters.outbound.parsers.antlr.generated.HaskellParser import HaskellParser
from pattern_detector.adapters.outbound.parsers.antlr.haskell_cst_visitor import HaskellCstVisitor
from pattern_detector.adapters.outbound.parsers.native_haskell_parser_adapter import NativeHaskellParserAdapter
from pattern_detector.domain.code_model import CodeModel, ModuleModel
from pattern_detector.ports.outbound import ParserPort


class SilentErrorListener(ErrorListener):
    """Silent error listener suppressing stderr output during parser recovery."""

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        pass


class AntlrHaskellParserAdapter(ParserPort):
    """Production-grade ANTLR4 Haskell parser adapter for DPX-Haskell."""

    def __init__(self, fallback_to_native: bool = True) -> None:
        self._fallback_to_native = fallback_to_native
        self._native_parser = NativeHaskellParserAdapter()

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_text in sources.items():
            mod = self.parse_file(file_path, source_text)
            model.modules[mod.name] = mod
        return model

    def parse_file(self, file_path: str, source_text: str) -> ModuleModel:
        try:
            # 1. Clean comments and strings for robust layout analysis
            clean_text = self._native_parser._strip_comments_and_strings(source_text)

            # 2. Tokenize with ANTLR4 HaskellLexer
            input_stream = InputStream(source_text)
            lexer = HaskellLexer(input_stream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(SilentErrorListener())

            token_stream = CommonTokenStream(lexer)

            # 3. Parse with ANTLR4 HaskellParser using SLL prediction mode for O(N) performance
            parser = HaskellParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(SilentErrorListener())
            parser._interp.predictionMode = PredictionMode.SLL

            tree = parser.haskellModule()

            # 4. Visit parse tree with HaskellCstVisitor
            visitor = HaskellCstVisitor(
                file_path=file_path,
                raw_source=source_text,
                clean_source=clean_text,
            )
            module = visitor.visit(tree)

            # Ensure pragmas and imports are fully populated
            if not module.pragmas:
                module.pragmas = self._native_parser._parse_pragmas(source_text)
            if not module.imports:
                module.imports = self._native_parser._parse_imports(clean_text)

            # If ANTLR tree captured empty types/functions (e.g. complex layout block), supplement with native parser
            if not module.types and not module.functions and self._fallback_to_native:
                native_mod = self._native_parser.parse_file(file_path, source_text)
                return native_mod

            # Supplement top-level function models
            native_funcs = self._native_parser._parse_functions(clean_text, file_path)
            for fn_name, fn_model in native_funcs.items():
                if fn_name not in module.functions:
                    module.functions[fn_name] = fn_model

            return module
        except Exception:
            if self._fallback_to_native:
                return self._native_parser.parse_file(file_path, source_text)
            raise
