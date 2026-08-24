"""AI / LLM Architectural Prompt Context Formatter for Haskell."""

from __future__ import annotations

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class LlmReportFormatter(ReportFormatterPort):
    """Outputs compact, token-efficient XML prompt context for LLMs."""

    def format(self, report: DetectionReport) -> str:
        lines = [
            "<haskell_codebase_architecture_context>",
            f"  <project target='{report.project_path}' files_scanned='{report.scanned_files_count}' detections='{report.total_detections_count}'>",
        ]

        for d in report.detections:
            loc = str(d.primary_location) if d.primary_location else "unknown"
            lines.append(
                f"    <detection pattern='{d.pattern_type.value}' category='{d.pattern_category.value}' confidence='{d.confidence.percentage_str}' target='{d.target_name}' location='{loc}'>"
            )
            lines.append(f"      <summary>{d.summary}</summary>")
            lines.append("    </detection>")

        lines.extend([
            "  </project>",
            "</haskell_codebase_architecture_context>",
        ])
        return "\n".join(lines)
