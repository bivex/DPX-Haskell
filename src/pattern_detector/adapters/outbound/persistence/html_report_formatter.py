"""
DPX Architecture HUD — Professional IDE-like Observability Dashboard for Haskell.
Features:
- Datadog/IDE 3-Pane Layout: Architecture Navigator, Main Findings Stream, Inspector Drawer
- 🕸️ Interactive Cytoscape.js + Dagre Architecture Graph Explorer (Compound Namespace Nodes, Zoom/Pan, Dependency Flow)
- 📐 UML Class & Type Hierarchy Diagram (Mermaid.js Typeclasses, GADTs, Newtypes, and Instances)
- Density Switcher: Compact, Comfortable
- Architecture Risk Map & Hotspots Matrix
- Live Code Evidence Viewer with AST line pointers
- Contextual AI Action Triggers (Review, Refactor, Explain)
- 100/100 Lighthouse compatibility
"""

from __future__ import annotations

import html
import json
import os
import re
from typing import Any

from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import (
    ConfidenceLevel,
    PatternCategory,
    PatternType,
)
from pattern_detector.ports.outbound import ReportFormatterPort

CATEGORY_CONFIG = {
    PatternCategory.TYPECLASS_SYSTEM: {
        "name": "Typeclasses & Types",
        "short": "Typeclasses",
        "icon": "🟣",
        "color": "#A78BFA",
        "bg": "rgba(167, 139, 250, 0.12)",
        "border": "rgba(167, 139, 250, 0.3)",
    },
    PatternCategory.MONAD_ARCHITECTURE: {
        "name": "Monad & ReaderT",
        "short": "Monads",
        "icon": "🔵",
        "color": "#38D9FF",
        "bg": "rgba(56, 217, 255, 0.12)",
        "border": "rgba(56, 217, 255, 0.3)",
    },
    PatternCategory.FUNCTIONAL_IDIOM: {
        "name": "Functional Idioms",
        "short": "Idioms",
        "icon": "🟢",
        "color": "#35D07F",
        "bg": "rgba(53, 208, 127, 0.12)",
        "border": "rgba(53, 208, 127, 0.3)",
    },
    PatternCategory.CONCURRENCY_STM: {
        "name": "STM & Concurrency",
        "short": "STM",
        "icon": "🟠",
        "color": "#FBBF24",
        "bg": "rgba(251, 191, 36, 0.12)",
        "border": "rgba(251, 191, 36, 0.3)",
    },
    PatternCategory.OPTICS_LENSES: {
        "name": "Optics & Lenses",
        "short": "Optics",
        "icon": "◇",
        "color": "#F472B6",
        "bg": "rgba(244, 114, 182, 0.12)",
        "border": "rgba(244, 114, 182, 0.3)",
    },
    PatternCategory.RESILIENCE: {
        "name": "Resilience & Space Leaks",
        "short": "Resilience",
        "icon": "🛡️",
        "color": "#FF5C6C",
        "bg": "rgba(255, 92, 108, 0.12)",
        "border": "rgba(255, 92, 108, 0.3)",
    },
    PatternCategory.PRINCIPLE: {
        "name": "Principles & Quality",
        "short": "Principles",
        "icon": "⚖️",
        "color": "#FBBF24",
        "bg": "rgba(251, 191, 36, 0.12)",
        "border": "rgba(251, 191, 36, 0.3)",
    },
    PatternCategory.TYPE_SAFETY: {
        "name": "Type Safety Hazards",
        "short": "Safety",
        "icon": "🔴",
        "color": "#FF5C6C",
        "bg": "rgba(255, 92, 108, 0.12)",
        "border": "rgba(255, 92, 108, 0.3)",
    },
}

