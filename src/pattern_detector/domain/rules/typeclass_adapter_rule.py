"""Haskell Typeclass Interface Adapter Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TypeclassAdapterRule(BasePatternRule):
    """Detects Typeclass Interface Adapters (class Name a where ...)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TYPECLASS_ADAPTER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for tc_name, tc in m.typeclasses.items():
                evidences = [
                    Evidence(
                        description=f"Typeclass '{tc_name}' in '{m.name}' defines an ad-hoc polymorphic Adapter interface with {len(tc.methods)} method(s)",
                        weight=0.85,
                        rule_code="TYPECLASS_INTERFACE_ADAPTER",
                        location=tc.location or m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=f"{m.name}.{tc_name}",
                    target_kind="typeclass",
                    evidences=evidences,
                    location=tc.location or m.location,
                )
                detections.append(det)

        return detections
