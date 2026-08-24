"""Haskell Lazy Space Leak Hazard Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LazySpaceLeakRiskRule(BasePatternRule):
    """Detects space leak hazards (lazy foldl, lazy State monad in loops)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LAZY_SPACE_LEAK_RISK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn in m.functions.values():
                body = fn.body
                if re.search(r"\bfoldl\s+[^\'\s]", body) or ("Control.Monad.State" in m.raw_source and "Control.Monad.State.Strict" not in m.raw_source and "modify" in body):
                    evidences = [
                        Evidence(
                            description=f"Resilience Risk (Lazy Space Leak): Function '{fn.id_str}' in '{m.name}' uses unforced lazy accumulator (`foldl`/lazy `State`); replace with strict `foldl'` / `Control.Monad.State.Strict`",
                            weight=0.80,
                            rule_code="LAZY_SPACE_LEAK_ACCUMULATOR",
                            location=fn.location or m.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{m.name}.{fn.name}",
                        target_kind="space_leak_hazard_function",
                        evidences=evidences,
                        location=fn.location or m.location,
                    )
                    detections.append(det)

        return detections