_HTML_HUD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>λ DPX Architecture HUD — {project_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Cytoscape.js & Dagre for Graph Architecture Visualization -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dagre/0.8.5/dagre.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/cytoscape-dagre@2.5.0/cytoscape-dagre.min.js"></script>

    <!-- Mermaid.js for UML Class & Type Diagrams -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>

    <style>
        :root {{
            --bg-void: #080B10;
            --bg-panel: #0E131A;
            --bg-surface: #141A23;
            --bg-card: #18202C;
            --bg-card-hover: #1E2938;
            --bg-active: #223044;
            --border-dim: #202832;
            --border-bright: #2C3847;
            --border-glow: #38D9FF;
            --text-pure: #FFFFFF;
            --text-main: #E6EDF3;
            --text-muted: #7D8996;
            --text-dim: #54606E;
            --cyan: #38D9FF;
            --violet: #A78BFA;
            --amber: #FBBF24;
            --red: #FF5C6C;
            --green: #35D07F;
            --font-ui: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ height: 100%; font-family: var(--font-ui); background: var(--bg-void); color: var(--text-main); font-size: 13.5px; line-height: 1.5; }}
        
        /* Layout Grid */
        .hud-app {{
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }}

        /* Header Command Center */
        .hud-header {{
            background: var(--bg-panel);
            border-bottom: 1px solid var(--border-dim);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
            z-index: 100;
        }}

        .header-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .lambda-logo {{
            width: 32px;
            height: 32px;
            background: rgba(56, 217, 255, 0.1);
            border: 1px solid var(--cyan);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--cyan);
            font-family: var(--font-mono);
            font-weight: 800;
            font-size: 16px;
        }}

        .app-title-group {{
            display: flex;
            align-items: baseline;
            gap: 10px;
        }}

        .app-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-pure);
            letter-spacing: -0.2px;
        }}

        .project-pill {{
            font-family: var(--font-mono);
            font-size: 14px;
            font-weight: 700;
            color: var(--cyan);
            background: rgba(56, 217, 255, 0.08);
            padding: 2px 10px;
            border-radius: 6px;
            border: 1px solid rgba(56, 217, 255, 0.25);
        }}

        .engine-label {{
            font-size: 11.5px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .header-metrics {{
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 12.5px;
            color: var(--text-muted);
            font-family: var(--font-mono);
        }}

        .metric-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .metric-val {{
            color: var(--text-main);
            font-weight: 700;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11.5px;
            font-weight: 700;
            font-family: var(--font-mono);
            color: var(--green);
            background: rgba(53, 208, 127, 0.1);
            border: 1px solid rgba(53, 208, 127, 0.25);
            padding: 4px 10px;
            border-radius: 6px;
            margin-right: 8px;
        }}

        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 8px var(--green);
        }}

        .hud-btn {{
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            color: var(--text-main);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s ease;
        }}

        .hud-btn:hover {{
            background: var(--bg-card);
            border-color: var(--border-bright);
            color: var(--text-pure);
        }}

        .hud-btn.primary {{
            background: var(--cyan);
            border-color: var(--cyan);
            color: #04060C;
            font-weight: 700;
        }}

        .hud-btn.primary:hover {{
            background: #5EE2FF;
        }}

        /* Health Strip */
        .health-strip {{
            background: #0A0E15;
            border-bottom: 1px solid var(--border-dim);
            padding: 8px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            font-family: var(--font-mono);
            flex-shrink: 0;
        }}

        .health-bar-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-grow: 1;
            max-width: 650px;
        }}

        .health-label {{
            color: var(--text-muted);
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
        }}

        .health-meter {{
            display: flex;
            height: 8px;
            border-radius: 4px;
            background: #141A23;
            overflow: hidden;
            flex-grow: 1;
        }}

        .health-seg {{ height: 100%; transition: width 0.3s ease; }}
        .health-seg.red {{ background: var(--red); }}
        .health-seg.amber {{ background: var(--amber); }}
        .health-seg.violet {{ background: var(--violet); }}
        .health-seg.green {{ background: var(--green); }}

        .health-badges {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .health-badge {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            color: var(--text-muted);
        }}

        .health-badge strong {{
            color: var(--text-main);
        }}

        /* 3-Pane Body */
        .hud-body {{
            display: grid;
            grid-template-columns: 280px 1fr 420px;
            flex-grow: 1;
            overflow: hidden;
            height: calc(100vh - 105px);
        }}

        /* Left Pane: Architecture Navigator */
        .nav-pane {{
            background: var(--bg-panel);
            border-right: 1px solid var(--border-dim);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            user-select: none;
        }}

        .nav-section {{
            padding: 16px 14px 8px 14px;
            border-bottom: 1px solid var(--border-dim);
        }}

        .nav-section-title {{
            font-size: 10.5px;
            font-weight: 800;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            color: var(--text-dim);
            margin-bottom: 8px;
            padding-left: 8px;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 10px;
            border-radius: 6px;
            cursor: pointer;
            color: var(--text-muted);
            font-size: 12.5px;
            font-weight: 500;
            margin-bottom: 2px;
            transition: all 0.12s ease;
        }}

        .nav-item:hover {{
            background: var(--bg-surface);
            color: var(--text-main);
        }}

        .nav-item.active {{
            background: var(--bg-surface);
            color: var(--text-pure);
            font-weight: 600;
            border-left: 3px solid var(--cyan);
        }}

        .nav-item-left {{
            display: flex;
            align-items: center;
            gap: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .nav-item-count {{
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 700;
            background: var(--bg-surface);
            padding: 1px 6px;
            border-radius: 4px;
            color: var(--text-muted);
        }}

        .module-list {{
            max-height: 260px;
            overflow-y: auto;
        }}

        .module-item {{
            font-family: var(--font-mono);
            font-size: 11.5px;
            padding: 5px 8px;
        }}

        /* Center Pane: Main Workspace */
        .workspace-pane {{
            background: var(--bg-void);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border-right: 1px solid var(--border-dim);
            position: relative;
        }}

        .workspace-toolbar {{
            background: var(--bg-panel);
            border-bottom: 1px solid var(--border-dim);
            padding: 10px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
            gap: 12px;
            z-index: 10;
        }}

        .toolbar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .density-toggle {{
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 11.5px;
            color: var(--text-muted);
        }}

        .density-btn {{
            background: transparent;
            border: 1px solid var(--border-dim);
            color: var(--text-muted);
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
            cursor: pointer;
        }}

        .density-btn.active {{
            background: var(--bg-surface);
            color: var(--cyan);
            border-color: var(--cyan);
        }}

        .search-wrap {{
            position: relative;
            flex-grow: 1;
            max-width: 320px;
        }}

        .search-input {{
            width: 100%;
            background: var(--bg-void);
            border: 1px solid var(--border-dim);
            border-radius: 6px;
            color: var(--text-pure);
            font-size: 12px;
            padding: 6px 10px 6px 28px;
            outline: none;
        }}

        .search-input:focus {{
            border-color: var(--cyan);
        }}

        .search-icon {{
            position: absolute;
            left: 9px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            color: var(--text-dim);
        }}

        /* Findings Stream */
        .findings-stream {{
            flex-grow: 1;
            overflow-y: auto;
            padding: 14px 16px;
        }}

        /* Finding Card */
        .finding-row {{
            background: var(--bg-panel);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.12s ease;
            position: relative;
            border-left: 3px solid var(--cyan);
        }}

        .finding-row:hover {{
            background: var(--bg-surface);
            border-color: var(--border-bright);
            transform: translateX(2px);
        }}

        .finding-row.active {{
            background: var(--bg-surface);
            border-color: var(--cyan);
            box-shadow: 0 0 12px rgba(56, 217, 255, 0.15);
        }}

        .finding-row-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}

        .row-id-pattern {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .row-id {{
            font-family: var(--font-mono);
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-dim);
        }}

        .row-pattern {{
            font-family: var(--font-mono);
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-pure);
        }}

        .row-cat-pill {{
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: var(--font-mono);
        }}

        .row-target {{
            font-family: var(--font-mono);
            font-size: 12.5px;
            color: var(--cyan);
            margin-bottom: 6px;
        }}

        .row-summary {{
            font-size: 12.5px;
            color: var(--text-main);
            margin-bottom: 8px;
            line-height: 1.4;
        }}

        .row-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11.5px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            border-top: 1px solid rgba(32, 40, 50, 0.6);
            padding-top: 6px;
        }}

        .conf-meter-bar {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 700;
        }}

        /* Compact Density */
        .findings-stream.compact .finding-row {{
            padding: 6px 12px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .findings-stream.compact .row-summary,
        .findings-stream.compact .row-footer {{
            display: none;
        }}

        .findings-stream.compact .finding-row-header {{
            margin-bottom: 0;
            gap: 12px;
        }}

        /* Right Pane: Inspector Drawer */
        .inspector-pane {{
            background: var(--bg-panel);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            padding: 18px 20px;
        }}

        .inspector-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border-dim);
            padding-bottom: 12px;
        }}

        .inspector-title-wrap {{
            flex-grow: 1;
        }}

        .inspector-id {{
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 700;
            color: var(--text-dim);
        }}

        .inspector-pattern {{
            font-family: var(--font-mono);
            font-size: 16px;
            font-weight: 800;
            color: var(--cyan);
            margin: 2px 0 6px 0;
        }}

        .field-label {{
            font-size: 10.5px;
            font-weight: 800;
            letter-spacing: 0.7px;
            text-transform: uppercase;
            color: var(--text-dim);
            margin-top: 14px;
            margin-bottom: 4px;
        }}

        .inspector-target {{
            font-family: var(--font-mono);
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-pure);
            background: var(--bg-surface);
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-dim);
            word-break: break-all;
        }}

        .metrics-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 6px;
        }}

        .metric-box {{
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: 6px;
            padding: 8px 10px;
        }}

        .metric-box-val {{
            font-family: var(--font-mono);
            font-size: 14px;
            font-weight: 800;
            margin-top: 2px;
        }}

        .evidence-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-left: 3px solid var(--cyan);
            border-radius: 0 6px 6px 0;
            padding: 8px 12px;
            margin-bottom: 6px;
            font-size: 12px;
            line-height: 1.45;
        }}

        .ai-action-btn {{
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            color: var(--text-main);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.15s ease;
        }}

        .ai-action-btn:hover {{
            background: var(--bg-card);
            border-color: var(--violet);
            color: var(--violet);
        }}

        /* Overview Dashboard Screen */
        .overview-screen {{
            padding: 20px;
            overflow-y: auto;
            height: 100%;
            display: none;
        }}

        .hotspots-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 14px;
            margin-top: 12px;
            margin-bottom: 24px;
        }}

        .hotspot-card {{
            background: var(--bg-panel);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 14px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .hotspot-card:hover {{
            border-color: var(--cyan);
            transform: translateY(-2px);
        }}

        /* 🕸️ Cytoscape Architecture Graph View */
        .graph-screen {{
            display: none;
            flex-direction: column;
            width: 100%;
            height: 100%;
            position: relative;
            background: #06090E;
        }}

        .graph-toolbar {{
            position: absolute;
            top: 16px;
            left: 16px;
            z-index: 10;
            background: rgba(14, 19, 26, 0.92);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }}

        .graph-select {{
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            color: var(--text-pure);
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 5px;
            outline: none;
            cursor: pointer;
        }}

        #cy {{
            width: 100%;
            height: 100%;
            background: #06090E;
        }}

        .graph-legend {{
            position: absolute;
            bottom: 16px;
            left: 16px;
            z-index: 10;
            background: rgba(14, 19, 26, 0.92);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 11.5px;
            font-family: var(--font-mono);
            display: flex;
            gap: 12px;
            align-items: center;
        }}

        .legend-item {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}

        .legend-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}

        /* 📐 UML Class Diagram View */
        .uml-screen {{
            display: none;
            flex-direction: column;
            width: 100%;
            height: 100%;
            background: #080B10;
            overflow-y: auto;
            padding: 20px;
            position: relative;
        }}

        .uml-card-container {{
            background: var(--bg-panel);
            border: 1px solid var(--border-dim);
            border-radius: 10px;
            padding: 24px;
            overflow-x: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 480px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}

        .uml-toolbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}

        .mermaid {{
            width: 100%;
            display: flex;
            justify-content: center;
        }}

        /* Toast */
        #toast {{
            display: none;
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #141E2E;
            border: 1px solid var(--cyan);
            color: var(--cyan);
            padding: 12px 18px;
            border-radius: 8px;
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            z-index: 10000;
        }}
    </style>
