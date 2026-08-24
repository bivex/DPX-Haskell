"""Dependency Injection Container for DPX-Haskell."""

from __future__ import annotations

from dataclasses import dataclass, field
from pattern_detector.adapters.outbound.parsers.native_haskell_parser_adapter import NativeHaskellParserAdapter
from pattern_detector.adapters.outbound.persistence.file_result_repositories import FileResultRepository
from pattern_detector.adapters.outbound.persistence.file_source_provider import FileSourceProvider
from pattern_detector.adapters.outbound.persistence.html_report_formatter import HtmlReportFormatter
from pattern_detector.adapters.outbound.persistence.json_report_formatter import JsonReportFormatter
from pattern_detector.adapters.outbound.persistence.llm_report_formatter import LlmReportFormatter
from pattern_detector.adapters.outbound.persistence.markdown_report_formatter import MarkdownReportFormatter
from pattern_detector.adapters.outbound.persistence.sarif_report_formatter import SarifReportFormatter
from pattern_detector.application.services.detection_service import PatternDetectorService
from pattern_detector.application.services.scanning_service import ScanningService
from pattern_detector.domain.rules import DEFAULT_RULES, PatternRule
from pattern_detector.ports.inbound import DetectorPort, ScannerPort
from pattern_detector.ports.outbound import ParserPort, SourceProviderPort


@dataclass
class Container:
    """Hexagonal Dependency Injection container."""

    rules: list[PatternRule] = field(default_factory=lambda: list(DEFAULT_RULES))

    def get_source_provider(self) -> SourceProviderPort:
        return FileSourceProvider()

    def get_parser(self) -> ParserPort:
        return NativeHaskellParserAdapter()

    def get_detector(self) -> DetectorPort:
        return PatternDetectorService(self.rules)

    def get_scanner(self) -> ScannerPort:
        json_repo = FileResultRepository(JsonReportFormatter(), "json")
        html_repo = FileResultRepository(HtmlReportFormatter(), "html")
        markdown_repo = FileResultRepository(MarkdownReportFormatter(), "markdown")
        sarif_repo = FileResultRepository(SarifReportFormatter(), "sarif")

        return ScanningService(
            source_provider=self.get_source_provider(),
            parser=self.get_parser(),
            detector=self.get_detector(),
            repositories=[json_repo, html_repo, markdown_repo, sarif_repo],
        )


def create_container(custom_rules: list[PatternRule] | None = None) -> Container:
    return Container(rules=custom_rules if custom_rules is not None else list(DEFAULT_RULES))
