"""Haskell Catch-All SomeException Anti-Pattern Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CatchAllSomeExceptionRule(BasePatternRule):
    """Detects blanket catching of `SomeException` swallowing asynchronous thread kills."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CATCH_ALL_SOME_EXCEPTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn in m.functions.values():
                if re.search(r"catch[\s\S]*?\\(?:_|\(SomeException\s+[^)]+\)\))\s*->", fn.body) or "handle (\\(_ :: SomeException)" in fn.body:
                    evidences = [
                        Evidence(
                            description=f"Resilience Anti-Pattern: Function '{fn.id_str}' in '{m.name}' catches `SomeException` without rethrowing async exceptions (`ThreadKilled`); use `Control.Exception.Safe`",
                            weight=0.85,
                            rule_code="CATCH_ALL_SOME_EXCEPTION",
                            location=fn.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{fn.name}",
                        target_kind="defensive_catch_function",
                        evidences=evidences,
                        location=fn.location or m.location,
                    )
                    detections.append(det)

        return detections
