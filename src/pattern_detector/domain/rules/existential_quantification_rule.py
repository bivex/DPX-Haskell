"""Haskell Existential Quantification Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ExistentialQuantificationRule(BasePatternRule):
    """Detects Existential Heterogeneous Type Wrappers (forall a. Class a => ...)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.EXISTENTIAL_QUANTIFICATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if re.search(r"data\s+[A-Z][a-zA-Z0-9_]*\s*=\s*forall\s+[a-z0-9_]+", src) or ("ExistentialQuantification" in m.pragmas and "forall " in src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' adopts Existential Quantification wrapping heterogeneous types satisfying a common typeclass constraint",
                        weight=0.85,
                        rule_code="EXISTENTIAL_HETEROGENEOUS_WRAPPER",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="existential_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
