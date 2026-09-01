"""Tests for ANTLR4 Haskell Grammar and Parser Adapter."""

from pattern_detector.adapters.outbound.parsers.antlr.antlr_haskell_parser_adapter import AntlrHaskellParserAdapter
from pattern_detector.application.services.detection_service import PatternDetectorService
from pattern_detector.bootstrap.container import create_container
from pattern_detector.domain.rules import DEFAULT_RULES
from pattern_detector.domain.value_objects import PatternType


def test_antlr_parser_parses_haskell_syntax():
    """Verify that AntlrHaskellParserAdapter successfully parses Haskell AST constructs."""
    source = """{-# LANGUAGE GADTs, DerivingStrategies, ExplicitForAll #-}
module Data.Container where

import Control.Monad.Reader
import Control.Concurrent.STM

newtype ItemId = ItemId Int deriving stock (Eq, Show)
newtype ItemName = ItemName String deriving stock (Eq, Show)

data Expr a where
  LitInt  :: Int -> Expr Int
  LitBool :: Bool -> Expr Bool

class Monad m => MonadStorage m where
  saveItem :: ItemId -> ItemName -> m ()
  getItem  :: ItemId -> m (Maybe ItemName)

instance MonadStorage IO where
  saveItem _ _ = pure ()
  getItem _ = pure Nothing

calculateTotal :: Int -> Int -> Int
calculateTotal price qty = price * qty
"""
    parser = AntlrHaskellParserAdapter()
    code_model = parser.parse_sources({"Data/Container.hs": source})

    assert "Data.Container" in code_model.modules
    module = code_model.modules["Data.Container"]

    # Pragmas
    assert "GADTs" in module.pragmas
    assert "DerivingStrategies" in module.pragmas

    # Imports
    assert "Control.Monad.Reader" in module.imports
    assert "Control.Concurrent.STM" in module.imports

    # Types
    assert "ItemId" in module.types
    assert module.types["ItemId"].is_newtype is True
    assert "stock" in module.types["ItemId"].deriving_strategies

    assert "Expr" in module.types
    assert module.types["Expr"].is_gadt is True

    # Typeclasses & Instances
    assert "MonadStorage" in module.typeclasses
    assert len(module.instances) >= 1
    assert module.instances[0].class_name == "MonadStorage"

    # Functions
    assert "calculateTotal" in module.functions
    assert module.functions["calculateTotal"].type_signature != ""


def test_antlr_parser_rule_detection_parity():
    """Verify that pattern rules detect patterns correctly on ANTLR parsed code model."""
    source = """{-# LANGUAGE GADTs, DerivingStrategies #-}
module BankApp.Service where

import Control.Monad.Reader
import Control.Concurrent.STM

newtype AccountId = AccountId String deriving stock (Eq, Show)
newtype Balance = Balance Double deriving stock (Eq, Show)

data Transaction a where
  Deposit  :: Balance -> Transaction Balance
  Withdraw :: Balance -> Transaction (Either String Balance)

type AppM a = ReaderT Env IO a

transferMoney :: TVar Balance -> TVar Balance -> Balance -> IO ()
transferMoney fromAcc toAcc amount = atomically $ do
  b <- readTVar fromAcc
  writeTVar fromAcc b
"""
    parser = AntlrHaskellParserAdapter()
    code_model = parser.parse_sources({"BankApp/Service.hs": source})

    service = PatternDetectorService(rules=DEFAULT_RULES)
    detections = service.detect_patterns(code_model)

    detected_types = {d.pattern_type for d in detections}

    assert PatternType.GADTS_TYPE_SAFE_AST in detected_types
    assert PatternType.NEWTYPE_STRONG_TYPING in detected_types
    assert PatternType.DERIVING_STRATEGIES in detected_types
    assert PatternType.READER_T_DESIGN_PATTERN in detected_types
    assert PatternType.STM_TRANSACTIONAL_MEMORY in detected_types


def test_container_default_parser_is_antlr():
    """Verify that Container defaults to AntlrHaskellParserAdapter."""
    container = create_container()
    parser = container.get_parser()
    assert isinstance(parser, AntlrHaskellParserAdapter)


def test_container_with_native_parser_option():
    """Verify that Container with parser_type='native' provides NativeHaskellParserAdapter."""
    from pattern_detector.adapters.outbound.parsers.native_haskell_parser_adapter import NativeHaskellParserAdapter

    container = create_container(parser_type="native")
    parser = container.get_parser()
    assert isinstance(parser, NativeHaskellParserAdapter)

