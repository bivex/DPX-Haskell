"""Filesystem repositories persisting detection reports to JSON, HTML, SARIF, and Markdown."""

from __future__ import annotations

from pathlib import Path

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort, ResultRepositoryPort


class FileResultRepository(ResultRepositoryPort):
    """Generic file persistence repository wrapping a ReportFormatterPort."""

    def __init__(self, formatter: ReportFormatterPort, output_key: str) -> None:
        self._formatter = formatter
        self.output_key = output_key

    def save(self, report: DetectionReport, destination: str) -> None:
        dest_path = Path(destination).resolve()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        content = self._formatter.format(report)
        dest_path.write_text(content, encoding="utf-8")
