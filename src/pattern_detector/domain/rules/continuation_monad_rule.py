"""Haskell Continuation Monad (ContT/callCC) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ContinuationMonadRule(BasePatternRule):
    """Detects Continuation Monad and callCC usage (ContT, callCC)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CONTINUATION_MONAD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if "ContT" in src or "callCC" in src or "runCont" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' employs Continuation Monad (`ContT`/`callCC`) for non-local control transfer and coroutine composition",
                        weight=0.85,
                        rule_code="CONTINUATION_MONAD_CALLCC",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="continuation_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
