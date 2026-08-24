"""Rule catalog registration for Haskell Pattern Detector."""

from __future__ import annotations

from pattern_detector.domain.rules.async_concurrent_flow_rule import AsyncConcurrentFlowRule
from pattern_detector.domain.rules.base import BasePatternRule, PatternRule
from pattern_detector.domain.rules.bracket_resource_management_rule import BracketResourceManagementRule
from pattern_detector.domain.rules.catch_all_some_exception_rule import CatchAllSomeExceptionRule
from pattern_detector.domain.rules.chan_mvar_mailbox_rule import ChanMvarMailboxRule
from pattern_detector.domain.rules.circular_module_import_rule import CircularModuleImportRule
from pattern_detector.domain.rules.continuation_monad_rule import ContinuationMonadRule
from pattern_detector.domain.rules.cyclomatic_complexity_kiss_rule import CyclomaticComplexityKissRule
from pattern_detector.domain.rules.deriving_strategies_rule import DerivingStrategiesRule
from pattern_detector.domain.rules.duplicate_code_dry_rule import DuplicateCodeDryRule
from pattern_detector.domain.rules.existential_quantification_rule import ExistentialQuantificationRule
from pattern_detector.domain.rules.free_monad_interpreter_rule import FreeMonadInterpreterRule
from pattern_detector.domain.rules.gadts_type_safe_ast_rule import GadtsTypeSafeAstRule
from pattern_detector.domain.rules.god_module_srp_rule import GodModuleSrpRule
from pattern_detector.domain.rules.lazy_space_leak_risk_rule import LazySpaceLeakRiskRule
from pattern_detector.domain.rules.lens_prism_optics_rule import LensPrismOpticsRule
from pattern_detector.domain.rules.monad_transformer_stack_rule import MonadTransformerStackRule
from pattern_detector.domain.rules.newtype_strong_typing_rule import NewtypeStrongTypingRule
from pattern_detector.domain.rules.phantom_types_rule import PhantomTypesRule
from pattern_detector.domain.rules.railway_do_notation_rule import RailwayDoNotationRule
from pattern_detector.domain.rules.reader_t_design_pattern_rule import ReaderTDesignPatternRule
from pattern_detector.domain.rules.recursion_schemes_rule import RecursionSchemesRule
from pattern_detector.domain.rules.smart_constructor_module_rule import SmartConstructorModuleRule
from pattern_detector.domain.rules.stm_transactional_memory_rule import StmTransactionalMemoryRule
from pattern_detector.domain.rules.stream_processing_pipeline_rule import StreamProcessingPipelineRule
from pattern_detector.domain.rules.tagless_final_style_rule import TaglessFinalStyleRule
from pattern_detector.domain.rules.type_family_associated_rule import TypeFamilyAssociatedRule
from pattern_detector.domain.rules.type_level_literals_rule import TypeLevelLiteralsRule
from pattern_detector.domain.rules.typeclass_adapter_rule import TypeclassAdapterRule
from pattern_detector.domain.rules.unchecked_bottom_error_rule import UncheckedBottomErrorRule
from pattern_detector.domain.rules.unchecked_from_just_rule import UncheckedFromJustRule

DEFAULT_RULES: list[PatternRule] = [
    # Typeclasses & Polymorphism (8)
    TypeclassAdapterRule(),
    TypeFamilyAssociatedRule(),
    ExistentialQuantificationRule(),
    GadtsTypeSafeAstRule(),
    NewtypeStrongTypingRule(),
    DerivingStrategiesRule(),
    TypeLevelLiteralsRule(),
    PhantomTypesRule(),

    # Functional Architecture, Monads & Transformers (9)
    ReaderTDesignPatternRule(),
    MonadTransformerStackRule(),
    FreeMonadInterpreterRule(),
    TaglessFinalStyleRule(),
    RailwayDoNotationRule(),
    LensPrismOpticsRule(),
    ContinuationMonadRule(),
    SmartConstructorModuleRule(),
    RecursionSchemesRule(),

    # Concurrency, Parallelism & Streams (4)
    StmTransactionalMemoryRule(),
    AsyncConcurrentFlowRule(),
    StreamProcessingPipelineRule(),
    ChanMvarMailboxRule(),

    # Type Safety, Space Leaks, Clean Code & SOLID (9)
    UncheckedBottomErrorRule(),
    UncheckedFromJustRule(),
    LazySpaceLeakRiskRule(),
    CatchAllSomeExceptionRule(),
    BracketResourceManagementRule(),
    GodModuleSrpRule(),
    CyclomaticComplexityKissRule(),
    DuplicateCodeDryRule(),
    CircularModuleImportRule(),
]

__all__ = [
    "BasePatternRule",
    "PatternRule",
    "DEFAULT_RULES",
    "TypeclassAdapterRule",
    "TypeFamilyAssociatedRule",
    "ExistentialQuantificationRule",
    "GadtsTypeSafeAstRule",
    "NewtypeStrongTypingRule",
    "DerivingStrategiesRule",
    "TypeLevelLiteralsRule",
    "PhantomTypesRule",
    "ReaderTDesignPatternRule",
    "MonadTransformerStackRule",
    "FreeMonadInterpreterRule",
    "TaglessFinalStyleRule",
    "RailwayDoNotationRule",
    "LensPrismOpticsRule",
    "ContinuationMonadRule",
    "SmartConstructorModuleRule",
    "RecursionSchemesRule",
    "StmTransactionalMemoryRule",
    "AsyncConcurrentFlowRule",
    "StreamProcessingPipelineRule",
    "ChanMvarMailboxRule",
    "UncheckedBottomErrorRule",
    "UncheckedFromJustRule",
    "LazySpaceLeakRiskRule",
    "CatchAllSomeExceptionRule",
    "BracketResourceManagementRule",
    "GodModuleSrpRule",
    "CyclomaticComplexityKissRule",
    "DuplicateCodeDryRule",
    "CircularModuleImportRule",
]
