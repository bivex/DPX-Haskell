"""
Elite, production-grade Cyber-Architectural HTML Dashboard Formatter for DPX-Haskell.
Designed with Gemini 3 Pro + Claude frontend design principles:
- Bold Aesthetic: Monadic Cyber-Blueprint & Deep Void Glassmorphism
- Distinctive Typography: Syne (Display) + Plus Jakarta Sans (Body) + JetBrains Mono (Code)
- Signature Element: Holographic Monad HUD, Live Reactive Pill Filters, Glassmorphic Cards
"""

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

CATEGORY_THEMES = {
    PatternCategory.TYPECLASS_SYSTEM: {
        "name": "Typeclasses & Polymorphism",
        "icon": "⟨T⟩",
        "accent": "#00f0ff",
        "glow": "rgba(0, 240, 255, 0.25)",
        "badge_bg": "rgba(0, 240, 255, 0.12)",
        "border": "rgba(0, 240, 255, 0.35)",
        "text": "#67e8f9",
    },
    PatternCategory.MONAD_ARCHITECTURE: {
        "name": "Monad Stacks & ReaderT",
        "icon": "λ⟦M⟧",
        "accent": "#b026ff",
        "glow": "rgba(176, 38, 255, 0.25)",
        "badge_bg": "rgba(176, 38, 255, 0.12)",
        "border": "rgba(176, 38, 255, 0.35)",
        "text": "#d8b4fe",
    },
    PatternCategory.FUNCTIONAL_IDIOM: {
        "name": "Functional Idioms & GADTs",
        "icon": "ƒ(x)",
        "accent": "#2dd4bf",
        "glow": "rgba(45, 212, 191, 0.25)",
        "badge_bg": "rgba(45, 212, 191, 0.12)",
        "border": "rgba(45, 212, 191, 0.35)",
        "text": "#5eead4",
    },
    PatternCategory.CONCURRENCY_STM: {
        "name": "STM & Concurrency",
        "icon": "⚡STM",
        "accent": "#38bdf8",
        "glow": "rgba(56, 189, 248, 0.25)",
        "badge_bg": "rgba(56, 189, 248, 0.12)",
        "border": "rgba(56, 189, 248, 0.35)",
        "text": "#7dd3fc",
    },
    PatternCategory.OPTICS_LENSES: {
        "name": "Optics & Lenses",
        "icon": "⊙_⊙",
        "accent": "#f472b6",
        "glow": "rgba(244, 114, 182, 0.25)",
        "badge_bg": "rgba(244, 114, 182, 0.12)",
        "border": "rgba(244, 114, 182, 0.35)",
        "text": "#f9a8d4",
    },
    PatternCategory.RESILIENCE: {
        "name": "Resilience & Space Leaks",
        "icon": "🛡️Ω",
        "accent": "#00ff9d",
        "glow": "rgba(0, 255, 157, 0.25)",
        "badge_bg": "rgba(0, 255, 157, 0.12)",
        "border": "rgba(0, 255, 157, 0.35)",
        "text": "#86efac",
    },
    PatternCategory.PRINCIPLE: {
        "name": "Principles & Quality",
        "icon": "⚖️📐",
        "accent": "#ffb700",
        "glow": "rgba(255, 183, 0, 0.25)",
        "badge_bg": "rgba(255, 183, 0, 0.12)",
        "border": "rgba(255, 183, 0, 0.35)",
        "text": "#fde047",
    },
    PatternCategory.TYPE_SAFETY: {
        "name": "Type Safety Hazards",
        "icon": "⚠️⊥",
        "accent": "#ff2a6d",
        "glow": "rgba(255, 42, 109, 0.25)",
        "badge_bg": "rgba(255, 42, 109, 0.12)",
        "border": "rgba(255, 42, 109, 0.35)",
        "text": "#fca5a5",
    },
}

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔷 DPX-Haskell HUD — {project_name}</title>
    <!-- Google Fonts: Syne, Plus Jakarta Sans, JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@700;800;900&display=swap" rel="stylesheet">

    <style>
        :root {{
            --bg-void: #04060c;
            --bg-surface: #090e1a;
            --bg-surface-elevated: #0f172a;
            --bg-card: rgba(13, 20, 36, 0.75);
            --bg-card-hover: rgba(19, 29, 53, 0.9);
            --border-dim: #182338;
            --border-bright: #283958;
            --cyan: #00f0ff;
            --cyan-glow: rgba(0, 240, 255, 0.25);
            --purple: #b026ff;
            --purple-glow: rgba(176, 38, 255, 0.25);
            --emerald: #00ff9d;
            --emerald-glow: rgba(0, 255, 157, 0.25);
            --rose: #ff2a6d;
            --rose-glow: rgba(255, 42, 109, 0.25);
            --amber: #ffb700;
            --amber-glow: rgba(255, 183, 0, 0.25);
            --text-pure: #ffffff;
            --text-bright: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-dim: #64748b;
            --font-display: 'Syne', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-code: 'JetBrains Mono', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        html {{
            font-size: 16px;
        }}

        body {{
            background-color: var(--bg-void);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(176, 38, 255, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
                linear-gradient(rgba(24, 35, 56, 0.15) 1px, transparent 1px),
                linear-gradient(90deg, rgba(24, 35, 56, 0.15) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 32px 32px, 32px 32px;
            color: var(--text-bright);
            font-family: var(--font-body);
            line-height: 1.6;
            padding: 40px 24px 80px 24px;
            min-height: 100vh;
        }}

        .hud-container {{
            max-width: 1440px;
            margin: 0 auto;
        }}

        /* Header Cyberpunk HUD */
        .hud-header {{
            min-height: 120px;
            background: linear-gradient(135deg, rgba(13, 20, 36, 0.9) 0%, rgba(9, 14, 26, 0.95) 100%);
            border: 1px solid var(--border-bright);
            border-radius: 16px;
            padding: 32px 36px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }}


        .hud-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--purple), var(--cyan), var(--emerald));
        }}

        .header-flex {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .header-brand {{
            display: flex;
            align-items: center;
            gap: 18px;
        }}

        .monad-logo-badge {{
            width: 56px;
            height: 56px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(176, 38, 255, 0.2) 0%, rgba(0, 240, 255, 0.2) 100%);
            border: 1px solid var(--cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            box-shadow: 0 0 20px var(--cyan-glow);
        }}

        .hud-title {{
            font-family: var(--font-display);
            font-size: 34px;
            font-weight: 900;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, var(--cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }}

        .target-tag {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 6px;
            font-size: 14.5px;
            color: var(--text-secondary);
        }}

        .code-pill {{
            font-family: var(--font-code);
            background: rgba(0, 240, 255, 0.1);
            color: var(--cyan);
            border: 1px solid rgba(0, 240, 255, 0.3);
            padding: 3px 10px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13.5px;
        }}

        .meta-pills {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .meta-pill {{
            font-family: var(--font-code);
            font-size: 12.5px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 8px;
            background: rgba(24, 35, 56, 0.6);
            border: 1px solid var(--border-bright);
            color: var(--text-bright);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        /* Holographic KPI Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 14px;
            padding: 22px 24px;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: var(--border-bright);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        }}

        .kpi-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
        }}

        .kpi-card.cyan::after {{ background: var(--cyan); box-shadow: 0 0 10px var(--cyan-glow); }}
        .kpi-card.rose::after {{ background: var(--rose); box-shadow: 0 0 10px var(--rose-glow); }}
        .kpi-card.purple::after {{ background: var(--purple); box-shadow: 0 0 10px var(--purple-glow); }}
        .kpi-card.emerald::after {{ background: var(--emerald); box-shadow: 0 0 10px var(--emerald-glow); }}

        .kpi-label {{
            font-family: var(--font-code);
            font-size: 11.5px;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--text-dim);
        }}

        .kpi-value {{
            font-family: var(--font-display);
            font-size: 40px;
            font-weight: 900;
            letter-spacing: -1px;
            margin: 6px 0;
            line-height: 1.1;
        }}

        .kpi-desc {{
            font-size: 13.5px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        /* AI Prompt Banner */
        .ai-banner {{
            background: linear-gradient(135deg, rgba(176, 38, 255, 0.12) 0%, rgba(9, 14, 26, 0.8) 100%);
            border: 1px solid rgba(176, 38, 255, 0.4);
            border-left: 5px solid var(--purple);
            border-radius: 14px;
            padding: 24px 28px;
            margin-bottom: 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 18px;
            box-shadow: 0 8px 30px rgba(176, 38, 255, 0.1);
        }}

        .ai-title {{
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .ai-btn {{
            font-family: var(--font-code);
            background: linear-gradient(135deg, var(--purple) 0%, #7928ca 100%);
            color: #ffffff;
            border: none;
            padding: 12px 22px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 13.5px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 20px var(--purple-glow);
            transition: all 0.2s ease;
        }}

        .ai-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(176, 38, 255, 0.5);
        }}

        /* Filter Controls */
        .controls-bar {{
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 28px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .category-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .cat-pill-btn {{
            font-family: var(--font-body);
            font-size: 13px;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 8px;
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border-bright);
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .cat-pill-btn:hover {{
            color: var(--text-pure);
            border-color: var(--cyan);
            background: rgba(0, 240, 255, 0.08);
        }}

        .cat-pill-btn.active {{
            background: var(--cyan);
            color: #04060c;
            border-color: var(--cyan);
            font-weight: 800;
            box-shadow: 0 0 15px var(--cyan-glow);
        }}

        .search-box-wrap {{
            position: relative;
            width: 100%;
        }}

        .search-input {{
            width: 100%;
            background: var(--bg-void);
            border: 1px solid var(--border-bright);
            color: #ffffff;
            font-family: var(--font-body);
            font-size: 14.5px;
            padding: 13px 20px 13px 44px;
            border-radius: 10px;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-input:focus {{
            border-color: var(--cyan);
            box-shadow: 0 0 0 3px rgba(0, 240, 255, 0.2);
        }}

        .search-icon {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--cyan);
            font-size: 16px;
        }}

        /* Findings Cards Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(640px, 1fr));
            gap: 20px;
        }}

        @media (max-width: 768px) {{
            .cards-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .finding-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 14px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            backdrop-filter: blur(10px);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }}

        .finding-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-bright);
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5);
        }}

        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .card-idx-pattern {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .card-idx {{
            font-family: var(--font-code);
            font-size: 13px;
            font-weight: 700;
            color: var(--text-dim);
        }}

        .card-pattern-title {{
            font-family: var(--font-code);
            font-size: 16px;
            font-weight: 800;
            color: var(--cyan);
        }}

        .category-badge {{
            font-family: var(--font-code);
            font-size: 11px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}

        .target-meta {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .target-code {{
            font-family: var(--font-code);
            font-size: 14.5px;
            font-weight: 700;
            color: #ffffff;
            background: rgba(4, 6, 12, 0.8);
            border: 1px solid var(--border-bright);
            padding: 4px 10px;
            border-radius: 6px;
            word-break: break-all;
        }}

        .kind-pill {{
            font-family: var(--font-code);
            font-size: 11.5px;
            color: var(--text-dim);
            background: rgba(24, 35, 56, 0.6);
            padding: 3px 8px;
            border-radius: 4px;
        }}

        .card-summary {{
            font-size: 14.5px;
            line-height: 1.6;
            color: var(--text-bright);
            font-weight: 500;
            margin-bottom: 16px;
        }}

        /* Evidence Box */
        .evidence-trail-title {{
            font-family: var(--font-code);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            color: var(--text-dim);
            margin-bottom: 6px;
        }}

        .evidence-item {{
            background: rgba(4, 6, 12, 0.7);
            border-left: 3px solid var(--cyan);
            padding: 8px 12px;
            border-radius: 0 6px 6px 0;
            font-size: 13px;
            line-height: 1.5;
            color: #cbd5e1;
            margin-bottom: 6px;
            border-top: 1px solid rgba(24, 35, 56, 0.4);
            border-right: 1px solid rgba(24, 35, 56, 0.4);
            border-bottom: 1px solid rgba(24, 35, 56, 0.4);
        }}

        .card-footer {{
            border-top: 1px solid var(--border-dim);
            padding-top: 14px;
            margin-top: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}

        .loc-pill {{
            font-family: var(--font-code);
            font-size: 12px;
            color: var(--rose);
            background: rgba(255, 42, 109, 0.08);
            border: 1px solid rgba(255, 42, 109, 0.25);
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            max-width: 68%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .conf-badge {{
            font-family: var(--font-code);
            font-size: 11.5px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            flex-shrink: 0;
            white-space: nowrap;
        }}

        .conf-very-high {{ background: rgba(0, 255, 157, 0.15); color: var(--emerald); border: 1px solid rgba(0, 255, 157, 0.4); }}
        .conf-high {{ background: rgba(0, 240, 255, 0.15); color: var(--cyan); border: 1px solid rgba(0, 240, 255, 0.4); }}
        .conf-medium {{ background: rgba(255, 183, 0, 0.15); color: var(--amber); border: 1px solid rgba(255, 183, 0, 0.4); }}

        #copyToast {{
            display: none;
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--bg-surface-elevated);
            border: 1px solid var(--emerald);
            color: var(--emerald);
            padding: 14px 20px;
            border-radius: 10px;
            font-family: var(--font-code);
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px var(--emerald-glow);
            z-index: 9999;
            animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slideIn {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
    </style>
</head>
<body>

<div class="hud-container">

    <!-- Header Section -->
    <header class="hud-header">
        <div class="header-flex">
            <div class="header-brand">
                <div class="monad-logo-badge">λ</div>
                <div>
                    <h1 class="hud-title">DPX-Haskell Architecture HUD</h1>
                    <div class="target-tag">
                        Target Codebase: <span class="code-pill">{project_name}</span>
                    </div>
                </div>
            </div>
            <div class="meta-pills">
                <span class="meta-pill" style="border-color: var(--cyan); color: var(--cyan);">
                    ⚡ Hexagonal DDD Engine
                </span>
                <span class="meta-pill" style="border-color: var(--emerald); color: var(--emerald);">
                    ⏱️ {elapsed_seconds}s
                </span>
                <span class="meta-pill" style="border-color: var(--purple); color: var(--purple);">
                    📁 {scanned_files} files
                </span>
            </div>
        </div>
    </header>

    <!-- Holographic KPI Cards -->
    <section class="kpi-grid">
        <div class="kpi-card cyan">
            <div class="kpi-label">Total Findings</div>
            <div class="kpi-value" style="color: var(--cyan);">{total_detections}</div>
            <div class="kpi-desc">Architecture patterns & smells mapped</div>
        </div>
        <div class="kpi-card rose">
            <div class="kpi-label">Action Required</div>
            <div class="kpi-value" style="color: var(--rose);">{total_violations}</div>
            <div class="kpi-desc">Safety hazards, space leaks & anti-patterns</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">Typeclasses & Monads</div>
            <div class="kpi-value" style="color: var(--purple);">{total_typeclasses_and_monads}</div>
            <div class="kpi-desc">Typeclasses, ReaderT & Transformer stacks</div>
        </div>
        <div class="kpi-card emerald">
            <div class="kpi-label">Clean Code & STM</div>
            <div class="kpi-value" style="color: var(--emerald);">{total_adherences}</div>
            <div class="kpi-desc">Clean functional idioms & STM transactions</div>
        </div>
    </section>

    <!-- AI Architecture Prompt HUD Banner -->
    <section class="ai-banner">
        <div>
            <h2 class="ai-title">🤖 AI / LLM Architectural Prompt Context</h2>
            <p style="color: var(--text-secondary); margin-top: 4px; font-size: 14px;">
                Instant token-optimized prompt for Claude, ChatGPT or Gemini to perform architectural review, ReaderT refactoring and space leak elimination.
            </p>
        </div>
        <button class="ai-btn" id="copyLlmBtn" onclick="copyLlmContext()">
            📋 Copy Context for LLM
        </button>
        <textarea id="llmContextData" style="display: none;">{llm_context_data}</textarea>
    </section>

    <!-- Controls & Search Bar -->
    <section class="controls-bar">
        <div class="category-pills" id="categoryPillBar">
            <button class="cat-pill-btn active" data-filter="all">All Findings ({total_detections})</button>
            {category_filter_buttons}
        </div>
        <div class="search-box-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="Instant filter by pattern name, module, function, or rule (e.g. ReaderT, STM, GADT, kiss)...">
        </div>
    </section>

    <!-- Findings Grid -->
    <main class="cards-grid" id="findingsGrid">
        {findings_cards_html}
    </main>

</div>

<div id="copyToast">✓ Architectural Prompt Copied to Clipboard!</div>

<script>
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.finding-card');
    const filterBtns = document.querySelectorAll('.cat-pill-btn');

    let activeCategory = 'all';

    function filterFindings() {{
        const q = searchInput.value.toLowerCase().trim();

        cards.forEach(card => {{
            const cat = card.dataset.category || '';
            const txt = card.textContent.toLowerCase();

            const matchCat = (activeCategory === 'all' || cat === activeCategory);
            const matchQuery = (!q || txt.includes(q));

            if (matchCat && matchQuery) {{
                card.style.display = 'flex';
            }} else {{
                card.style.display = 'none';
            }}
        }});
    }}

    searchInput.addEventListener('input', filterFindings);

    filterBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeCategory = btn.dataset.filter;
            filterFindings();
        }});
    }});

    function copyLlmContext() {{
        const raw = document.getElementById('llmContextData').value;
        const btn = document.getElementById('copyLlmBtn');
        const toast = document.getElementById('copyToast');

        navigator.clipboard.writeText(raw).then(() => {{
            btn.innerHTML = '✓ Copied!';
            toast.style.display = 'block';
            setTimeout(() => {{
                btn.innerHTML = '📋 Copy Context for LLM';
                toast.style.display = 'none';
            }}, 2400);
        }}).catch(() => {{
            const ta = document.createElement('textarea');
            ta.value = raw;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            btn.innerHTML = '✓ Copied!';
            toast.style.display = 'block';
            setTimeout(() => {{
                btn.innerHTML = '📋 Copy Context for LLM';
                toast.style.display = 'none';
            }}, 2400);
        }});
    }}
</script>

</body>
</html>
"""


class HtmlReportFormatter(ReportFormatterPort):
    """Generates an elite Cyber-Architectural HUD HTML dashboard for Haskell."""

    def format(self, report: DetectionReport) -> str:
        project_name = self._resolve_project_name(report.project_path)

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
        for cat, theme in CATEGORY_THEMES.items():
            cnt = report.summary_by_category.get(cat.value, 0)
            if cnt > 0:
                filter_buttons.append(
                    f'<button class="cat-pill-btn" data-filter="{cat.value}">{theme["icon"]} {theme["name"]} ({cnt})</button>'
                )

        cards_html = []
        for idx, d in enumerate(report.detections, 1):
            theme = CATEGORY_THEMES.get(d.pattern_category, CATEGORY_THEMES[PatternCategory.FUNCTIONAL_IDIOM])
            conf_class = (
                "conf-very-high"
                if d.level == ConfidenceLevel.VERY_HIGH
                else "conf-high"
                if d.level == ConfidenceLevel.HIGH
                else "conf-medium"
            )
            raw_loc = str(d.primary_location) if d.primary_location else "N/A"
            disp_loc, full_loc = self._format_display_location(raw_loc, report.project_path)

            evidences_html = "".join([
                f'<div class="evidence-item" style="border-left-color: {theme["accent"]};">'
                f'<strong style="color: {theme["text"]}; font-family: var(--font-code);">+{int(ev.weight * 100)}% [{html.escape(ev.rule_code)}]</strong> '
                f'{html.escape(ev.description)}'
                f'</div>'
                for ev in d.evidences
            ])

            cards_html.append(
                f"""
                <article class="finding-card" data-category="{d.pattern_category.value}" style="border-left: 4px solid {theme['accent']};">
                    <div>
                        <div class="card-top">
                            <div class="card-idx-pattern">
                                <span class="card-idx">#{idx}</span>
                                <span class="card-pattern-title">{html.escape(d.pattern_type.value)}</span>
                            </div>
                            <span class="category-badge" style="background: {theme['badge_bg']}; color: {theme['text']}; border: 1px solid {theme['border']};">
                                {theme['icon']} {theme['name']}
                            </span>
                        </div>
                        <div class="target-meta">
                            <span>Target:</span>
                            <code class="target-code">{html.escape(d.target_name)}</code>
                            <span class="kind-pill">{html.escape(d.target_kind)}</span>
                        </div>
                        <p class="card-summary">{html.escape(d.summary)}</p>
                        <div>
                            <div class="evidence-trail-title">🔎 Evidence Trail ({len(d.evidences)} heuristics):</div>
                            {evidences_html}
                        </div>
                    </div>
                    <footer class="card-footer">
                        <span class="loc-pill" title="{html.escape(full_loc)}">📍 {html.escape(disp_loc)}</span>
                        <span class="conf-badge {conf_class}">{d.confidence.percentage_str} [{d.level.value.upper()}]</span>
                    </footer>
                </article>
                """
            )

        llm_context = self._generate_llm_prompt(report, project_name)

        return _HTML_TEMPLATE.format(
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
        if not loc_str or loc_str == "N/A":
            return "N/A", ""

        full_loc = loc_str
        clean_proj = project_path.rstrip("/\\")
        if clean_proj and loc_str.startswith(clean_proj):
            rel = loc_str[len(clean_proj):].lstrip("/\\")
            return rel, full_loc

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
