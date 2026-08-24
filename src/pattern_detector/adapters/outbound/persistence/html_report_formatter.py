"""Standalone, interactive Semantic UI (Fomantic-UI) HTML dashboard formatter for Haskell Pattern Detector."""

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
        "badge_bg": "rgba(168, 85, 247, 0.15)",
        "badge_border": "rgba(168, 85, 247, 0.4)",
        "badge_text": "#c084fc",
        "accent": "#a855f7",
        "label_color": "purple",
    },
    PatternCategory.MONAD_ARCHITECTURE: {
        "color": "violet",
        "icon": "layer group",
        "name": "Monad Stacks & ReaderT",
        "badge_bg": "rgba(139, 92, 246, 0.15)",
        "badge_border": "rgba(139, 92, 246, 0.4)",
        "badge_text": "#a78bfa",
        "accent": "#8b5cf6",
        "label_color": "violet",
    },
    PatternCategory.FUNCTIONAL_IDIOM: {
        "color": "teal",
        "icon": "code branch",
        "name": "Functional Idioms & GADTs",
        "badge_bg": "rgba(20, 184, 166, 0.15)",
        "badge_border": "rgba(20, 184, 166, 0.4)",
        "badge_text": "#2dd4bf",
        "accent": "#14b8a6",
        "label_color": "teal",
    },
    PatternCategory.CONCURRENCY_STM: {
        "color": "blue",
        "icon": "bolt",
        "name": "STM & Concurrency",
        "badge_bg": "rgba(56, 189, 248, 0.15)",
        "badge_border": "rgba(56, 189, 248, 0.4)",
        "badge_text": "#38bdf8",
        "accent": "#0ea5e9",
        "label_color": "blue",
    },
    PatternCategory.OPTICS_LENSES: {
        "color": "pink",
        "icon": "eye",
        "name": "Optics & Lenses",
        "badge_bg": "rgba(236, 72, 153, 0.15)",
        "badge_border": "rgba(236, 72, 153, 0.4)",
        "badge_text": "#f472b6",
        "accent": "#ec4899",
        "label_color": "pink",
    },
    PatternCategory.RESILIENCE: {
        "color": "green",
        "icon": "shield alternate",
        "name": "Resilience & Space Leaks",
        "badge_bg": "rgba(34, 197, 94, 0.15)",
        "badge_border": "rgba(34, 197, 94, 0.4)",
        "badge_text": "#4ade80",
        "accent": "#22c55e",
        "label_color": "green",
    },
    PatternCategory.PRINCIPLE: {
        "color": "yellow",
        "icon": "balance scale",
        "name": "Principles & Quality",
        "badge_bg": "rgba(234, 179, 8, 0.15)",
        "badge_border": "rgba(234, 179, 8, 0.4)",
        "badge_text": "#facc15",
        "accent": "#eab308",
        "label_color": "yellow",
    },
    PatternCategory.TYPE_SAFETY: {
        "color": "red",
        "icon": "exclamation triangle",
        "name": "Type Safety Hazards",
        "badge_bg": "rgba(239, 68, 68, 0.15)",
        "badge_border": "rgba(239, 68, 68, 0.4)",
        "badge_text": "#f87171",
        "accent": "#ef4444",
        "label_color": "red",
    },
}

