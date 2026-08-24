"""Tests for ScanningService and FileSourceProvider exclusions."""

import tempfile
from pathlib import Path

from pattern_detector.adapters.outbound.persistence.file_source_provider import FileSourceProvider
from pattern_detector.bootstrap.container import create_container
from pattern_detector.ports.inbound import ScanOptions


def test_file_source_provider_exclude_dirs():
    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir)
        (base / "src").mkdir()
        (base / "test").mkdir()
        (base / "benchmarks").mkdir()

        (base / "src" / "Lib.hs").write_text("module Lib where\nval = 1", encoding="utf-8")
        (base / "test" / "LibTest.hs").write_text("module LibTest where\ntest1 = 2", encoding="utf-8")
        (base / "benchmarks" / "Bench.hs").write_text("module Bench where\nb = 3", encoding="utf-8")

        provider = FileSourceProvider()
        sources = provider.get_sources(str(base), exclude_dirs=["test", "benchmarks"])

        assert len(sources) == 1
        assert any("src/Lib.hs" in k or "src\\Lib.hs" in k for k in sources.keys())


def test_scanning_service_memory():
    container = create_container()
    scanner = container.get_scanner()

    sources = {
        "App.hs": """
module App where

import Control.Monad.Reader

type AppM a = ReaderT Config IO a
"""
    }

    report = scanner.scan_sources(sources)
    assert report.scanned_files_count == 1
    assert report.total_detections_count >= 1