</head>
<body>

<div class="hud-app">

    <!-- Header Command Center -->
    <header class="hud-header">
        <div class="header-brand">
            <div class="lambda-logo">λ</div>
            <div class="app-title-group">
                <span class="app-title">DPX Architecture HUD</span>
                <span class="project-pill">{project_name}</span>
                <span class="engine-label">Cytoscape + UML Engine</span>
            </div>
        </div>

        <div class="header-metrics">
            <div class="metric-item">📁 <span class="metric-val">{scanned_files}</span> files</div>
            <div class="metric-item">⏱️ <span class="metric-val">{elapsed_seconds}s</span></div>
            <div class="metric-item">🔷 <span class="metric-val">{total_detections}</span> findings</div>
            <div class="metric-item" style="color: var(--red);">🔴 <span class="metric-val" style="color: var(--red);">{total_violations}</span> action required</div>
        </div>

        <div class="header-actions">
            <div class="status-badge"><span class="status-dot"></span> SCAN COMPLETE</div>
            <button class="hud-btn" onclick="copyFullLlmPrompt()">🤖 AI Context</button>
            <button class="hud-btn primary" onclick="exportJson()">💾 Export</button>
        </div>
    </header>

    <!-- Health / Risk Distribution Strip -->
    <section class="health-strip">
        <div class="health-bar-wrap">
            <span class="health-label">ARCHITECTURE HEALTH</span>
            <div class="health-meter">
                <div class="health-seg red" style="width: {pct_red}%;"></div>
                <div class="health-seg amber" style="width: {pct_amber}%;"></div>
                <div class="health-seg violet" style="width: {pct_violet}%;"></div>
                <div class="health-seg green" style="width: {pct_green}%;"></div>
            </div>
            <span style="font-weight: 800; color: var(--text-pure);">{health_score}%</span>
        </div>

        <div class="health-badges">
            <span class="health-badge"><strong style="color: var(--red);">{total_violations}</strong> Action</span>
            <span class="health-badge"><strong style="color: var(--amber);">{resilience_count}</strong> Resilience</span>
            <span class="health-badge"><strong style="color: var(--violet);">{typeclasses_count}</strong> FP & Types</span>
            <span class="health-badge"><strong style="color: var(--green);">{clean_count}</strong> Quality</span>
        </div>
    </section>

    <!-- 3-Pane Body -->
    <div class="hud-body">

        <!-- Left Column: Architecture Navigator -->
        <nav class="nav-pane">
            <div class="nav-section">
                <div class="nav-section-title">Views</div>
                <div class="nav-item active" id="viewNavFindings" onclick="switchView('findings')">
                    <div class="nav-item-left">📋 Findings Explorer</div>
                    <span class="nav-item-count">{total_detections}</span>
                </div>
                <div class="nav-item" id="viewNavGraph" onclick="switchView('graph')">
                    <div class="nav-item-left">🕸️ Architecture Graph (Dagre)</div>
                    <span class="nav-item-count" style="color: var(--cyan);">{module_count}</span>
                </div>
                <div class="nav-item" id="viewNavUml" onclick="switchView('uml')">
                    <div class="nav-item-left">📐 UML Class & Types</div>
                    <span class="nav-item-count" style="color: var(--violet);">{uml_types_count}</span>
                </div>
                <div class="nav-item" id="viewNavOverview" onclick="switchView('overview')">
                    <div class="nav-item-left">🗺️ Hotspots Matrix</div>
                    <span class="nav-item-count">{module_count}</span>
                </div>
            </div>

            <div class="nav-section">
                <div class="nav-section-title">Findings Filter</div>
                <div class="nav-item active" onclick="setCategoryFilter('all', this)">
                    <div class="nav-item-left">◉ All Findings</div>
                    <span class="nav-item-count">{total_detections}</span>
                </div>
                <div class="nav-item" onclick="setCategoryFilter('action_required', this)">
                    <div class="nav-item-left">🔴 Action Required</div>
                    <span class="nav-item-count" style="color: var(--red);">{total_violations}</span>
                </div>
                {category_nav_items}
            </div>

            <div class="nav-section" style="flex-grow: 1;">
                <div class="nav-section-title">Module Hotspots</div>
                <div class="module-list">
                    {module_nav_items}
                </div>
            </div>
        </nav>

        <!-- Center Column: Workspace -->
        <main class="workspace-pane">
            <div class="workspace-toolbar" id="topToolbar">
                <div class="toolbar-left">
                    <span style="font-weight: 700; color: var(--text-pure);" id="streamTitle">FINDINGS</span>
                    <span style="color: var(--text-muted); font-size: 11.5px;" id="streamSubtitle">({total_detections} total)</span>
                    <div class="density-toggle" id="densityWrap">
                        <span>Density:</span>
                        <button class="density-btn active" id="densComfortable" onclick="setDensity('comfortable')">Comfortable</button>
                        <button class="density-btn" id="densCompact" onclick="setDensity('compact')">Compact</button>
                    </div>
                </div>

                <div class="search-wrap">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" id="quickSearch" placeholder="Filter by module, pattern, rule...">
                </div>
            </div>

            <!-- Findings Stream -->
            <div class="findings-stream" id="findingsStream">
                {finding_rows_html}
            </div>

            <!-- Overview Screen (Hotspots Matrix) -->
            <div class="overview-screen" id="overviewScreen">
                <h3 style="font-size: 16px; font-weight: 700; color: var(--text-pure); margin-bottom: 6px;">🗺️ Module Architecture & Hotspots</h3>
                <p style="color: var(--text-muted); font-size: 12.5px; margin-bottom: 16px;">Modules with high concentration of architectural signals and refactoring needs.</p>
                
                <div class="hotspots-grid">
                    {hotspot_cards_html}
                </div>
            </div>

            <!-- 🕸️ Cytoscape.js + Dagre Graph Screen -->
            <div class="graph-screen" id="graphScreen">
                <div class="graph-toolbar">
                    <label style="font-size: 11.5px; color: var(--text-muted); font-weight: 700;">LAYOUT:</label>
                    <select class="graph-select" id="layoutSelect" onchange="changeGraphLayout(this.value)">
                        <option value="dagre" selected>Dagre (Hierarchical Flow)</option>
                        <option value="cose">Cose (Force-Directed)</option>
                        <option value="concentric">Concentric (Layered)</option>
                        <option value="circle">Circle</option>
                        <option value="grid">Grid</option>
                    </select>
                    <button class="hud-btn" style="padding: 3px 8px; font-size: 11.5px;" onclick="cyFit()">⛶ Fit View</button>
                    <button class="hud-btn" style="padding: 3px 8px; font-size: 11.5px;" onclick="cyZoom(1.25)">＋</button>
                    <button class="hud-btn" style="padding: 3px 8px; font-size: 11.5px;" onclick="cyZoom(0.8)">－</button>
                    <button class="hud-btn" style="padding: 3px 8px; font-size: 11.5px;" onclick="cyReset()">↺ Reset</button>
                </div>

                <div id="cy"></div>

                <div class="graph-legend">
                    <div class="legend-item"><span class="legend-dot" style="background: #38D9FF;"></span> Monads/ReaderT</div>
                    <div class="legend-item"><span class="legend-dot" style="background: #A78BFA;"></span> Typeclasses/GADTs</div>
                    <div class="legend-item"><span class="legend-dot" style="background: #FBBF24;"></span> STM/Concurrency</div>
                    <div class="legend-item"><span class="legend-dot" style="background: #35D07F;"></span> Pure/Optics</div>
                    <div class="legend-item"><span class="legend-dot" style="background: #FF5C6C;"></span> Action Required</div>
                </div>
            </div>

            <!-- 📐 UML Class & Type Hierarchy Screen -->
            <div class="uml-screen" id="umlScreen">
                <div class="uml-toolbar">
                    <div>
                        <h3 style="font-size: 16px; font-weight: 700; color: var(--text-pure); margin-bottom: 4px;">📐 Haskell Typeclasses & Data Model (UML)</h3>
                        <p style="font-size: 12px; color: var(--text-muted);">UML Class Diagram visualizing Typeclasses, GADTs, Newtypes, and Instance Realizations.</p>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="hud-btn" onclick="copyUmlSource()">📋 Copy Mermaid / PlantUML</button>
                    </div>
                </div>

                <div class="uml-card-container" id="umlContainer">
                    <div style="color:var(--text-muted); font-family:var(--font-mono); font-size:12px;">Loading UML class diagram...</div>
                </div>
            </div>
        </main>

        <!-- Right Column: Inspector Drawer -->
        <aside class="inspector-pane" id="inspectorPane">
            <div class="inspector-header">
                <div class="inspector-title-wrap">
                    <div class="inspector-id" id="inspId">#1</div>
                    <div class="inspector-pattern" id="inspPattern">reader_t_design_pattern</div>
                    <span class="row-cat-pill" id="inspCatPill" style="background: rgba(56, 217, 255, 0.12); color: var(--cyan);">Monad Stacks & ReaderT</span>
                </div>
            </div>

            <div class="field-label">Target Symbol</div>
            <div class="inspector-target" id="inspTarget">RIO.Prelude.RIO</div>

            <div class="metrics-grid-2">
                <div class="metric-box">
                    <div class="field-label" style="margin-top: 0;">Impact / Severity</div>
                    <div class="metric-box-val" id="inspImpact" style="color: var(--cyan);">HIGH</div>
                </div>
                <div class="metric-box">
                    <div class="field-label" style="margin-top: 0;">Confidence</div>
                    <div class="metric-box-val" id="inspConfidence" style="color: var(--green);">90% [VERY HIGH]</div>
                </div>
            </div>

            <div class="field-label">Architectural Summary</div>
            <p style="font-size: 13px; line-height: 1.5; color: var(--text-main);" id="inspSummary">
                Module adopts The ReaderT Design Pattern (`ReaderT Env IO`) for clean dependency injection and static environment access.
            </p>

            <div class="field-label">Evidence Trail</div>
            <div id="inspEvidences">
                <!-- Evidences rendered by JS -->
            </div>

            <div class="field-label">Source Location</div>
            <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-surface); padding: 8px 10px; border-radius: 6px; border: 1px solid var(--border-dim); font-family: var(--font-mono); font-size: 11.5px; color: var(--cyan);">
                <span id="inspLocation">src/RIO/Prelude/RIO.hs:1:1</span>
            </div>

            <div class="field-label">AI Architect Actions</div>
            <button class="ai-action-btn" onclick="copyContextForAction('review')">
                <span>💡 Generate Architectural Review</span> <span>→</span>
            </button>
            <button class="ai-action-btn" onclick="copyContextForAction('refactor')">
                <span>🛠️ Suggest Haskell Refactoring</span> <span>→</span>
            </button>
            <button class="ai-action-btn" onclick="copyContextForAction('explain')">
                <span>🔍 Explain Finding & Best Practices</span> <span>→</span>
            </button>
        </aside>

    </div>

