"""Haskell Railway Do-Notation Monadic Flow Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class RailwayDoNotationRule(BasePatternRule):
    """Detects monadic railway chaining in `do` blocks."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.RAILWAY_DO_NOTATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn in m.functions.values():
                bind_count = fn.body.count(" <- ") + fn.body.count(" >>= ")
                if fn.has_do and bind_count >= 3:
                    evidences = [
                        Evidence(
                            description=f"Function '{fn.id_str}' in '{m.name}' chains a {bind_count}-step Monadic Railway flow in `do` notation",
                            weight=0.80,
                            rule_code="MONADIC_DO_RAILWAY_PIPELINE",
                            location=fn.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{fn.name}",
                        target_kind="monadic_function",
                        evidences=evidences,
                        location=fn.location or m.location,
                    )
                    detections.append(det)

        return detections
