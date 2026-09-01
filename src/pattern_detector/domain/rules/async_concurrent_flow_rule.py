"""Haskell Structured Async Concurrency Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AsyncConcurrentFlowRule(BasePatternRule):
    """Detects structured asynchronous concurrency (async, concurrently, race, wait)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ASYNC_CONCURRENT_FLOW

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.clean_source or m.raw_source
            if "Control.Concurrent.Async" in m.imports or re.search(r"\b(concurrently|race|async|waitBoth|withAsync)\b", src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' manages concurrent tasks via Structured Async Concurrency (`async`/`concurrently`/`race`) with automatic cancellation propagation",
                        weight=0.85,
                        rule_code="STRUCTURED_ASYNC_CONCURRENCY",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="async_concurrency_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
