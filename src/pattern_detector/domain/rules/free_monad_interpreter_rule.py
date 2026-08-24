"""Haskell Free Monad DSL Interpreter Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FreeMonadInterpreterRule(BasePatternRule):
    """Detects Free Monad DSL programs and interpreters (Free, liftF, iterM)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FREE_MONAD_INTERPRETER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if ("Free " in src or "Control.Monad.Free" in src or "liftF" in src) and ("type " in src or "data " in src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' implements Free Monad DSL Interpreter separating program description from operational interpretation",
                        weight=0.85,
                        rule_code="FREE_MONAD_DSL_INTERPRETER",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="free_monad_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