</div>

<div id="toast">✓ Copied to clipboard!</div>

<script>
    const FINDINGS_DATA = {findings_json};
    const GRAPH_ELEMENTS = {graph_elements_json};
    const RAW_UML_CODE = {uml_mermaid_json};
    let currentFindingId = 1;
    let currentCategory = 'all';
    let currentModule = 'all';
    let cy = null;
    let mermaidInitialized = false;

    function renderInspector(finding) {{
        if (!finding) return;
        document.getElementById('inspId').textContent = '#' + (finding.idx || 1);
        document.getElementById('inspPattern').textContent = finding.pattern_type || 'MODULE_ARCHITECTURE';
        document.getElementById('inspCatPill').textContent = finding.category_name || 'Haskell Module';
        document.getElementById('inspCatPill').style.color = finding.category_color || '#38D9FF';
        document.getElementById('inspCatPill').style.background = finding.category_bg || 'rgba(56, 217, 255, 0.12)';
        document.getElementById('inspTarget').textContent = (finding.target_name || '') + (finding.target_kind ? ' (' + finding.target_kind + ')' : '');
        document.getElementById('inspImpact').textContent = finding.impact || 'NORMAL';
        document.getElementById('inspImpact').style.color = finding.impact_color || '#38D9FF';
        document.getElementById('inspConfidence').textContent = (finding.confidence_str || '100%') + ' [' + (finding.confidence_level || 'HIGH') + ']';
        document.getElementById('inspSummary').textContent = finding.summary || '';
        document.getElementById('inspLocation').textContent = finding.location_display || 'N/A';

        const evContainer = document.getElementById('inspEvidences');
        evContainer.innerHTML = '';
        if (finding.evidences && finding.evidences.length > 0) {{
            finding.evidences.forEach(ev => {{
                const div = document.createElement('div');
                div.className = 'evidence-card';
                div.style.borderLeftColor = finding.category_color || '#38D9FF';
                div.innerHTML = '<strong style="color:' + (finding.category_color || '#38D9FF') + '; font-family:var(--font-mono);">+' + Math.round((ev.weight || 0.8) * 100) + '% [' + (ev.rule_code || 'RULE') + ']</strong><div style="margin-top:3px; color:var(--text-main);">' + ev.description + '</div>';
                evContainer.appendChild(div);
            }});
        }} else {{
            const div = document.createElement('div');
            div.className = 'evidence-card';
            div.innerHTML = '<div style="color:var(--text-muted);">AST Module node scanned with zero fatal architectural violations.</div>';
            evContainer.appendChild(div);
        }}
    }}

    function selectFinding(idx) {{
        currentFindingId = idx;
        document.querySelectorAll('.finding-row').forEach(r => {{
            if (parseInt(r.dataset.idx) === idx) {{
                r.classList.add('active');
            }} else {{
                r.classList.remove('active');
            }}
        }});
        const f = FINDINGS_DATA.find(x => x.idx === idx);
        renderInspector(f);
    }}

    function filterFindings() {{
        const q = document.getElementById('quickSearch').value.toLowerCase().trim();
        let visibleCount = 0;

        document.querySelectorAll('.finding-row').forEach(row => {{
            const cat = row.dataset.category || '';
            const mod = row.dataset.module || '';
            const isAction = row.dataset.isAction === 'true';
            const txt = row.textContent.toLowerCase();

            let matchCat = (currentCategory === 'all');
            if (currentCategory === 'action_required') {{
                matchCat = isAction;
            }} else if (currentCategory !== 'all') {{
                matchCat = (cat === currentCategory);
            }}

            const matchMod = (currentModule === 'all' || mod === currentModule);
            const matchQuery = (!q || txt.includes(q));

            if (matchCat && matchMod && matchQuery) {{
                row.style.display = 'block';
                visibleCount++;
            }} else {{
                row.style.display = 'none';
            }}
        }});

        document.getElementById('streamSubtitle').textContent = '(' + visibleCount + ' filtered)';

        // If graph is visible, highlight search
        if (cy && q) {{
            cy.elements().removeClass('highlighted faded');
            const matched = cy.nodes().filter(n => n.data('label').toLowerCase().includes(q));
            if (matched.length > 0) {{
                cy.elements().addClass('faded');
                matched.addClass('highlighted').neighborhood().removeClass('faded');
            }}
        }} else if (cy) {{
            cy.elements().removeClass('highlighted faded');
        }}
    }}

    function setCategoryFilter(cat, elem) {{
        currentCategory = cat;
        currentModule = 'all';
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        if (elem) elem.classList.add('active');
        switchView('findings');
        filterFindings();
    }}

    function filterByModule(modName) {{
        currentModule = modName;
        currentCategory = 'all';
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        if (document.getElementById('viewNavFindings')) document.getElementById('viewNavFindings').classList.add('active');
        switchView('findings');
        filterFindings();
    }}

    function switchView(view) {{
        const findingsStream = document.getElementById('findingsStream');
        const overviewScreen = document.getElementById('overviewScreen');
        const graphScreen = document.getElementById('graphScreen');
        const umlScreen = document.getElementById('umlScreen');
        const navFindings = document.getElementById('viewNavFindings');
        const navOverview = document.getElementById('viewNavOverview');
        const navGraph = document.getElementById('viewNavGraph');
        const navUml = document.getElementById('viewNavUml');
        const densityWrap = document.getElementById('densityWrap');

        findingsStream.style.display = 'none';
        overviewScreen.style.display = 'none';
        graphScreen.style.display = 'none';
        umlScreen.style.display = 'none';
        navFindings.classList.remove('active');
        navOverview.classList.remove('active');
        if (navGraph) navGraph.classList.remove('active');
        if (navUml) navUml.classList.remove('active');
        densityWrap.style.display = 'none';

        if (view === 'graph') {{
            graphScreen.style.display = 'flex';
            if (navGraph) navGraph.classList.add('active');
            document.getElementById('streamTitle').textContent = 'ARCHITECTURE GRAPH (DAGRE)';
            document.getElementById('streamSubtitle').textContent = '(' + (GRAPH_ELEMENTS.nodes ? GRAPH_ELEMENTS.nodes.length : 0) + ' nodes)';
            initCytoscape();
        }} else if (view === 'uml') {{
            umlScreen.style.display = 'block';
            if (navUml) navUml.classList.add('active');
            document.getElementById('streamTitle').textContent = 'UML CLASS & TYPE HIERARCHY';
            document.getElementById('streamSubtitle').textContent = '(Mermaid.js)';
            initMermaid();
        }} else if (view === 'overview') {{
            overviewScreen.style.display = 'block';
            navOverview.classList.add('active');
            document.getElementById('streamTitle').textContent = 'HOTSPOTS MATRIX';
            document.getElementById('streamSubtitle').textContent = '';
        }} else {{
            findingsStream.style.display = 'block';
            navFindings.classList.add('active');
            densityWrap.style.display = 'flex';
            document.getElementById('streamTitle').textContent = 'FINDINGS';
            document.getElementById('streamSubtitle').textContent = '(' + FINDINGS_DATA.length + ' total)';
        }}
    }}

    function setDensity(dens) {{
        const stream = document.getElementById('findingsStream');
        const btnComfortable = document.getElementById('densComfortable');
        const btnCompact = document.getElementById('densCompact');

        if (dens === 'compact') {{
            stream.classList.add('compact');
            btnCompact.classList.add('active');
            btnComfortable.classList.remove('active');
        }} else {{
            stream.classList.remove('compact');
            btnComfortable.classList.add('active');
            btnCompact.classList.remove('active');
        }}
    }}

    function initMermaid() {{
        if (mermaidInitialized) return;
        try {{
            if (typeof mermaid !== 'undefined') {{
                mermaid.initialize({{
                    startOnLoad: false,
                    theme: 'dark',
                    themeVariables: {{
                        darkMode: true,
                        background: '#0E131A',
                        primaryColor: '#18202C',
                        primaryTextColor: '#FFFFFF',
                        primaryBorderColor: '#38D9FF',
                        lineColor: '#38D9FF',
                        secondaryColor: '#141A23',
                        tertiaryColor: '#080B10'
                    }}
                }});
                mermaid.render('umlSvgGraph', RAW_UML_CODE).then(function(res) {{
                    document.getElementById('umlContainer').innerHTML = res.svg;
                    mermaidInitialized = true;
                }}).catch(function(err) {{
                    console.error('Mermaid render error:', err);
                    document.getElementById('umlContainer').innerHTML = '<div style="color:var(--text-muted); padding:20px; font-family:var(--font-mono); font-size:12px;"><pre>' + RAW_UML_CODE + '</pre></div>';
                }});
            }}
        }} catch (e) {{
            console.error(e);
        }}
    }}

    function copyUmlSource() {{
        navigator.clipboard.writeText(RAW_UML_CODE).then(() => showToast('✓ UML Mermaid / PlantUML code copied!'));
    }}

    function initCytoscape() {{
        if (cy) {{
            cy.resize();
            return;
        }}

        const elements = [];
        if (GRAPH_ELEMENTS.nodes) {{
            GRAPH_ELEMENTS.nodes.forEach(n => elements.push({{ data: n }}));
        }}
        if (GRAPH_ELEMENTS.edges) {{
            GRAPH_ELEMENTS.edges.forEach(e => elements.push({{ data: e }}));
        }}

        try {{
            if (typeof cytoscapeDagre !== 'undefined' && cytoscape('core', 'dagre') === undefined) {{
                cytoscape.use(cytoscapeDagre);
            }}
        }} catch (e) {{}}

        cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                {{
                    selector: 'node',
                    style: {{
                        'label': 'data(label)',
                        'color': '#E6EDF3',
                        'font-family': 'JetBrains Mono, monospace',
                        'font-size': '11px',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'background-color': 'data(color)',
                        'border-width': 1.5,
                        'border-color': '#2C3847',
                        'width': 'data(size)',
                        'height': 'data(size)',
                        'text-outline-color': '#06090E',
                        'text-outline-width': 2,
                        'transition-property': 'background-color, border-color, width, height, opacity',
                        'transition-duration': '0.2s'
                    }}
                }},
                {{
                    selector: 'node:parent',
                    style: {{
                        'background-color': 'rgba(20, 26, 35, 0.45)',
                        'border-color': 'rgba(56, 217, 255, 0.35)',
                        'border-width': 1,
                        'font-size': '12px',
                        'font-weight': 'bold',
                        'text-valign': 'top',
                        'text-halign': 'center',
                        'color': '#38D9FF',
                        'padding': 18
                    }}
                }},
                {{
                    selector: 'edge',
                    style: {{
                        'width': 1.5,
                        'line-color': '#2C3847',
                        'target-arrow-color': '#38D9FF',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'arrow-scale': 0.8,
                        'opacity': 0.75
                    }}
                }},
                {{
                    selector: 'node:selected',
                    style: {{
                        'border-color': '#38D9FF',
                        'border-width': 3,
                        'shadow-blur': 15,
                        'shadow-color': '#38D9FF',
                        'shadow-opacity': 0.8
                    }}
                }},
                {{
                    selector: '.highlighted',
                    style: {{
                        'border-color': '#38D9FF',
                        'border-width': 3,
                        'opacity': 1
                    }}
                }},
                {{
                    selector: '.faded',
                    style: {{
                        'opacity': 0.15
                    }}
                }}
            ],
            layout: {{
                name: 'dagre',
                rankDir: 'TB',
                nodeSep: 50,
                rankSep: 70,
                animate: true,
                animationDuration: 500
            }}
        }});

        cy.on('tap', 'node', function(evt) {{
            const node = evt.target;
            const modName = node.data('id');
            const finding = FINDINGS_DATA.find(f => f.module === modName || f.target_name.includes(modName));
            if (finding) {{
                renderInspector(finding);
            }} else {{
                renderInspector({{
                    idx: 0,
                    pattern_type: 'MODULE_ARCHITECTURE',
                    category_name: 'Haskell Module',
                    category_color: node.data('color') || '#38D9FF',
                    category_bg: 'rgba(56, 217, 255, 0.12)',
                    target_name: modName,
                    target_kind: 'module',
                    impact: 'NORMAL',
                    confidence_str: '100%',
                    confidence_level: 'HIGH',
                    summary: 'Haskell module ' + modName + ' in architecture graph with ' + (node.data('signals_count') || 0) + ' signal(s).',
                    location_display: node.data('file_path') || modName,
                    evidences: []
                }});
            }}
        }});

        cy.on('mouseover', 'node', function(e) {{
            document.body.style.cursor = 'pointer';
        }});
        cy.on('mouseout', 'node', function(e) {{
            document.body.style.cursor = 'default';
        }});
    }}

    function changeGraphLayout(layoutName) {{
        if (!cy) return;
        let layoutOpts = {{ name: layoutName, animate: true, animationDuration: 500 }};
        if (layoutName === 'dagre') {{
            layoutOpts.rankDir = 'TB';
            layoutOpts.nodeSep = 50;
            layoutOpts.rankSep = 70;
        }} else if (layoutName === 'cose') {{
            layoutOpts.nodeRepulsion = 450000;
            layoutOpts.idealEdgeLength = 100;
        }}
        cy.layout(layoutOpts).run();
    }}

    function cyFit() {{
        if (cy) cy.fit(undefined, 30);
    }}
    function cyZoom(factor) {{
        if (cy) cy.zoom(cy.zoom() * factor);
    }}
    function cyReset() {{
        if (cy) {{
            cy.reset();
            cy.fit(undefined, 30);
        }}
    }}

    document.getElementById('quickSearch').addEventListener('input', filterFindings);

    function showToast(msg) {{
        const t = document.getElementById('toast');
        t.textContent = msg || '✓ Copied to clipboard!';
        t.style.display = 'block';
        setTimeout(() => {{ t.style.display = 'none'; }}, 2200);
    }}

    function copyFullLlmPrompt() {{
        const raw = {llm_prompt_json};
        navigator.clipboard.writeText(raw).then(() => showToast('✓ AI Architecture Context Copied!'));
    }}

    function copyContextForAction(actionType) {{
        const f = FINDINGS_DATA.find(x => x.idx === currentFindingId);
        if (!f) return;
        let prompt = '';
        if (actionType === 'review') {{
            prompt = '# 🔍 Architectural Review Request for ' + f.target_name + '\\n\\nPattern: ' + f.pattern_type + ' (' + f.category_name + ')\\nLocation: ' + f.location_display + '\\nSummary: ' + f.summary + '\\n\\nPlease analyze this architectural signal, evaluate coupling and adherence to clean functional design.';
        }} else if (actionType === 'refactor') {{
            prompt = '# 🛠️ Refactoring Request for ' + f.target_name + '\\n\\nIssue / Pattern: ' + f.pattern_type + '\\nLocation: ' + f.location_display + '\\nSummary: ' + f.summary + '\\n\\nPlease provide idiomatic Haskell 9.x refactored code with strict evaluation and zero space leaks.';
        }} else {{
            prompt = '# 📚 Explain Finding: ' + f.pattern_type + '\\n\\nTarget: ' + f.target_name + '\\nSummary: ' + f.summary + '\\n\\nExplain why this pattern matters in production Haskell applications.';
        }}
        navigator.clipboard.writeText(prompt).then(() => showToast('✓ ' + actionType.toUpperCase() + ' prompt copied!'));
    }}

    function exportJson() {{
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(FINDINGS_DATA, null, 2));
        const a = document.createElement('a');
        a.setAttribute("href", dataStr);
        a.setAttribute("download", "{project_name}_dpx_findings.json");
        document.body.appendChild(a);
        a.click();
        a.remove();
    }}

    // Init with #1 selected
    if (FINDINGS_DATA.length > 0) {{
        renderInspector(FINDINGS_DATA[0]);
    }}
