"""Standalone, high-visibility Semantic UI (Fomantic-UI) HTML dashboard formatter for Haskell Pattern Detector."""

from __future__ import annotations

import html
import os
from typing import Any

from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import (
    ConfidenceLevel,
    PatternCategory,
    PatternType,
)
from pattern_detector.ports.outbound import ReportFormatterPort

CATEGORY_STYLES = {
    PatternCategory.TYPECLASS_SYSTEM: {
        "color": "purple",
        "icon": "cubes",
        "name": "Typeclasses & Polymorphism",
        "badge_bg": "rgba(168, 85, 247, 0.2)",
        "badge_border": "rgba(168, 85, 247, 0.5)",
        "badge_text": "#d8b4fe",
        "accent": "#a855f7",
        "label_color": "purple",
    },
    PatternCategory.MONAD_ARCHITECTURE: {
        "color": "violet",
        "icon": "layer group",
        "name": "Monad Stacks & ReaderT",
        "badge_bg": "rgba(139, 92, 246, 0.2)",
        "badge_border": "rgba(139, 92, 246, 0.5)",
        "badge_text": "#c4b5fd",
        "accent": "#8b5cf6",
        "label_color": "violet",
    },
    PatternCategory.FUNCTIONAL_IDIOM: {
        "color": "teal",
        "icon": "code branch",
        "name": "Functional Idioms & GADTs",
        "badge_bg": "rgba(20, 184, 166, 0.2)",
        "badge_border": "rgba(20, 184, 166, 0.5)",
        "badge_text": "#5eead4",
        "accent": "#14b8a6",
        "label_color": "teal",
    },
    PatternCategory.CONCURRENCY_STM: {
        "color": "blue",
        "icon": "bolt",
        "name": "STM & Concurrency",
        "badge_bg": "rgba(56, 189, 248, 0.2)",
        "badge_border": "rgba(56, 189, 248, 0.5)",
        "badge_text": "#7dd3fc",
        "accent": "#0ea5e9",
        "label_color": "blue",
    },
    PatternCategory.OPTICS_LENSES: {
        "color": "pink",
        "icon": "eye",
        "name": "Optics & Lenses",
        "badge_bg": "rgba(236, 72, 153, 0.2)",
        "badge_border": "rgba(236, 72, 153, 0.5)",
        "badge_text": "#f9a8d4",
        "accent": "#ec4899",
        "label_color": "pink",
    },
    PatternCategory.RESILIENCE: {
        "color": "green",
        "icon": "shield alternate",
        "name": "Resilience & Space Leaks",
        "badge_bg": "rgba(34, 197, 94, 0.2)",
        "badge_border": "rgba(34, 197, 94, 0.5)",
        "badge_text": "#86efac",
        "accent": "#22c55e",
        "label_color": "green",
    },
    PatternCategory.PRINCIPLE: {
        "color": "yellow",
        "icon": "balance scale",
        "name": "Principles & Quality",
        "badge_bg": "rgba(234, 179, 8, 0.2)",
        "badge_border": "rgba(234, 179, 8, 0.5)",
        "badge_text": "#fde047",
        "accent": "#eab308",
        "label_color": "yellow",
    },
    PatternCategory.TYPE_SAFETY: {
        "color": "red",
        "icon": "exclamation triangle",
        "name": "Type Safety Hazards",
        "badge_bg": "rgba(239, 68, 68, 0.2)",
        "badge_border": "rgba(239, 68, 68, 0.5)",
        "badge_text": "#fca5a5",
        "accent": "#ef4444",
        "label_color": "red",
    },
}

