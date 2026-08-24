"""Haskell Deriving Strategies Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DerivingStrategiesRule(BasePatternRule):
    """Detects explicit Deriving Strategies (stock, newtype, anyclass)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DERIVING_STRATEGIES

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            has_strategies = any(t.deriving_strategies for t in m.types.values())
            if has_strategies or "DerivingStrategies" in m.pragmas or "deriving stock" in m.raw_source or "deriving newtype" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' explicitly specifies Deriving Strategies (stock/newtype/anyclass) ensuring deterministic typeclass derivation",
                        weight=0.80,
                        rule_code="EXPLICIT_DERIVING_STRATEGIES",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="deriving_strategies_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
