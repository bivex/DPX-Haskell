"""Markdown report formatter for Haskell Architecture Analysis."""

from __future__ import annotations

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class MarkdownReportFormatter(ReportFormatterPort):
    """Renders a DetectionReport in Markdown format."""

    def format(self, report: DetectionReport) -> str:
        lines = [
            f"# 🔷 DPX-Haskell Architecture Report",
            f"",
            f"- **Target Path:** `{report.project_path}`",
            f"- **Files Scanned:** `{report.scanned_files_count}`",
            f"- **Total Detections:** `{report.total_detections_count}`",
            f"- **Scan Time:** `{report.elapsed_seconds}s`",
            f"",
            f"## 📊 Breakdown by Category",
            f"",
            f"| Category | Count |",
            f"|---|---|",
        ]

        for cat, cnt in sorted(report.summary_by_category.items()):
            lines.append(f"| `{cat}` | {cnt} |")

        lines.extend([
            f"",
            f"## 🔎 Detailed Findings",
            f"",
        ])

        for i, d in enumerate(report.detections, start=1):
            loc = f"`{d.primary_location}`" if d.primary_location else "_N/A_"
            lines.append(f"### #{i} `{d.pattern_type.value}` on `{d.target_name}`")
            lines.append(f"- **Category:** `{d.pattern_category.value}`")
            lines.append(f"- **Confidence:** {d.confidence.percentage_str} ({d.level.value.upper()})")
            lines.append(f"- **Location:** {loc}")
            lines.append(f"- **Summary:** {d.summary}")
            lines.append("")

        return "\n".join(lines)
