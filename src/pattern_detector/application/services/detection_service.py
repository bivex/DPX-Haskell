"""Application service orchestrating Haskell pattern detection rules."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules import DEFAULT_RULES, PatternRule
from pattern_detector.domain.value_objects import PatternCategory
from pattern_detector.ports.inbound import DetectorPort, ScanOptions


class PatternDetectorService(DetectorPort):
    """Executes registered Haskell pattern detection rules against domain CodeModel."""

    def __init__(self, rules: list[PatternRule] | None = None) -> None:
        self._rules = rules if rules is not None else list(DEFAULT_RULES)

    @property
    def rules(self) -> list[PatternRule]:
        return list(self._rules)

    def detect_patterns(self, model: CodeModel, options: ScanOptions | None = None) -> list[Detection]:
        opts = options or ScanOptions()
        all_detections: list[Detection] = []

        for rule in self._rules:
            # Filter out quality principles if excluded
            if not opts.include_principles and rule.pattern_category == PatternCategory.PRINCIPLE:
                continue

            # Category filter
            if opts.categories and rule.pattern_category not in opts.categories:
                continue

            # Specific pattern filter
            if opts.enabled_patterns and rule.pattern_type.value not in opts.enabled_patterns:
                continue

            try:
                rule_detections = rule.detect(model)
                for det in rule_detections:
                    if det.confidence.score >= self._min_score_for_level(opts.min_confidence):
                        all_detections.append(det)
            except Exception:
                continue

        return all_detections

    def _min_score_for_level(self, level) -> float:
        mapping = {
            "low": 0.0,
            "medium": 0.50,
            "high": 0.70,
            "very_high": 0.85,
        }
        val = level.value if hasattr(level, "value") else str(level)
        return mapping.get(val, 0.0)
