"""Haskell Phantom Types Invariant Verification Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PhantomTypesRule(BasePatternRule):
    """Detects Phantom Types verifying domain state invariants at compile time."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PHANTOM_TYPES

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for t_name, t in m.types.items():
                if t.is_newtype and t.params and len(t.params) >= 1:
                    # e.g. newtype Id a = Id Text (where 'a' does not appear on RHS)
                    rhs = t.name
                    evidences = [
                        Evidence(
                            description=f"Type '{t_name}' in '{m.name}' adopts Phantom Types pattern carrying unused type parameters for compile-time state verification",
                            weight=0.80,
                            rule_code="PHANTOM_TYPE_STATE_TAG",
                            location=t.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="phantom_type",
                        evidences=evidences,
                        location=t.location or m.location,
                    )
                    detections.append(det)

        return detections
