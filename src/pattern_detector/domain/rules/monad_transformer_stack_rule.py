"""Haskell Monad Transformer Stack Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MonadTransformerStackRule(BasePatternRule):
    """Detects layered Monad Transformer Stacks (ExceptT, StateT, ReaderT, WriterT)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MONAD_TRANSFORMER_STACK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            transformers = re.findall(r"\b(ExceptT|StateT|ReaderT|WriterT|MaybeT|IdentityT|ContT|RWST)\b", src)
            unique_t = set(transformers)
            if len(unique_t) >= 2 or ("type " in src and len(transformers) >= 2):
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' layers a Monad Transformer Stack combining {len(unique_t)} distinct computational capabilities ({', '.join(sorted(unique_t))})",
                        weight=0.85,
                        rule_code="MONAD_TRANSFORMER_LAYER_STACK",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="monad_transformer_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