_HTML_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔷 DPX-Haskell: Architecture & Pattern Dashboard - {project_name}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fomantic-ui/2.9.3/semantic.min.css">
    <style>
        :root {{
            --bg-main: #060911;
            --bg-card: #0f1523;
            --bg-card-hover: #141c2e;
            --border-color: #1e293b;
            --border-hover: #38bdf8;
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Segoe UI", Roboto, sans-serif;
            padding: 32px 20px;
            line-height: 1.5;
        }}
        .ui.container {{
            max-width: 1440px !important;
        }}
        .ui.inverted.segment {{
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45) !important;
            border-radius: 12px !important;
        }}
        .ui.inverted.card {{
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
        }}
        .ui.inverted.card:hover {{
            background-color: var(--bg-card-hover) !important;
            border-color: var(--border-hover) !important;
            box-shadow: 0 10px 30px rgba(56, 189, 248, 0.2) !important;
            transform: translateY(-3px);
        }}
        .header-title {{
            font-size: 30px;
            font-weight: 900;
            letter-spacing: -0.6px;
            background: linear-gradient(135deg, #c084fc 0%, #38bdf8 50%, #4ade80 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            white-space: nowrap;
        }}
        .code-snippet {{
            font-family: "JetBrains Mono", "Fira Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background: #040711;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid #1e293b;
            color: #38bdf8;
            font-size: 14px;
            font-weight: 600;
        }}
        .code-snippet-large {{
            font-family: "JetBrains Mono", "Fira Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background: #040711;
            padding: 5px 12px;
            border-radius: 6px;
            border: 1px solid #223049;
            color: #67e8f9;
            font-size: 14.5px;
            font-weight: 700;
            display: inline-block;
            word-break: break-all;
        }}
        .evidence-box {{
            background: #080d19;
            border-left: 4px solid #38bdf8;
            padding: 10px 14px;
            margin-top: 8px;
            border-radius: 0 6px 6px 0;
            font-size: 13px;
            color: #e2e8f0;
            line-height: 1.5;
            border-top: 1px solid #131d2e;
            border-right: 1px solid #131d2e;
            border-bottom: 1px solid #131d2e;
        }}
        .stat-value {{
            font-size: 36px !important;
            font-weight: 900 !important;
            letter-spacing: -1px;
            line-height: 1.1;
        }}
        .stat-desc {{
            color: #94a3b8 !important;
            font-size: 13.5px !important;
            font-weight: 500;
            margin-top: 6px;
        }}
        .filter-btn {{
            font-size: 13px !important;
            font-weight: 700 !important;
            padding: 9px 15px !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
        }}
        .filter-btn.active {{
            background-color: #2563eb !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        }}
        .location-pill {{
            font-family: "JetBrains Mono", ui-monospace, monospace;
            font-size: 12px;
            color: #f472b6;
            background: rgba(244, 114, 182, 0.1);
            padding: 5px 10px;
            border-radius: 6px;
            border: 1px solid rgba(244, 114, 182, 0.3);
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            max-width: 68%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .conf-badge {{
            flex-shrink: 0 !important;
            white-space: nowrap !important;
            font-weight: 800 !important;
            font-size: 11.5px !important;
            letter-spacing: 0.5px !important;
            padding: 6px 11px !important;
            border-radius: 6px !important;
        }}
        .finding-summary {{
            font-size: 14.5px;
            line-height: 1.6;
            color: #f1f5f9;
            font-weight: 500;
        }}
        #searchInput {{
            background: #080d19 !important;
            border: 1px solid #223049 !important;
            color: #ffffff !important;
            font-size: 14px !important;
            padding: 11px 16px !important;
            border-radius: 8px !important;
        }}
        #searchInput:focus {{
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3) !important;
        }}
    </style>
</head>
<body>

