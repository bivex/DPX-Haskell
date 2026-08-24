"""Haskell The ReaderT Design Pattern Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ReaderTDesignPatternRule(BasePatternRule):
    """Detects The ReaderT Design Pattern (ReaderT Env IO a / newtype App = App (ReaderT ...))."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.READER_T_DESIGN_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if "ReaderT " in src and " IO" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' adopts The ReaderT Design Pattern (`ReaderT Env IO`) for clean dependency injection and static environment access",
                        weight=0.90,
                        rule_code="READER_T_PATTERN_DI",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="reader_t_architecture",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
