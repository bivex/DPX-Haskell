"""Haskell Actor Mailbox Channel Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ChanMvarMailboxRule(BasePatternRule):
    """Detects Actor Mailbox message channels (TQueue, TChan, Chan, MVar)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CHAN_MVAR_MAILBOX

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.clean_source or m.raw_source
            if re.search(r"\b(TQueue|TChan|newChan|writeChan|readChan|newTQueue|newMVar|takeMVar|putMVar)\b", src):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' coordinates worker synchronization via Actor Mailbox Channel (`TQueue`/`TChan`/`Chan`)",
                        weight=0.85,
                        rule_code="ACTOR_MAILBOX_CHANNEL",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="mailbox_channel_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