<div class="ui container">

    <!-- Header Section -->
    <div class="ui inverted segment" style="margin-bottom: 28px; padding: 26px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="font-size: 32px;">🔷</span>
                    <span class="header-title">DPX-Haskell Architecture & Pattern Engine</span>
                </div>
                <div style="color: var(--text-secondary); font-size: 14.5px;">
                    Target Codebase: <code class="code-snippet">{project_name}</code>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <div class="ui medium blue label" style="font-weight: 700;">
                    <i class="layer group icon"></i> Hexagonal DDD
                </div>
                <div class="ui medium teal label" style="font-weight: 700;">
                    <i class="clock outline icon"></i> {elapsed_seconds}s
                </div>
                <div class="ui medium purple label" style="font-weight: 700;">
                    <i class="file alternate outline icon"></i> {scanned_files} files
                </div>
            </div>
        </div>
    </div>

    <!-- KPI Statistics -->
    <div class="ui four stackable cards" style="margin-bottom: 28px;">
        <div class="ui inverted card" style="border-top: 3px solid #38bdf8 !important;">
            <div class="content" style="padding: 20px;">
                <div class="ui top right attached label blue mini" style="font-weight: 700;">TOTAL FINDINGS</div>
                <div class="header stat-value" style="color: #38bdf8; margin-top: 8px;">{total_detections}</div>
                <div class="description stat-desc">Total patterns & architecture findings</div>
            </div>
        </div>
        <div class="ui inverted card" style="border-top: 3px solid #f87171 !important;">
            <div class="content" style="padding: 20px;">
                <div class="ui top right attached label red mini" style="font-weight: 700;">ACTION REQUIRED</div>
                <div class="header stat-value" style="color: #f87171; margin-top: 8px;">{total_violations}</div>
                <div class="description stat-desc">Safety hazards, space leaks & smells</div>
            </div>
        </div>
        <div class="ui inverted card" style="border-top: 3px solid #c084fc !important;">
            <div class="content" style="padding: 20px;">
                <div class="ui top right attached label purple mini" style="font-weight: 700;">TYPECLASSES & MONADS</div>
                <div class="header stat-value" style="color: #c084fc; margin-top: 8px;">{total_typeclasses_and_monads}</div>
                <div class="description stat-desc">Typeclasses, ReaderT & Transformer stacks</div>
            </div>
        </div>
        <div class="ui inverted card" style="border-top: 3px solid #4ade80 !important;">
            <div class="content" style="padding: 20px;">
                <div class="ui top right attached label green mini" style="font-weight: 700;">CLEAN CODE & STM</div>
                <div class="header stat-value" style="color: #4ade80; margin-top: 8px;">{total_adherences}</div>
                <div class="description stat-desc">Clean functional idioms & STM transactions</div>
            </div>
        </div>
    </div>

    <!-- AI Architecture Map & Prompt Banner -->
    <div class="ui inverted segment" style="margin-bottom: 28px; padding: 22px; border-left: 5px solid #a855f7 !important;">
        <div class="ui stackable grid items-center">
            <div class="eleven wide column">
                <h3 style="margin: 0; color: #ffffff; font-size: 17px; font-weight: 800; display: flex; align-items: center; gap: 8px;">
                    <i class="magic icon" style="color: #c084fc;"></i> AI / LLM Architectural Prompt Context
                </h3>
                <p style="color: #cbd5e1; margin-top: 6px; font-size: 14px; line-height: 1.5;">
                    Generate instant refactoring recommendations, STM transaction reviews, and monad transformer optimizations formatted for Claude, ChatGPT, or Gemini.
                </p>
            </div>
            <div class="five wide column right aligned">
                <button class="ui medium purple button" id="copyLlmBtn" onclick="copyLlmContext()" style="font-weight: 800; padding: 12px 20px;">
                    <i class="copy outline icon"></i> 📋 Copy Context for LLM
                </button>
            </div>
        </div>
        <textarea id="llmContextData" style="display: none;">{llm_context_data}</textarea>
    </div>

    <!-- Filter Buttons Bar & Search -->
    <div class="ui inverted segment" style="margin-bottom: 24px; padding: 16px 20px;">
        <div class="ui stackable grid items-center">
            <div class="eleven wide column">
                <div class="ui inverted buttons" id="categoryFilterBar" style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <button class="ui button active filter-btn" data-filter="all">All Findings ({total_detections})</button>
                    {category_filter_buttons}
                </div>
            </div>
            <div class="five wide column right aligned">
                <div class="ui fluid icon inverted input">
                    <input type="text" id="searchInput" placeholder="🔎 Search findings, modules, functions...">
                    <i class="search icon" style="color: #38bdf8;"></i>
                </div>
            </div>
        </div>
    </div>

    <!-- Findings Grid -->
    <div class="ui stackable cards" id="findingsContainer" style="margin: -0.5em;">
        {findings_cards_html}
    </div>

</div>