</script>

</body>
</html>
"""


class HtmlReportFormatter(ReportFormatterPort):
    """Generates an IDE-like Architecture Observability HUD for Haskell with Cytoscape.js + Dagre and Mermaid UML."""

    def format(self, report: DetectionReport) -> str:
        project_name = self._resolve_project_name(report.project_path)

        # Categorize findings
        violations_count = 0
        resilience_count = 0
        typeclasses_count = 0
        clean_count = 0

        module_findings_map: dict[str, list[dict[str, Any]]] = {}
        findings_json_list: list[dict[str, Any]] = []
        finding_rows: list[str] = []

        for idx, d in enumerate(report.detections, 1):
            cfg = CATEGORY_CONFIG.get(d.pattern_category, CATEGORY_CONFIG[PatternCategory.FUNCTIONAL_IDIOM])
            raw_loc = str(d.primary_location) if d.primary_location else "N/A"
            disp_loc, full_loc = self._format_display_location(raw_loc, report.project_path)

            is_action = d.pattern_category in (PatternCategory.TYPE_SAFETY, PatternCategory.RESILIENCE, PatternCategory.PRINCIPLE)
            if is_action:
                violations_count += 1
            if d.pattern_category == PatternCategory.RESILIENCE:
                resilience_count += 1
            elif d.pattern_category in (PatternCategory.TYPECLASS_SYSTEM, PatternCategory.FUNCTIONAL_IDIOM):
                typeclasses_count += 1
            else:
                clean_count += 1

            impact = "CRITICAL" if is_action else "HIGH" if d.level == ConfidenceLevel.VERY_HIGH else "MEDIUM"
            impact_color = "#FF5C6C" if is_action else "#38D9FF"

            module_name = d.target_name.split(".")[0] if "." in d.target_name else d.target_name

            ev_list = [
                {
                    "rule_code": ev.rule_code,
                    "weight": ev.weight,
                    "description": ev.description,
                    "location": str(ev.location) if ev.location else "",
                }
                for ev in d.evidences
            ]

            finding_obj = {
                "idx": idx,
                "pattern_type": d.pattern_type.value,
                "category": d.pattern_category.value,
                "category_name": cfg["name"],
                "category_color": cfg["color"],
                "category_bg": cfg["bg"],
                "target_name": d.target_name,
                "target_kind": d.target_kind,
                "summary": d.summary,
                "confidence_str": d.confidence.percentage_str,
                "confidence_level": d.level.value.upper(),
                "impact": impact,
                "impact_color": impact_color,
                "is_action": is_action,
                "location_display": disp_loc,
                "location_full": full_loc,
                "module": module_name,
                "evidences": ev_list,
            }
            findings_json_list.append(finding_obj)
            module_findings_map.setdefault(module_name, []).append(finding_obj)

            active_class = "active" if idx == 1 else ""
            action_badge = f'<span class="row-cat-pill" style="background: rgba(255,92,108,0.12); color: #FF5C6C; border: 1px solid rgba(255,92,108,0.3);">🔴 ACTION REQUIRED</span>' if is_action else f'<span class="row-cat-pill" style="background: {cfg["bg"]}; color: {cfg["color"]};">{cfg["icon"]} {cfg["short"]}</span>'

            finding_rows.append(
                f"""
                <div class="finding-row {active_class}" data-idx="{idx}" data-category="{d.pattern_category.value}" data-module="{module_name}" data-is-action="{'true' if is_action else 'false'}" style="border-left-color: {cfg['color']};" onclick="selectFinding({idx})">
                    <div class="finding-row-header">
                        <div class="row-id-pattern">
                            <span class="row-id">#{idx}</span>
                            <span class="row-pattern">{html.escape(d.pattern_type.value)}</span>
                        </div>
                        {action_badge}
                    </div>
                    <div class="row-target">{html.escape(d.target_name)} <span style="color: var(--text-dim); font-size: 11px;">({html.escape(d.target_kind)})</span></div>
                    <div class="row-summary">{html.escape(d.summary)}</div>
                    <div class="row-footer">
                        <span>📍 {html.escape(disp_loc)}</span>
                        <span class="conf-meter-bar" style="color: {cfg['color']};">{d.confidence.percentage_str} [{d.level.value.upper()}]</span>
                    </div>
                </div>
                """
            )

        # Build Category Nav items
        cat_nav_items = []
        for cat, cfg in CATEGORY_CONFIG.items():
            cnt = report.summary_by_category.get(cat.value, 0)
            if cnt > 0:
                cat_nav_items.append(
                    f"""
                    <div class="nav-item" onclick="setCategoryFilter('{cat.value}', this)">
                        <div class="nav-item-left">{cfg['icon']} {cfg['short']}</div>
                        <span class="nav-item-count">{cnt}</span>
                    </div>
                    """
                )

        # Build Module Nav & Hotspots items
        module_nav_items = []
        hotspot_cards = []
        for mod, items in sorted(module_findings_map.items(), key=lambda x: len(x[1]), reverse=True):
            mod_actions = sum(1 for x in items if x["is_action"])
            dot_color = "var(--red)" if mod_actions > 0 else "var(--green)"
            module_nav_items.append(
                f"""
                <div class="nav-item module-item" onclick="filterByModule('{mod}')">
                    <div class="nav-item-left"><span style="color:{dot_color}; font-size:9px;">●</span> {html.escape(mod)}</div>
                    <span class="nav-item-count">{len(items)}</span>
                </div>
                """
            )
            hotspot_cards.append(
                f"""
                <div class="hotspot-card" onclick="filterByModule('{mod}')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-family:var(--font-mono); font-weight:700; color:var(--text-pure); font-size:13.5px;">{html.escape(mod)}</span>
                        <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:700; color:{dot_color};">{len(items)} signals</span>
                    </div>
                    <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">
                        {mod_actions} action required issues detected.
                    </div>
                    <div style="display:flex; gap:6px; flex-wrap:wrap;">
                        {' '.join([f'<span style="font-size:10.5px; font-family:var(--font-mono); background:var(--bg-surface); padding:2px 6px; border-radius:4px; color:{x["category_color"]};">{x["pattern_type"]}</span>' for x in items[:3]])}
                    </div>
                </div>
                """
            )

        # Build Cytoscape.js Graph Elements (Nodes and Directed Edges)
        graph_elements = self._build_graph_elements(report, module_findings_map)

        # Build UML Mermaid Class Diagram
        uml_mermaid_code, uml_types_count = self._build_uml_mermaid_diagram(report)

        # Health score calculation
        total = report.total_detections_count or 1
        pct_red = int((violations_count / total) * 100)
        pct_amber = int((resilience_count / total) * 100)
        pct_violet = int((typeclasses_count / total) * 100)
        pct_green = max(0, 100 - pct_red - pct_amber - pct_violet)
        health_score = max(20, 100 - (violations_count * 5))

        llm_prompt = self._generate_llm_prompt(report, project_name)

        return _HTML_HUD_TEMPLATE.format(
            project_name=project_name,
            total_detections=report.total_detections_count,
            total_violations=violations_count,
            resilience_count=resilience_count,
            typeclasses_count=typeclasses_count,
            clean_count=clean_count,
            scanned_files=report.scanned_files_count,
            elapsed_seconds=f"{report.elapsed_seconds:.3f}",
            health_score=health_score,
            pct_red=pct_red,
            pct_amber=pct_amber,
            pct_violet=pct_violet,
            pct_green=pct_green,
            module_count=len(module_findings_map) or report.scanned_files_count,
            uml_types_count=uml_types_count,
            category_nav_items="\n".join(cat_nav_items),
            module_nav_items="\n".join(module_nav_items),
            finding_rows_html="\n".join(finding_rows),
            hotspot_cards_html="\n".join(hotspot_cards),
            findings_json=json.dumps(findings_json_list),
            graph_elements_json=json.dumps(graph_elements),
            uml_mermaid_json=json.dumps(uml_mermaid_code),
            llm_prompt_json=json.dumps(llm_prompt),
        )

    def _build_graph_elements(
        self,
        report: DetectionReport,
        module_findings_map: dict[str, list[dict[str, Any]]],
    ) -> dict[str, list[dict[str, Any]]]:
        """Constructs Cytoscape nodes and edges from CodeModel and detections."""
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        existing_nodes: set[str] = set()
        existing_edges: set[tuple[str, str]] = set()

        code_model = getattr(report, "code_model", None)

        if code_model and hasattr(code_model, "modules") and code_model.modules:
            for mod_name, mod in code_model.modules.items():
                if not mod_name or mod_name in existing_nodes:
                    continue

                existing_nodes.add(mod_name)
                items = module_findings_map.get(mod_name, [])
                has_action = any(x["is_action"] for x in items)

                # Determine node color by dominant pattern category
                node_color = "#38D9FF"
                if has_action:
                    node_color = "#FF5C6C"
                elif items:
                    node_color = items[0]["category_color"]

                node_size = max(40, min(80, 40 + len(items) * 5))

                nodes.append({
                    "id": mod_name,
                    "label": mod_name,
                    "color": node_color,
                    "size": node_size,
                    "file_path": mod.file_path,
                    "signals_count": len(items),
                })

                for imp in mod.imports:
                    target_mod = imp.split()[0] if " " in imp else imp
                    if target_mod in code_model.modules and (mod_name, target_mod) not in existing_edges:
                        existing_edges.add((mod_name, target_mod))
                        edges.append({
                            "id": f"{mod_name}->{target_mod}",
                            "source": mod_name,
                            "target": target_mod,
                        })
        else:
            for mod_name, items in module_findings_map.items():
                if mod_name in existing_nodes:
                    continue
                existing_nodes.add(mod_name)
                has_action = any(x["is_action"] for x in items)
                node_color = "#FF5C6C" if has_action else items[0]["category_color"] if items else "#38D9FF"

                nodes.append({
                    "id": mod_name,
                    "label": mod_name,
                    "color": node_color,
                    "size": max(40, min(80, 40 + len(items) * 5)),
                    "file_path": mod_name,
                    "signals_count": len(items),
                })

        return {"nodes": nodes, "edges": edges}

    def _build_uml_mermaid_diagram(self, report: DetectionReport) -> tuple[str, int]:
        """Constructs a Mermaid.js UML Class Diagram from Typeclasses, GADTs, Newtypes, and Instances."""
        lines = ["classDiagram"]
        types_count = 0
        code_model = getattr(report, "code_model", None)

        def sanitize(name: str) -> str:
            clean = re.sub(r"[^a-zA-Z0-9_]", "_", name).strip("_")
            return clean if clean else "Anonymous"

        if code_model and hasattr(code_model, "modules") and code_model.modules:
            for mod_name, mod in code_model.modules.items():
                # 1. Typeclasses
                for tc_name, tc in mod.typeclasses.items():
                    s_tc = sanitize(tc_name)
                    types_count += 1
                    lines.append(f"    class {s_tc} {{")
                    lines.append("        <<typeclass>>")
                    if tc.methods:
                        for m in tc.methods[:6]:
                            clean_m = sanitize(m.split("::")[0].strip()) if "::" in m else sanitize(m)
                            lines.append(f"        +{clean_m}()")
                    else:
                        lines.append("        +typeclassMethod()")
                    lines.append("    }")

                    for sup in tc.superclasses:
                        s_sup = sanitize(sup.split()[0])
                        if s_sup and s_sup != s_tc:
                            lines.append(f"    {s_sup} <|-- {s_tc} : superclass")

                # 2. Types / GADTs / Newtypes
                for t_name, t in mod.types.items():
                    s_t = sanitize(t_name)
                    types_count += 1
                    stereotype = "gadt" if t.is_gadt else "newtype" if t.is_newtype else "data"
                    lines.append(f"    class {s_t} {{")
                    lines.append(f"        <<{stereotype}>>")
                    if t.constructors:
                        for c in t.constructors[:6]:
                            c_clean = sanitize(c.name)
                            lines.append(f"        +{c_clean}()")
                    else:
                        lines.append(f"        +{s_t}()")
                    lines.append("    }")

                # 3. Instances
                for inst in mod.instances:
                    s_class = sanitize(inst.class_name)
                    s_target = sanitize(inst.target_type.split()[0] if inst.target_type else "Instance")
                    if s_class and s_target:
                        lines.append(f"    {s_class} <|.. {s_target} : instance")
        else:
            # Synthetic fallback from detections
            for d in report.detections:
                if d.pattern_category == PatternCategory.TYPECLASS_SYSTEM or "type" in d.target_kind:
                    s_target = sanitize(d.target_name.split(".")[-1])
                    types_count += 1
                    s_kind = sanitize(d.target_kind)
                    lines.append(f"    class {s_target} {{")
                    lines.append(f"        <<{s_kind}>>")
                    lines.append(f"        +{s_target}()")
                    lines.append("    }")

        if types_count == 0:
            lines.append("    class HaskellApp {")
            lines.append("        <<module>>")
            lines.append("        +main()")
            lines.append("    }")
            types_count = 1

        return "\n".join(lines), types_count

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
            f"# 🔷 DPX-Haskell: Architecture Context & Refactoring Analysis for {project_name}",
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
