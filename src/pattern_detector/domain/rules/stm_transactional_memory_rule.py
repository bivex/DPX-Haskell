"""Haskell Software Transactional Memory (STM) Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StmTransactionalMemoryRule(BasePatternRule):
    """Detects Software Transactional Memory (STM) lock-free concurrency."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STM_TRANSACTIONAL_MEMORY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.clean_source or m.raw_source
            if "Control.Concurrent.STM" in m.imports or re.search(r"\b(atomically|TVar|TMVar|retry|orElse)\b", src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' coordinates concurrency via Software Transactional Memory (STM) ensuring composable, deadlock-free transactional atomicity",
                        weight=0.90,
                        rule_code="SOFTWARE_TRANSACTIONAL_MEMORY",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="stm_concurrency_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
