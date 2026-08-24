"""Interactive Dark-Mode HTML Dashboard for Haskell Architecture & Patterns."""

from __future__ import annotations

import html
from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class HtmlReportFormatter(ReportFormatterPort):
    """Formats a DetectionReport into an interactive dark-theme HTML page."""

    def format(self, report: DetectionReport) -> str:
        cats = report.summary_by_category
        conf = report.summary_by_confidence_level

        det_rows = []
        for i, d in enumerate(report.detections, start=1):
            loc_str = html.escape(str(d.primary_location)) if d.primary_location else "N/A"
            conf_badge = f'<span class="badge {d.level.value}">{d.confidence.percentage_str} [{d.level.value.upper()}]</span>'
            summary_txt = html.escape(d.summary)
            target_txt = html.escape(d.target_name)
            p_type = html.escape(d.pattern_type.value)
            p_cat = html.escape(d.pattern_category.value)

            det_rows.append(
                f"""
                <tr class="detection-row" data-category="{p_cat}" data-level="{d.level.value}">
                    <td>#{i}</td>
                    <td><strong><code>{p_type}</code></strong></td>
                    <td><span class="cat-badge">{p_cat}</span></td>
                    <td><code>{target_txt}</code></td>
                    <td>{conf_badge}</td>
                    <td><small>{loc_str}</small></td>
                    <td>{summary_txt}</td>
                </tr>
                """
            )

        rows_html = "\n".join(det_rows)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DPX-Haskell: Architecture & Pattern Dashboard</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --border-color: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-purple: #9333ea;
            --accent-blue: #38bdf8;
            --accent-green: #22c55e;
            --accent-yellow: #eab308;
            --accent-red: #ef4444;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 24px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .title {{
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
        }}
        .card-num {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-blue);
        }}
        .card-label {{
            color: var(--text-muted);
            font-size: 0.875rem;
            margin-top: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background-color: #0b1120;
            color: var(--text-muted);
            font-weight: 600;
        }}
        tr:hover {{
            background-color: rgba(255, 255, 255, 0.02);
        }}
        .badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge.very_high {{ background-color: rgba(34, 197, 94, 0.2); color: var(--accent-green); border: 1px solid var(--accent-green); }}
        .badge.high {{ background-color: rgba(56, 189, 248, 0.2); color: var(--accent-blue); border: 1px solid var(--accent-blue); }}
        .badge.medium {{ background-color: rgba(234, 179, 8, 0.2); color: var(--accent-yellow); border: 1px solid var(--accent-yellow); }}
        .badge.low {{ background-color: rgba(239, 68, 68, 0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }}
        .cat-badge {{
            background-color: rgba(147, 51, 234, 0.2);
            color: #d8b4fe;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
        }}
        code {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            color: #f472b6;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="title">DPX-Haskell Architecture Report</div>
            <div style="color: var(--text-muted); margin-top: 4px;">Target: <code>{html.escape(report.project_path)}</code></div>
        </div>
        <div style="text-align: right; color: var(--text-muted); font-size: 0.875rem;">
            Scanned in <strong>{report.elapsed_seconds}s</strong>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-num">{report.scanned_files_count}</div>
            <div class="card-label">Files Scanned</div>
        </div>
        <div class="card">
            <div class="card-num">{report.total_detections_count}</div>
            <div class="card-label">Total Detections</div>
        </div>
        <div class="card">
            <div class="card-num">{cats.get("typeclass_system", 0)}</div>
            <div class="card-label">Typeclass & Polymorphism</div>
        </div>
        <div class="card">
            <div class="card-num">{cats.get("monad_architecture", 0)}</div>
            <div class="card-label">Monads & ReaderT</div>
        </div>
        <div class="card">
            <div class="card-num">{cats.get("concurrency_stm", 0)}</div>
            <div class="card-label">STM & Async Concurrency</div>
        </div>
        <div class="card">
            <div class="card-num">{cats.get("resilience", 0) + cats.get("type_safety", 0)}</div>
            <div class="card-label">Safety & Space Leak Hazards</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Pattern / Rule</th>
                <th>Category</th>
                <th>Target</th>
                <th>Confidence</th>
                <th>Location</th>
                <th>Summary</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</body>
</html>
"""
