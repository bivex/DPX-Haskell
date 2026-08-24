"""Haskell Newtype Domain Value Object Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class NewtypeStrongTypingRule(BasePatternRule):
    """Detects newtype Domain Value Objects for zero-cost strong typing."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.NEWTYPE_STRONG_TYPING

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            newtypes = [t for t in m.types.values() if t.is_newtype]
            if len(newtypes) >= 2:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' enforces DDD Value Object strong typing via {len(newtypes)} newtype wrapper(s) at zero runtime cost",
                        weight=0.80,
                        rule_code="NEWTYPE_DOMAIN_VALUE_OBJECT",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="newtype_domain_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
