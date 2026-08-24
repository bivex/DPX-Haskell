"""Haskell Unchecked Bottom / Panic Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class UncheckedBottomErrorRule(BasePatternRule):
    """Detects partial crashes / bottom values (error, undefined, head, tail)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNCHECKED_BOTTOM_ERROR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn in m.functions.values():
                body = fn.body
                if re.search(r"\berror\s+\"[^\"]+\"", body) or re.search(r"\bundefined\b", body):
                    evidences = [
                        Evidence(
                            description=f"Type Safety Hazard: Function '{fn.id_str}' in '{m.name}' introduces runtime bottom panic (`error`/`undefined`); return typed `Either` or `Maybe` instead",
                            weight=0.85,
                            rule_code="UNCHECKED_BOTTOM_PANIC",
                            location=fn.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{fn.name}",
                        target_kind="unsafe_bottom_function",
                        evidences=evidences,
                        location=fn.location or m.location,
                    )
                    detections.append(det)

        return detections
