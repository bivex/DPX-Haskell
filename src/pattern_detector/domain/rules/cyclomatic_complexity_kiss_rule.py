"""Haskell KISS Complexity Rule (Pattern Matching & Guards)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CyclomaticComplexityKissRule(BasePatternRule):
    """Detects KISS violations in Haskell (branches in case...of / guards ≥12)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CYCLOMATIC_COMPLEXITY_KISS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn in m.functions.values():
                if fn.cyclomatic_complexity >= 12:
                    evidences = [
                        Evidence(
                            description=f"KISS Violation (High Complexity): Function '{fn.id_str}' in '{m.name}' has cyclomatic complexity of {fn.cyclomatic_complexity}; refactor complex pattern branches",
                            weight=0.75,
                            rule_code="KISS_HIGH_CYCLOMATIC_COMPLEXITY",
                            location=fn.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{fn.name}",
                        target_kind="complex_function",
                        evidences=evidences,
                        location=fn.location or m.location,
                    )
                    detections.append(det)

        return detections
