"""Haskell GADT Type-Safe AST Evaluator Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GadtsTypeSafeAstRule(BasePatternRule):
    """Detects Generalized Algebraic Data Types (GADTs) in Haskell."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GADTS_TYPE_SAFE_AST

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for t_name, t in m.types.items():
                if t.is_gadt:
                    evidences = [
                        Evidence(
                            description=f"Data type '{t_name}' in '{m.name}' implements Generalized Algebraic Data Type (GADT) ensuring compile-time type preservation",
                            weight=0.85,
                            rule_code="GADT_TYPE_SAFE_AST",
                            location=t.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="gadt_data_type",
                        evidences=evidences,
                        location=t.location or m.location,
                    )
                    detections.append(det)

        return detections
