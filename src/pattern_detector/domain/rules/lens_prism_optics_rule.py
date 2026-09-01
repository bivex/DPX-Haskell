"""Haskell Functional Optics (Lenses & Prisms) Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LensPrismOpticsRule(BasePatternRule):
    """Detects Functional Optics (makeLenses, (^.), (.~), preview, view)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LENS_PRISM_OPTICS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.clean_source or m.raw_source
            if "Control.Lens" in m.imports or "Optics" in m.imports or re.search(r"\b(makeLenses|makePrisms|makeFields)\b", src) or re.search(r"(\^\.|\.~|%~)", src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' integrates Functional Optics (Lenses/Prisms) for composable immutable data access and transformation",
                        weight=0.85,
                        rule_code="FUNCTIONAL_OPTICS_LENSES",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="lens_optics_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
