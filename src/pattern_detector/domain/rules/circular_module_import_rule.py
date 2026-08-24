"""Haskell Circular Module Import Cycle Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CircularModuleImportRule(BasePatternRule):
    """Detects cyclic `import` dependencies between Haskell modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CIRCULAR_MODULE_IMPORT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        cycles = model.find_circular_imports()

        for cycle in cycles:
            cycle_str = " ➔ ".join(cycle) + " ➔ " + cycle[0]
            first_mod = model.find_module(cycle[0])
            loc = first_mod.location if first_mod else None

            evidences = [
                Evidence(
                    description=f"Circular Module Import detected: {cycle_str}",
                    weight=0.85,
                    rule_code="CIRCULAR_MODULE_CYCLE",
                    location=loc,
                )
            ]
            det = self._create_detection(
                target_name=" ⇄ ".join(cycle),
                target_kind="module_cycle",
                evidences=evidences,
                location=loc,
            )
            detections.append(det)

        return detections
