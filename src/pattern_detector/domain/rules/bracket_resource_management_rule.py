"""Haskell Bracket Resource Management (RAII) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BracketResourceManagementRule(BasePatternRule):
    """Detects deterministic resource cleanup via Bracket / ResourceT (bracket, bracketOnError, withFile)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BRACKET_RESOURCE_MANAGEMENT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if "bracket " in src or "bracketOnError" in src or "ResourceT" in src or "withFile" in src or "withBinaryFile" in src or "withSocketsDo" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' enforces deterministic resource cleanup via Bracket Pattern (`bracket`/`ResourceT`) guaranteeing cleanup even under asynchronous exceptions",
                        weight=0.85,
                        rule_code="BRACKET_RESOURCE_MANAGEMENT",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="bracket_resource_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
