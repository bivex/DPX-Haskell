"""Haskell Unchecked fromJust Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class UncheckedFromJustRule(BasePatternRule):
    """Detects unsafe `fromJust` partial function calls risking runtime crashes."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNCHECKED_FROM_JUST

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn in m.functions.values():
                if re.search(r"\bfromJust\b", fn.body):
                    evidences = [
                        Evidence(
                            description=f"Type Safety Hazard: Function '{fn.id_str}' in '{m.name}' calls partial `fromJust` which throws an uncatchable exception on `Nothing`; use `fromMaybe` or pattern match",
                            weight=0.85,
                            rule_code="UNSAFE_FROM_JUST_CALL",
                            location=fn.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{fn.name}",
                        target_kind="unsafe_from_just_function",
                        evidences=evidences,
                        location=fn.location or m.location,
                    )
                    detections.append(det)

        return detections
