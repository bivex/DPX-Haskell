"""Domain value objects for the Haskell Pattern Detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Broad classification of Haskell design patterns, typeclass idioms, monad transformers, and safety rules."""

    TYPECLASS_SYSTEM = "typeclass_system"
    MONAD_ARCHITECTURE = "monad_architecture"
    FUNCTIONAL_IDIOM = "functional_idiom"
    CONCURRENCY_STM = "concurrency_stm"
    OPTICS_LENSES = "optics_lenses"
    RESILIENCE = "resilience"
    PRINCIPLE = "principle"
    TYPE_SAFETY = "type_safety"


class PatternType(str, Enum):
    """Specific Haskell design pattern, monad transformer, STM concurrency, and architecture smell identifiers."""

    # Typeclasses & Polymorphism (6)
    TYPECLASS_ADAPTER = "typeclass_adapter"
    TYPE_FAMILY_ASSOCIATED = "type_family_associated"
    EXISTENTIAL_QUANTIFICATION = "existential_quantification"
    GADTS_TYPE_SAFE_AST = "gadts_type_safe_ast"
    NEWTYPE_STRONG_TYPING = "newtype_strong_typing"
    DERIVING_STRATEGIES = "deriving_strategies"

    # Functional Architecture, Monads & Transformers (8)
    READER_T_DESIGN_PATTERN = "reader_t_design_pattern"
    MONAD_TRANSFORMER_STACK = "monad_transformer_stack"
    FREE_MONAD_INTERPRETER = "free_monad_interpreter"
    TAGLESS_FINAL_STYLE = "tagless_final_style"
    RAILWAY_DO_NOTATION = "railway_do_notation"
    LENS_PRISM_OPTICS = "lens_prism_optics"
    CONTINUATION_MONAD = "continuation_monad"
    SMART_CONSTRUCTOR_MODULE = "smart_constructor_module"
    RECURSION_SCHEMES = "recursion_schemes"
    BRACKET_RESOURCE_MANAGEMENT = "bracket_resource_management"
    TYPE_LEVEL_LITERALS = "type_level_literals"
    PHANTOM_TYPES = "phantom_types"

    # Concurrency, Parallelism & Streams (4)

    STM_TRANSACTIONAL_MEMORY = "stm_transactional_memory"
    ASYNC_CONCURRENT_FLOW = "async_concurrent_flow"
    STREAM_PROCESSING_PIPELINE = "stream_processing_pipeline"
    CHAN_MVAR_MAILBOX = "chan_mvar_mailbox"

    # Type Safety, Space Leaks, Clean Code & SOLID (8)
    UNCHECKED_BOTTOM_ERROR = "unchecked_bottom_error"
    UNCHECKED_FROM_JUST = "unchecked_from_just"
    LAZY_SPACE_LEAK_RISK = "lazy_space_leak_risk"
    CATCH_ALL_SOME_EXCEPTION = "catch_all_some_exception"
    GOD_MODULE_SRP = "god_module_srp"
    CYCLOMATIC_COMPLEXITY_KISS = "cyclomatic_complexity_kiss"
    DUPLICATE_CODE_DRY = "duplicate_code_dry"
    CIRCULAR_MODULE_IMPORT = "circular_module_import"


class ConfidenceLevel(str, Enum):
    """Categorical confidence rating for a pattern detection."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

    @classmethod
    def from_score(cls, score: float) -> ConfidenceLevel:
        if score >= 0.85:
            return cls.VERY_HIGH
        if score >= 0.70:
            return cls.HIGH
        if score >= 0.50:
            return cls.MEDIUM
        return cls.LOW


@dataclass(frozen=True)
class SourceLocation:
    """Represents a precise location in a Haskell source file (.hs / .lhs)."""

    file_path: str
    line: int = 1
    column: int = 1
    end_line: int | None = None
    end_column: int | None = None

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Evidence:
    """A single piece of heuristic evidence supporting a pattern detection."""

    description: str
    weight: float
    rule_code: str
    location: SourceLocation | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Evidence weight must be between 0.0 and 1.0, got {self.weight}")


@dataclass(frozen=True)
class Confidence:
    """Aggregated confidence score computed from multiple pieces of evidence."""

    score: float
    level: ConfidenceLevel = field(init=False)

    def __post_init__(self) -> None:
        clamped = max(0.0, min(1.0, self.score))
        object.__setattr__(self, "score", clamped)
        object.__setattr__(self, "level", ConfidenceLevel.from_score(clamped))

    @classmethod
    def from_evidences(cls, evidences: list[Evidence]) -> Confidence:
        if not evidences:
            return cls(0.0)
        complement_product = 1.0
        for ev in evidences:
            complement_product *= (1.0 - ev.weight)
        return cls(1.0 - complement_product)

    @property
    def percentage_str(self) -> str:
        return f"{int(self.score * 100)}%"
