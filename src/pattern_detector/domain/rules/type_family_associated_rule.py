"""Haskell Type Families & Associated Types Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TypeFamilyAssociatedRule(BasePatternRule):
    """Detects Type Families and Associated Data/Type Families."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TYPE_FAMILY_ASSOCIATED

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if "type family " in src or "data family " in src or any(tc.associated_types for tc in m.typeclasses.values()):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' implements Type Families / Associated Types for type-level computation and indexed type mappings",
                        weight=0.85,
                        rule_code="TYPE_FAMILY_ASSOCIATED_TYPES",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="type_family_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