_HTML_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔷 DPX-Haskell: Typeclass Architecture & Monad Dashboard - {project_name}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fomantic-ui/2.9.3/semantic.min.css">
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: #151b2b;
            --border-color: #232d42;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }}
        body {{
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 30px 15px;
        }}
        .ui.container {{
            max-width: 1400px !important;
        }}
        .ui.inverted.segment {{
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
            border-radius: 10px !important;
        }}
        .ui.inverted.card {{
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
        }}
        .ui.inverted.card:hover {{
            border-color: #3b82f6 !important;
            box-shadow: 0 6px 25px rgba(59, 130, 246, 0.15) !important;
            transform: translateY(-2px);
            transition: all 0.2s ease;
        }}
        .header-title {{
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #a855f7 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }}
        .code-snippet {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background: #080c14;
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #1e293b;
            color: #38bdf8;
            font-size: 13px;
        }}
        .evidence-box {{
            background: rgba(15, 23, 42, 0.7);
            border-left: 3px solid #3b82f6;
            padding: 8px 12px;
            margin-top: 8px;
            border-radius: 0 4px 4px 0;
            font-size: 12px;
            color: #cbd5e1;
        }}
        .stat-value {{
            font-size: 28px !important;
            font-weight: 800 !important;
        }}
        .filter-btn.active {{
            background-color: #3b82f6 !important;
            color: #ffffff !important;
        }}
    </style>
</head>
<body>

<div class="ui container">

    <!-- Header Section -->
    <div class="ui inverted segment" style="margin-bottom: 25px; padding: 25px;">
        <div class="ui stackable grid items-center">
            <div class="ten wide column">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="font-size: 32px;">🔷</span>
                    <span class="header-title">DPX-Haskell Architecture & Pattern Engine</span>
                </div>
                <div style="color: var(--text-secondary); font-size: 14px;">
                    Target Codebase: <code class="code-snippet">{project_name}</code>
                </div>
            </div>
            <div class="six wide column right aligned">
                <div class="ui mini blue label">
                    <i class="layer group icon"></i> Hexagonal DDD
                </div>
                <div class="ui mini teal label">
                    <i class="clock outline icon"></i> {elapsed_seconds}s
                </div>
                <div class="ui mini purple label">
                    <i class="file alternate outline icon"></i> {scanned_files} files
                </div>
            </div>
        </div>
    </div>

    <!-- KPI Statistics -->
    <div class="ui four stackable cards" style="margin-bottom: 25px;">
        <div class="ui inverted card">
            <div class="content">
                <div class="ui top right attached label blue mini">TOTAL FINDINGS</div>
                <div class="header stat-value" style="color: #38bdf8; margin-top: 10px;">{total_detections}</div>
                <div class="description" style="color: var(--text-secondary);">Architecture patterns & smells identified</div>
            </div>
        </div>
        <div class="ui inverted card">
            <div class="content">
                <div class="ui top right attached label red mini">ACTION REQUIRED</div>
                <div class="header stat-value" style="color: #f87171; margin-top: 10px;">{total_violations}</div>
                <div class="description" style="color: var(--text-secondary);">Safety hazards, space leaks & smells</div>
            </div>
        </div>
        <div class="ui inverted card">
            <div class="content">
                <div class="ui top right attached label purple mini">TYPECLASSES & MONADS</div>
                <div class="header stat-value" style="color: #c084fc; margin-top: 10px;">{total_typeclasses_and_monads}</div>
                <div class="description" style="color: var(--text-secondary);">Typeclasses, ReaderT & Transformer stacks</div>
            </div>
        </div>
        <div class="ui inverted card">
            <div class="content">
                <div class="ui top right attached label green mini">CLEAN CODE</div>
                <div class="header stat-value" style="color: #4ade80; margin-top: 10px;">{total_adherences}</div>
                <div class="description" style="color: var(--text-secondary);">Clean functional structures & STM</div>
            </div>
        </div>
    </div>

    <!-- AI Architecture Map & Prompt Banner -->
    <div class="ui inverted segment" style="margin-bottom: 25px; border-left: 4px solid #a855f7 !important;">
        <div class="ui stackable grid items-center">
            <div class="eleven wide column">
                <h4 style="margin: 0; color: #f8fafc;">
                    <i class="magic icon" style="color: #a855f7;"></i> AI / LLM Architectural Prompt Context
                </h4>
                <p style="color: var(--text-secondary); margin-top: 6px; font-size: 13px;">
                    Generate instant refactoring recommendations, STM transaction reviews, and monad transformer optimizations for Claude, ChatGPT or Gemini.
                </p>
            </div>
            <div class="five wide column right aligned">
                <button class="ui mini purple button" id="copyLlmBtn" onclick="copyLlmContext()">
                    <i class="copy outline icon"></i> 📋 Copy Context for LLM
                </button>
            </div>
        </div>
        <textarea id="llmContextData" style="display: none;">{llm_context_data}</textarea>
    </div>

    <!-- Filter Buttons Bar -->
    <div class="ui inverted segment" style="margin-bottom: 20px; padding: 12px;">
        <div class="ui stackable grid items-center">
            <div class="twelve wide column">
                <div class="ui mini inverted buttons" id="categoryFilterBar">
                    <button class="ui button active filter-btn" data-filter="all">All ({total_detections})</button>
                    {category_filter_buttons}
                </div>
            </div>
            <div class="four wide column right aligned">
                <div class="ui mini icon inverted input fluid">
                    <input type="text" id="searchInput" placeholder="Search findings, modules, functions...">
                    <i class="search icon"></i>
                </div>
            </div>
        </div>
    </div>

    <!-- Findings Grid -->
    <div class="ui stackable cards" id="findingsContainer">
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
            }}, 2000);
        }}).catch(() => {{
            const ta = document.createElement('textarea');
            ta.value = raw;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            btn.innerHTML = '<i class="check icon"></i> Copied!';
            setTimeout(() => {{ btn.innerHTML = oldHtml; }}, 2000);
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
                    f'<button class="ui button filter-btn" data-filter="{cat.value}"><i class="{style["icon"]} icon"></i> {style["name"]} ({cnt})</button>'
                )

        cards_html = []
        for idx, d in enumerate(report.detections, 1):
            style = CATEGORY_STYLES.get(d.pattern_category, CATEGORY_STYLES[PatternCategory.FUNCTIONAL_IDIOM])
            conf_color = "green" if d.level == ConfidenceLevel.VERY_HIGH else "teal" if d.level == ConfidenceLevel.HIGH else "orange"
            loc_str = str(d.primary_location) if d.primary_location else "N/A"

            evidences_html = "".join([
                f'<div class="evidence-box">'
                f'<strong>+{int(ev.weight * 100)}% [{html.escape(ev.rule_code)}]</strong> {html.escape(ev.description)}'
                f'</div>'
                for ev in d.evidences
            ])

            cards_html.append(
                f"""
                <div class="ui inverted card finding-card" data-category="{d.pattern_category.value}" style="width: calc(50% - 1em); margin: 0.5em;">
                    <div class="content">
                        <div class="ui top right attached label mini" style="background: {style['badge_bg']}; color: {style['badge_text']}; border: 1px solid {style['badge_border']};">
                            <i class="{style['icon']} icon"></i> {style['name'].upper()}
                        </div>
                        <div class="header" style="color: #f8fafc; font-size: 15px; margin-top: 5px;">
                            #{idx} <code>{html.escape(d.pattern_type.value)}</code>
                        </div>
                        <div class="meta" style="color: var(--text-secondary); margin-top: 4px;">
                            Target: <code class="code-snippet">{html.escape(d.target_name)}</code> ({html.escape(d.target_kind)})
                        </div>
                        <div class="description" style="color: #cbd5e1; margin-top: 10px; font-size: 13px;">
                            {html.escape(d.summary)}
                        </div>
                        {evidences_html}
                    </div>
                    <div class="extra content" style="border-top: 1px solid var(--border-color); font-size: 12px; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center;">
                        <span><i class="map marker alternate icon" style="color: #f43f5e;"></i> {html.escape(loc_str)}</span>
                        <span class="ui mini {conf_color} label">{d.confidence.percentage_str} [{d.level.value.upper()}]</span>
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
