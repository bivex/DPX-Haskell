"""Haskell Stream Processing Pipeline Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StreamProcessingPipelineRule(BasePatternRule):
    """Detects constant-memory streaming pipelines (Conduit, Pipes, Streaming)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STREAM_PROCESSING_PIPELINE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.clean_source or m.raw_source
            if any(imp.startswith("Data.Conduit") or imp.startswith("Pipes") or imp.startswith("Streaming") for imp in m.imports) or ".|" in src or re.search(r"\b(ConduitT|Producer|Consumer|Pipe)\b", src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' constructs a Stream Processing Pipeline ensuring constant-memory processing and backpressure guarantees",
                        weight=0.85,
                        rule_code="STREAM_PROCESSING_PIPELINE",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="streaming_pipeline_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
