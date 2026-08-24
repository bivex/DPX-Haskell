"""Haskell Smart Constructor Encapsulation Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SmartConstructorModuleRule(BasePatternRule):
    """Detects Smart Constructor validation functions (mk... :: ... -> Either/Maybe)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SMART_CONSTRUCTOR_MODULE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for m in model.all_modules():
            for fn_name, fn in m.functions.items():
                if fn_name.startswith("mk") and len(fn_name) > 2 and fn_name[2].isupper():
                    if "Either " in fn.type_signature or "Maybe " in fn.type_signature or "Right " in fn.body or "Left " in fn.body or "Just " in fn.body:
                        evidences = [
                            Evidence(
                                description=f"Function '{fn.id_str}' in '{m.name}' implements Smart Constructor pattern enforcing domain validation invariants",
                                weight=0.80,
                                rule_code="SMART_CONSTRUCTOR_INVARIANT",
                                location=fn.location or m.location,
                            )
                        ]
                        det = self._create_detection(
                            target_name=f"{m.name}.{fn.name}",
                            target_kind="smart_constructor_function",
                            evidences=evidences,
                            location=fn.location or m.location,
                        )
                        detections.append(det)

        return detections
