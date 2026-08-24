"""Tests for DPX-Haskell Domain Value Objects and CodeModel."""

from pattern_detector.domain.code_model import CodeModel, ModuleModel
from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    SourceLocation,
)


def test_confidence_calculation():
    e1 = Evidence(description="Test rule 1", weight=0.6, rule_code="R1")
    e2 = Evidence(description="Test rule 2", weight=0.5, rule_code="R2")
    conf = Confidence.from_evidences([e1, e2])
    # 1 - (1 - 0.6) * (1 - 0.5) = 1 - 0.4 * 0.5 = 0.80
    assert abs(conf.score - 0.80) < 1e-4
    assert conf.level == ConfidenceLevel.HIGH
    assert conf.percentage_str == "80%"


def test_source_location_str():
    loc = SourceLocation(file_path="src/App.hs", line=42, column=5)
    assert str(loc) == "src/App.hs:42:5"


def test_circular_module_import_detection():
    m1 = ModuleModel(name="ModuleA", file_path="ModuleA.hs", imports=["ModuleB"])
    m2 = ModuleModel(name="ModuleB", file_path="ModuleB.hs", imports=["ModuleC"])
    m3 = ModuleModel(name="ModuleC", file_path="ModuleC.hs", imports=["ModuleA"])

    model = CodeModel(modules={"ModuleA": m1, "ModuleB": m2, "ModuleC": m3})
    cycles = model.find_circular_imports()

    assert len(cycles) == 1
    assert set(cycles[0]) == {"ModuleA", "ModuleB", "ModuleC"}