<script>
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.finding-card');
    const filterBtns = document.querySelectorAll('.filter-btn');

    let currentCategory = 'all';

    function applyFilters() {{
        const query = searchInput.value.toLowerCase().trim();

        cards.forEach(card => {{
            const category = card.dataset.category || '';
            const text = card.textContent.toLowerCase();

            const matchesCategory = (currentCategory === 'all' || category === currentCategory);
            const matchesSearch = (!query || text.includes(query));

            if (matchesCategory && matchesSearch) {{
                card.style.display = 'flex';
            }} else {{
                card.style.display = 'none';
            }}
        }});
    }}

    searchInput.addEventListener('input', applyFilters);

    filterBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.filter;
            applyFilters();
        }});
    }});

    function copyLlmContext() {{
        const raw = document.getElementById('llmContextData').value;
        const btn = document.getElementById('copyLlmBtn');
        const oldHtml = btn.innerHTML;

        navigator.clipboard.writeText(raw).then(() => {{
            btn.innerHTML = '<i class="check icon"></i> Copied to Clipboard!';
            btn.classList.remove('purple');
            btn.classList.add('green');
            setTimeout(() => {{
                btn.innerHTML = oldHtml;
                btn.classList.remove('green');
                btn.classList.add('purple');
            }}, 2200);
        }}).catch(() => {{
            const ta = document.createElement('textarea');
            ta.value = raw;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            btn.innerHTML = '<i class="check icon"></i> Copied!';
            setTimeout(() => {{ btn.innerHTML = oldHtml; }}, 2200);
        }});
    }}
</script>

