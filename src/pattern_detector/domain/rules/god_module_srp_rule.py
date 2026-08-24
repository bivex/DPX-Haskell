"""Haskell Single Responsibility (God Module) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GodModuleSrpRule(BasePatternRule):
    """Detects God Modules in Haskell (≥30 declarations or ≥800 LOC)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GOD_MODULE_SRP

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            decl_count = len(m.functions) + len(m.types) + len(m.typeclasses)
            loc_count = m.raw_source.count("\n") + 1

            if decl_count >= 30 or loc_count >= 800:
                evidences = [
                    Evidence(
                        description=f"SRP Violation (God Module): Module '{m.name}' contains {decl_count} declarations across {loc_count} lines of code; decompose into focused domain modules",
                        weight=0.85,
                        rule_code="SRP_GOD_MODULE",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="god_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
