"""CLI Inbound Adapter for Haskell Pattern Detector using Typer and Rich."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich import print as rprint
from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pattern_detector.adapters.outbound.persistence.llm_report_formatter import LlmReportFormatter
from pattern_detector.bootstrap.container import Container, create_container
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.pattern import PATTERN_CATALOG
from pattern_detector.domain.value_objects import ConfidenceLevel, PatternCategory, PatternType
from pattern_detector.ports.inbound import ScanOptions

app = typer.Typer(
    name="dpx-haskell",
    help="DPX-Haskell: Static Architecture, Typeclass Idiom, Monad Transformer & Safety Analyzer for Haskell (GHC 9.2 - 9.10+ / Haskell2021).",
    add_completion=False,
)
console = Console()


@app.command(name="scan")
def scan(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to a Haskell project directory or single source file (.hs, .lhs).",
        ),
    ],
    min_confidence: Annotated[
        ConfidenceLevel,
        typer.Option(
            "--min-confidence",
            "-c",
            help="Filter detections by minimum confidence level (low, medium, high, very_high).",
        ),
    ] = ConfidenceLevel.LOW,
    pattern: Annotated[
        list[str] | None,
        typer.Option(
            "--pattern",
            "-p",
            help="Filter by specific pattern type (repeatable).",
        ),
    ] = None,
    json_output: Annotated[
        str | None,
        typer.Option(
            "--json",
            "-J",
            help="Export results to a JSON file.",
        ),
    ] = None,
    html_output: Annotated[
        str | None,
        typer.Option(
            "--html",
            "-H",
            help="Export results to an interactive Dark HTML Dashboard.",
        ),
    ] = None,
    markdown_output: Annotated[
        str | None,
        typer.Option(
            "--markdown",
            "-M",
            help="Export results to a Markdown report file.",
        ),
    ] = None,
    sarif_output: Annotated[
        str | None,
        typer.Option(
            "--sarif",
            "-S",
            help="Export results to OASIS SARIF v2.1.0 format for GitHub Code Scanning / CI-CD.",
        ),
    ] = None,
    llm: Annotated[
        bool,
        typer.Option(
            "--llm",
            help="Output structured AI architectural prompt context.",
        ),
    ] = False,
    no_principles: Annotated[
        bool,
        typer.Option(
            "--no-principles",
            help="Exclude quality principles and clean code smells (Typeclasses, Monads & STM only).",
        ),
    ] = False,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "--exclude",
            "-e",
            help="Directory name(s) or relative paths to exclude from scanning (e.g. -e test -e benchmarks -e examples).",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose logging.",
        ),
    ] = False,
    parser_backend: Annotated[
        str,
        typer.Option(
            "--parser",
            help="Parser backend: 'antlr' (default, ANTLR4 grammar) or 'native' (fast layout-aware).",
        ),
    ] = "antlr",
) -> None:
    """Scan a Haskell project or source file for typeclass idioms, monad stacks, STM concurrency, and space leak hazards."""
    target_path = str(Path(path).resolve())
    container = create_container(parser_type=parser_backend)
    options = ScanOptions(
        min_confidence=min_confidence,
        enabled_patterns=pattern or [],
        output_json_path=json_output,
        output_html_path=html_output,
        output_markdown_path=markdown_output,
        output_sarif_path=sarif_output,
        include_principles=not no_principles,
        exclude_dirs=exclude or [],
        verbose=verbose,
    )

    if llm:
        scanner = container.get_scanner()
        report = scanner.scan_path(target_path, options=options)
        formatter = LlmReportFormatter()
        print(formatter.format(report))
    else:
        _handle_terminal_scan(container, path, target_path, options)


def _handle_terminal_scan(container: Container, raw_path: str, target_path: str, options: ScanOptions) -> None:
    rprint(
        Panel(
            f"[bold purple]DPX-Haskell Architecture & Pattern Engine[/bold purple]\n"
            f"[dim]Target: {raw_path}[/dim]",
            border_style="purple",
        )
    )

    with console.status("[bold blue]Scanning Haskell modules, typeclasses, monad stacks, and STM blocks...[/bold blue]"):
        scanner = container.get_scanner()
        report = scanner.scan_path(target_path, options=options)

    if not report.detections:
        rprint("[yellow]No patterns or architecture smells detected.[/yellow]")
        return

    _render_summary(report)
    _render_detections(report)


def _render_summary(report: DetectionReport) -> None:
    table = Table(
        title=f"Scan Summary: {report.scanned_files_count} files in {report.elapsed_seconds}s",
        box=ROUNDED,
    )
    table.add_column("Category", style="cyan")
    table.add_column("Detections", style="magenta", justify="right")

    for cat, cnt in sorted(report.summary_by_category.items()):
        table.add_row(cat, str(cnt))

    console.print(table)


def _render_detections(report: DetectionReport) -> None:
    for i, d in enumerate(report.detections, 1):
        color = "green" if d.level == ConfidenceLevel.VERY_HIGH else "blue" if d.level == ConfidenceLevel.HIGH else "yellow"
        loc_str = str(d.primary_location) if d.primary_location else "N/A"

        rprint(
            f"\n[bold #{color}]#{i} {d.pattern_type.value.upper()}[/bold #{color}] on [dim]{d.target_kind}[/dim] [bold]{d.target_name}[/bold]"
        )
        rprint(f"├── 📍 Location: [cyan]{loc_str}[/cyan]")
        rprint(f"├── 🎯 Confidence: [{color}]{d.confidence.percentage_str} [{d.level.value.upper()}][/{color}]")
        rprint(f"├── 📝 Summary: {d.summary}")

        if d.evidences:
            rprint(f"└── 🔎 Evidence Trail ({len(d.evidences)} heuristics):")
            for ev in d.evidences:
                rprint(f"    └── +{int(ev.weight * 100)}% ({ev.rule_code}) {ev.description}")


@app.command(name="list-patterns")
def list_patterns() -> None:
    """List all supported Haskell design patterns, typeclass idioms, and safety rules."""
    table = Table(title="DPX-Haskell Pattern & Safety Rule Catalog", box=ROUNDED)
    table.add_column("Pattern Type", style="cyan")
    table.add_column("Category", style="purple")
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")

    for pt, entry in PATTERN_CATALOG.items():
        table.add_row(pt.value, entry.category.value, entry.name, entry.description)

    console.print(table)


@app.command(name="version")
def version() -> None:
    """Display DPX-Haskell version information."""
    rprint("[bold purple]DPX-Haskell[/bold purple] version [bold cyan]0.1.0[/bold cyan]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
