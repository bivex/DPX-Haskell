"""Haskell Tagless Final Capability Style Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TaglessFinalStyleRule(BasePatternRule):
    """Detects Tagless Final / MTL Capability classes (class Monad m => MonadDB m where ...)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TAGLESS_FINAL_STYLE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for tc_name, tc in m.typeclasses.items():
                if tc_name.startswith("Monad") and len(tc_name) > 5 and any("m " in m_str or "-> m" in m_str for m_str in tc.methods):
                    evidences = [
                        Evidence(
                            description=f"Typeclass '{tc_name}' in '{m.name}' adopts Tagless Final / MTL capability pattern providing polymorphic monadic effects",
                            weight=0.85,
                            rule_code="TAGLESS_FINAL_CAPABILITY_CLASS",
                            location=tc.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{tc_name}",
                        target_kind="tagless_final_capability",
                        evidences=evidences,
                        location=tc.location or m.location,
                    )
                    detections.append(det)

        return detections