</body>
</html>
"""


class HtmlReportFormatter(ReportFormatterPort):
    """Generates an interactive, dark-themed Semantic UI (Fomantic-UI) dashboard for Haskell."""

    def format(self, report: DetectionReport) -> str:
        project_name = self._resolve_project_name(report.project_path)

        # Classify violations vs adherences vs patterns
        violations_count = 0
        adherences_count = 0
        typeclasses_and_monads_count = 0

        for d in report.detections:
            if d.pattern_category in (PatternCategory.TYPE_SAFETY, PatternCategory.RESILIENCE, PatternCategory.PRINCIPLE):
                violations_count += 1
            elif d.pattern_category in (PatternCategory.TYPECLASS_SYSTEM, PatternCategory.MONAD_ARCHITECTURE):
                typeclasses_and_monads_count += 1
            else:
                adherences_count += 1

        filter_buttons = []
        for cat, style in CATEGORY_STYLES.items():
            cnt = report.summary_by_category.get(cat.value, 0)
            if cnt > 0:
                filter_buttons.append(
                    f'<button class="ui button filter-btn" data-filter="{cat.value}"><i class="{style["icon"]} icon" style="color: {style["accent"]};"></i> {style["name"]} ({cnt})</button>'
                )

        cards_html = []
        for idx, d in enumerate(report.detections, 1):
            style = CATEGORY_STYLES.get(d.pattern_category, CATEGORY_STYLES[PatternCategory.FUNCTIONAL_IDIOM])
            conf_color = "green" if d.level == ConfidenceLevel.VERY_HIGH else "teal" if d.level == ConfidenceLevel.HIGH else "orange"
            raw_loc = str(d.primary_location) if d.primary_location else "N/A"
            disp_loc, full_loc = self._format_display_location(raw_loc, report.project_path)

            evidences_html = "".join([
                f'<div class="evidence-box" style="border-left-color: {style["accent"]};">'
                f'<span style="color: {style["badge_text"]}; font-weight: 800; font-family: monospace;">+{int(ev.weight * 100)}%</span> '
                f'<span style="color: #94a3b8; font-family: monospace; font-size: 11.5px; font-weight: 600;">[{html.escape(ev.rule_code)}]</span> '
                f'<span style="color: #f1f5f9;">{html.escape(ev.description)}</span>'
                f'</div>'
                for ev in d.evidences
            ])

            cards_html.append(
                f"""
                <div class="ui inverted card finding-card" data-category="{d.pattern_category.value}" style="width: calc(50% - 1em); margin: 0.5em; border-left: 5px solid {style['accent']} !important;">
                    <div class="content" style="padding: 18px 20px;">
                        <div class="ui top right attached label" style="background: {style['badge_bg']}; color: {style['badge_text']}; border: 1px solid {style['badge_border']}; font-weight: 800; font-size: 11px; letter-spacing: 0.5px;">
                            <i class="{style['icon']} icon"></i> {style['name'].upper()}
                        </div>
                        <div class="header" style="color: #ffffff; font-size: 16px; font-weight: 800; margin-top: 4px; display: flex; align-items: center; gap: 8px;">
                            <span style="color: #64748b; font-size: 14px;">#{idx}</span>
                            <span style="color: #38bdf8;"><code>{html.escape(d.pattern_type.value)}</code></span>
                        </div>
                        <div class="meta" style="color: var(--text-secondary); margin-top: 8px; font-size: 13.5px;">
                            <span style="color: #94a3b8; font-weight: 600;">Target:</span> <code class="code-snippet-large">{html.escape(d.target_name)}</code>
                            <span class="ui mini label" style="background: #1e293b; color: #94a3b8; margin-left: 6px;">{html.escape(d.target_kind)}</span>
                        </div>
                        <div class="description finding-summary" style="margin-top: 12px;">
                            {html.escape(d.summary)}
                        </div>
                        <div style="margin-top: 14px;">
                            <div style="font-size: 11.5px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 4px;">
                                <i class="search icon"></i> Evidence Trail ({len(d.evidences)} heuristics):
                            </div>
                            {evidences_html}
                        </div>
                    </div>
                    <div class="extra content" style="border-top: 1px solid var(--border-color); padding: 12px 20px; font-size: 13px; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                        <span class="location-pill" title="{html.escape(full_loc)}"><i class="map marker alternate icon"></i> {html.escape(disp_loc)}</span>
                        <span class="ui mini {conf_color} label conf-badge">{d.confidence.percentage_str} [{d.level.value.upper()}]</span>
                    </div>
                </div>
                """
            )

        llm_context = self._generate_llm_prompt(report, project_name)

        return _HTML_DASHBOARD_TEMPLATE.format(
            project_name=project_name,
            total_detections=report.total_detections_count,
            total_violations=violations_count,
            total_typeclasses_and_monads=typeclasses_and_monads_count,
            total_adherences=adherences_count,
            scanned_files=report.scanned_files_count,
            elapsed_seconds=f"{report.elapsed_seconds:.3f}",
            category_filter_buttons="\n".join(filter_buttons),
            findings_cards_html="\n".join(cards_html),
            llm_context_data=html.escape(llm_context),
        )

    def _format_display_location(self, loc_str: str, project_path: str) -> tuple[str, str]:
        """Formats location string to be concise for card display while preserving full path for tooltips."""
        if not loc_str or loc_str == "N/A":
            return "N/A", ""

        full_loc = loc_str
        clean_proj = project_path.rstrip("/\\")
        if clean_proj and loc_str.startswith(clean_proj):
            rel = loc_str[len(clean_proj):].lstrip("/\\")
            return rel, full_loc

        # If long absolute path, display trailing segments
        parts = loc_str.replace("\\", "/").split("/")
        if len(parts) > 4:
            short = ".../" + "/".join(parts[-3:])
            return short, full_loc

        return loc_str, full_loc

    def _resolve_project_name(self, path: str) -> str:
        if not path or path == ".":
            return "Current Codebase"
        return os.path.basename(path.rstrip("/\\")) or path

    def _generate_llm_prompt(self, report: DetectionReport, project_name: str) -> str:
        lines = [
            f"# 🔷 DPX-Haskell: Architectural Context & Refactoring Prompt for {project_name}",
            f"- Scanned Files: {report.scanned_files_count}",
            f"- Total Detections: {report.total_detections_count}",
            "",
            "## Identified Patterns & Smells:",
        ]
        for d in report.detections:
            loc = f" in {d.primary_location}" if d.primary_location else ""
            lines.append(f"- [{d.pattern_category.value}] {d.pattern_type.value} on `{d.target_name}` ({d.confidence.percentage_str}){loc}: {d.summary}")

        lines.extend([
            "",
            "## Instructions for AI Architect:",
            "1. Review typeclass hierarchies, associated types, and GADTs for clean modularity.",
            "2. Audit ReaderT application stacks and eliminate unnecessary monad transformer layering.",
            "3. Inspect STM blocks (`TVar`/`atomically`) and verify retry loop termination.",
            "4. Eliminate unforced space leaks (replace lazy `foldl` with strict `foldl'`) and unsafe `fromJust`/`error` panics.",
        ])
        return "\n".join(lines)
