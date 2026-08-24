"""Haskell Recursion Schemes (Catamorphisms/Anamorphisms) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class RecursionSchemesRule(BasePatternRule):
    """Detects Recursion Schemes (Fix, cata, ana, hylo, Data.Functor.Foldable)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.RECURSION_SCHEMES

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if "Data.Functor.Foldable" in src or "cata " in src or "ana " in src or "Fix " in src or "hylo " in src:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' adopts Recursion Schemes (`cata`/`ana`/`Fix`) abstracting explicit recursive AST traversals into generic morphisms",
                        weight=0.85,
                        rule_code="RECURSION_SCHEMES_MORPHISM",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="recursion_schemes_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
