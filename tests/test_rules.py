"""Tests for Haskell Pattern Detection Rules."""

from pattern_detector.adapters.outbound.parsers.native_haskell_parser_adapter import NativeHaskellParserAdapter
from pattern_detector.domain.rules.async_concurrent_flow_rule import AsyncConcurrentFlowRule
from pattern_detector.domain.rules.chan_mvar_mailbox_rule import ChanMvarMailboxRule
from pattern_detector.domain.rules.deriving_strategies_rule import DerivingStrategiesRule
from pattern_detector.domain.rules.free_monad_interpreter_rule import FreeMonadInterpreterRule
from pattern_detector.domain.rules.gadts_type_safe_ast_rule import GadtsTypeSafeAstRule
from pattern_detector.domain.rules.lazy_space_leak_risk_rule import LazySpaceLeakRiskRule
from pattern_detector.domain.rules.lens_prism_optics_rule import LensPrismOpticsRule
from pattern_detector.domain.rules.monad_transformer_stack_rule import MonadTransformerStackRule
from pattern_detector.domain.rules.newtype_strong_typing_rule import NewtypeStrongTypingRule
from pattern_detector.domain.rules.reader_t_design_pattern_rule import ReaderTDesignPatternRule
from pattern_detector.domain.rules.stm_transactional_memory_rule import StmTransactionalMemoryRule
from pattern_detector.domain.rules.stream_processing_pipeline_rule import StreamProcessingPipelineRule
from pattern_detector.domain.rules.tagless_final_style_rule import TaglessFinalStyleRule
from pattern_detector.domain.rules.typeclass_adapter_rule import TypeclassAdapterRule
from pattern_detector.domain.rules.unchecked_bottom_error_rule import UncheckedBottomErrorRule
from pattern_detector.domain.rules.unchecked_from_just_rule import UncheckedFromJustRule
from pattern_detector.domain.value_objects import PatternType



def test_detect_typeclass_gadts_and_reader_t():
    source = """
module App.Service where

import Control.Monad.Reader
import Control.Concurrent.STM

newtype Age = Age Int
newtype Name = Name String

data Ast a where
  Lit :: Int -> Ast Int

class Transport t where
  send :: t -> String -> IO ()

type AppM a = ReaderT Env IO a

runTransfer :: TVar Int -> TVar Int -> Int -> IO ()
runTransfer fromVar toVar amount = atomically $ do
  fromBal <- readTVar fromVar
  writeTVar fromVar (fromBal - amount)
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"App/Service.hs": source})

    # 1. Typeclass
    tc_rule = TypeclassAdapterRule()
    tc_dets = tc_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.TYPECLASS_ADAPTER for d in tc_dets)

    # 2. GADT
    gadt_rule = GadtsTypeSafeAstRule()
    gadt_dets = gadt_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.GADTS_TYPE_SAFE_AST for d in gadt_dets)

    # 3. Newtypes
    newtype_rule = NewtypeStrongTypingRule()
    newtype_dets = newtype_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.NEWTYPE_STRONG_TYPING for d in newtype_dets)

    # 4. ReaderT
    reader_rule = ReaderTDesignPatternRule()
    reader_dets = reader_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.READER_T_DESIGN_PATTERN for d in reader_dets)

    # 5. STM
    stm_rule = StmTransactionalMemoryRule()
    stm_dets = stm_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.STM_TRANSACTIONAL_MEMORY for d in stm_dets)


def test_detect_safety_and_space_leak_smells():
    source = """
module Unsafe.Module where

import Data.Maybe (fromJust)

badFunction :: [Int] -> Int
badFunction xs =
  if null xs
    then error "Empty list!"
    else fromJust (lookup 1 [(1, 42)])

leakFunction :: [Int] -> Int
leakFunction list = foldl (+) 0 list
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Unsafe/Module.hs": source})

    # Bottom
    bottom_rule = UncheckedBottomErrorRule()
    bottom_dets = bottom_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.UNCHECKED_BOTTOM_ERROR for d in bottom_dets)

    # fromJust
    from_just_rule = UncheckedFromJustRule()
    from_just_dets = from_just_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.UNCHECKED_FROM_JUST for d in from_just_dets)

    # Lazy space leak
    leak_rule = LazySpaceLeakRiskRule()
    leak_dets = leak_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.LAZY_SPACE_LEAK_RISK for d in leak_dets)


def test_detect_monad_transformers_free_monad_optics_and_streams():
    source = """
module Enterprise.Architecture where

import Control.Monad.Reader
import Control.Monad.Except
import Control.Monad.State.Strict
import Control.Monad.Free
import Control.Lens
import Control.Concurrent.Async
import Control.Concurrent.STM.TQueue
import Data.Conduit
import qualified Data.Conduit.List as CL

data StorageF next = Save String next | Load (String -> next)
type StorageDSL = Free StorageF

type AppStack a = ExceptT String (ReaderT Env IO) a

data User = User { _name :: String, _age :: Int }
makeLenses ''User

processStream :: ConduitT Int Int IO ()
processStream = CL.map (+1) .| CL.filter (> 0)

workerQueue :: TQueue String -> IO ()
workerQueue queue = do
  (r1, r2) <- concurrently (pure 1) (pure 2)
  pure ()
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Enterprise/Architecture.hs": source})

    # Transformer stack
    stack_rule = MonadTransformerStackRule()
    stack_dets = stack_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.MONAD_TRANSFORMER_STACK for d in stack_dets)

    # Free monad
    free_rule = FreeMonadInterpreterRule()
    free_dets = free_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.FREE_MONAD_INTERPRETER for d in free_dets)

    # Optics
    lens_rule = LensPrismOpticsRule()
    lens_dets = lens_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.LENS_PRISM_OPTICS for d in lens_dets)

    # Streams
    stream_rule = StreamProcessingPipelineRule()
    stream_dets = stream_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.STREAM_PROCESSING_PIPELINE for d in stream_dets)

    # Async
    async_rule = AsyncConcurrentFlowRule()
    async_dets = async_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.ASYNC_CONCURRENT_FLOW for d in async_dets)

    # Mailbox
    mbox_rule = ChanMvarMailboxRule()
    mbox_dets = mbox_rule.detect(code_model)
    assert any(d.pattern_type == PatternType.CHAN_MVAR_MAILBOX for d in mbox_dets)
