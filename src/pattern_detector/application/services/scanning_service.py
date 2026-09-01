"""Application scanning service coordinating source fetching, parsing, and report generation."""

from __future__ import annotations

import time
from typing import Sequence

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.inbound import ScanOptions, ScannerPort
from pattern_detector.ports.outbound import (
    ParserPort,
    ReportFormatterPort,
    ResultRepositoryPort,
    SourceProviderPort,
)


class ScanningService(ScannerPort):
    """Hexagonal Application service implementing ScannerPort."""

    def __init__(
        self,
        source_provider: SourceProviderPort,
        parser: ParserPort,
        detector: Any,
        repositories: Sequence[ResultRepositoryPort] | None = None,
    ) -> None:
        self._source_provider = source_provider
        self._parser = parser
        self._detector = detector
        self._repositories = list(repositories) if repositories else []

    def scan_path(self, path: str, options: ScanOptions | None = None) -> DetectionReport:
        opts = options or ScanOptions()
        t0 = time.perf_counter()

        sources = self._source_provider.get_sources(
            path,
            extensions=[".hs", ".lhs"],
            exclude_dirs=opts.exclude_dirs,
        )
        code_model = self._parser.parse_sources(sources)
        code_model.project_path = path

        detections = self._detector.detect_patterns(code_model, options=opts)
        elapsed = time.perf_counter() - t0

        report = DetectionReport(
            project_path=path,
            scanned_files_count=len(sources),
            detections=detections,
            elapsed_seconds=round(elapsed, 4),
            code_model=code_model,
        )

        self._save_report(report, opts)
        return report

    def scan_sources(self, sources: dict[str, str], options: ScanOptions | None = None) -> DetectionReport:
        opts = options or ScanOptions()
        t0 = time.perf_counter()

        code_model = self._parser.parse_sources(sources)
        detections = self._detector.detect_patterns(code_model, options=opts)
        elapsed = time.perf_counter() - t0

        return DetectionReport(
            project_path="in-memory",
            scanned_files_count=len(sources),
            detections=detections,
            elapsed_seconds=round(elapsed, 4),
            code_model=code_model,
        )

    def _save_report(self, report: DetectionReport, options: ScanOptions) -> None:
        for repo in self._repositories:
            if hasattr(repo, "output_key"):
                key = getattr(repo, "output_key")
                out_path = getattr(options, f"output_{key}_path", None)
                if out_path:
                    repo.save(report, out_path)
