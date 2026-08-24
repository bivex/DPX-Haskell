"""Haskell Type-Level Programming (DataKinds & TypeLits) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TypeLevelLiteralsRule(BasePatternRule):
    """Detects Type-Level computation (DataKinds, GHC.TypeLits, KnownNat, KnownSymbol, Symbol)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TYPE_LEVEL_LITERALS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            src = m.raw_source
            if "DataKinds" in m.pragmas or "GHC.TypeLits" in src or "GHC.TypeNats" in src or "KnownNat" in src or "KnownSymbol" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' implements Type-Level Programming (`DataKinds`/`GHC.TypeLits`) enforcing compile-time dimensionality and protocol invariants",
                        weight=0.85,
                        rule_code="TYPE_LEVEL_LITERALS_DATAKINDS",
                        location=m.location,
                    )
                ]
                det = self._create_detection(
                    target_name=m.name,
                    target_kind="type_level_module",
                    evidences=evidences,
                    location=m.location,
                )
                detections.append(det)

        return detections
