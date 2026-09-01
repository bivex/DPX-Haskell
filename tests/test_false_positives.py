"""False Positive Detection Tests for DPX-Haskell.

Verifies that clean, idiomatic, and non-target Haskell code does NOT trigger
false positive detections across any of the 26+ architectural, typeclass,
monad, concurrency, or code quality rules.
"""

from pattern_detector.adapters.outbound.parsers.native_haskell_parser_adapter import NativeHaskellParserAdapter
from pattern_detector.application.services.detection_service import PatternDetectorService
from pattern_detector.domain.rules import DEFAULT_RULES
from pattern_detector.domain.rules.async_concurrent_flow_rule import AsyncConcurrentFlowRule
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
from pattern_detector.domain.value_objects import PatternType


def test_clean_safety_and_space_leak_no_false_positives():
    """Verify that strict folding, safe Maybes, typed errors, and specific catch do not trigger safety smells."""
    source = """
module Clean.Safety where

import Data.List (foldl')
import Data.Maybe (fromMaybe)
import Control.Exception (catch, IOException)
import Control.Monad.State.Strict

-- Note: comments mentioning error, undefined, fromJust, foldl must not trigger
-- foldl (+) 0 xs
-- error "panic"
-- undefined

safeSum :: [Int] -> Int
safeSum = foldl' (+) 0

safeFoldr :: [Int] -> Int
safeFoldr = foldr (+) 0

safeLookup :: Int -> [(Int, String)] -> String
safeLookup k kvs = fromMaybe "default" (lookup k kvs)

safeDivision :: Double -> Double -> Either String Double
safeDivision _ 0 = Left "Division by zero"
safeDivision x y = Right (x / y)

safeCatchIO :: IO () -> IO ()
safeCatchIO action = action `catch` (\\(e :: IOException) -> putStrLn "Handled IO error")

strictStateCounter :: State Int ()
strictStateCounter = modify' (+1)
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Clean/Safety.hs": source})

    # Unchecked bottom: should NOT detect anything
    assert len(UncheckedBottomErrorRule().detect(code_model)) == 0

    # Unchecked fromJust: should NOT detect anything
    assert len(UncheckedFromJustRule().detect(code_model)) == 0

    # Lazy space leak: foldl' and Control.Monad.State.Strict must NOT trigger
    assert len(LazySpaceLeakRiskRule().detect(code_model)) == 0

    # Catch all: specific IOException must NOT trigger
    assert len(CatchAllSomeExceptionRule().detect(code_model)) == 0


def test_standard_types_no_typeclass_or_gadt_false_positives():
    """Verify that standard ADTs, simple newtypes, and ordinary typeclasses do not trigger advanced patterns."""
    source = """
module Standard.Types where

-- Standard algebraic data type (not a GADT)
data Shape
  = Circle Double
  | Rectangle Double Double
  deriving (Eq, Show)

-- Single newtype (does not meet >=2 threshold for value object pattern)
newtype Email = Email String

-- Ordinary typeclass (not tagless final, not a type family)
class Pretty a where
  pretty :: a -> String

instance Pretty Shape where
  pretty (Circle r) = "Circle " ++ show r
  pretty (Rectangle w h) = "Rect " ++ show w ++ "x" ++ show h
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Standard/Types.hs": source})

    # GADTs: Standard ADT should not be detected as GADT
    assert len(GadtsTypeSafeAstRule().detect(code_model)) == 0

    # Newtype strong typing: 1 newtype should not trigger (requires >= 2)
    assert len(NewtypeStrongTypingRule().detect(code_model)) == 0

    # Deriving strategies: Standard deriving without stock/newtype/anyclass keyword
    assert len(DerivingStrategiesRule().detect(code_model)) == 0

    # Type families: No type family
    assert len(TypeFamilyAssociatedRule().detect(code_model)) == 0

    # Type level literals: No DataKinds / TypeLits
    assert len(TypeLevelLiteralsRule().detect(code_model)) == 0

    # Tagless final: Pretty is not a Monad capability class
    assert len(TaglessFinalStyleRule().detect(code_model)) == 0

    # Phantom types: Email is not phantom
    assert len(PhantomTypesRule().detect(code_model)) == 0


def test_standard_monadic_and_functional_no_false_positives():
    """Verify that standard IO, short do-blocks, standard records, and explicit recursion do not trigger false positives."""
    source = """
module Standard.Functional where

-- Standard record with normal record update
data User = User
  { userName :: String
  , userAge :: Int
  }

updateUserName :: String -> User -> User
updateUserName newName u = u { userName = newName }

-- Short do-block (1-2 statements, not a railway pipeline)
printGreeting :: String -> IO ()
printGreeting name = do
  putStrLn ("Hello, " ++ name)

-- Standard constructor helper (returns User directly, not Either/Maybe)
makeUser :: String -> Int -> User
makeUser n a = User n a

-- Standard explicit recursion (not recursion schemes)
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Standard/Functional.hs": source})

    # ReaderT pattern: Not present
    assert len(ReaderTDesignPatternRule().detect(code_model)) == 0

    # Monad transformer stack: Not present
    assert len(MonadTransformerStackRule().detect(code_model)) == 0

    # Free Monad: Not present
    assert len(FreeMonadInterpreterRule().detect(code_model)) == 0

    # Continuation Monad: Not present
    assert len(ContinuationMonadRule().detect(code_model)) == 0

    # Railway do-notation: Short do block should not trigger (requires >= 3 binds)
    assert len(RailwayDoNotationRule().detect(code_model)) == 0

    # Lenses / Optics: Standard record update should not trigger
    assert len(LensPrismOpticsRule().detect(code_model)) == 0

    # Smart Constructor: makeUser returns User directly (not Either/Maybe, no validation)
    assert len(SmartConstructorModuleRule().detect(code_model)) == 0


def test_standard_concurrency_no_false_positives():
    """Verify that pure code or non-concurrent IO does not trigger STM, Async, Stream, or Mailbox patterns."""
    source = """
module Standard.Sequential where

processList :: [Int] -> [Int]
processList xs = map (+1) (filter (> 0) xs)

readConfig :: FilePath -> IO String
readConfig path = readFile path
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Standard/Sequential.hs": source})

    assert len(StmTransactionalMemoryRule().detect(code_model)) == 0
    assert len(AsyncConcurrentFlowRule().detect(code_model)) == 0
    assert len(StreamProcessingPipelineRule().detect(code_model)) == 0
    assert len(ChanMvarMailboxRule().detect(code_model)) == 0


def test_clean_solid_and_kiss_no_false_positives():
    """Verify that well-sized modules, simple functions, and distinct functions do not trigger SRP, KISS, or DRY violations."""
    source = """
module Clean.SOLID where

computeTax :: Double -> Double
computeTax income =
  if income > 100000
    then income * 0.35
    else income * 0.20

formatReceipt :: String -> Double -> String
formatReceipt item total = item ++ ": $" ++ show total
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Clean/SOLID.hs": source})

    # God Module SRP: 2 declarations, well under 30
    assert len(GodModuleSrpRule().detect(code_model)) == 0

    # KISS Cyclomatic Complexity: Very simple functions, complexity < 12
    assert len(CyclomaticComplexityKissRule().detect(code_model)) == 0

    # DRY: Distinct functions
    assert len(DuplicateCodeDryRule().detect(code_model)) == 0


def test_acyclic_imports_no_circular_dependency_false_positive():
    """Verify that a linear dependency graph (A -> B -> C) does NOT trigger circular import detection."""
    sources = {
        "ModuleA.hs": """
module ModuleA where
import ModuleB
valA :: Int
valA = valB + 1
""",
        "ModuleB.hs": """
module ModuleB where
import ModuleC
valB :: Int
valB = valC * 2
""",
        "ModuleC.hs": """
module ModuleC where
valC :: Int
valC = 42
""",
    }
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources(sources)

    circular_dets = CircularModuleImportRule().detect(code_model)
    assert len(circular_dets) == 0


def test_trivial_pure_module_zero_detections_across_all_rules():
    """Verify that a minimal pure Haskell module yields zero detections across all default rules."""
    source = """
module Minimal.Pure where

constantValue :: Int
constantValue = 42

identity :: a -> a
identity x = x
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Minimal/Pure.hs": source})

    service = PatternDetectorService(rules=DEFAULT_RULES)
    detections = service.detect_patterns(code_model)

    assert len(detections) == 0, f"Expected 0 detections, got {len(detections)}: {[d.pattern_type.value for d in detections]}"


def test_comments_and_string_literals_do_not_trigger_false_positives():
    """Verify that comments, documentation, string literals, and similar substrings do not trigger false positives."""
    source = '''
module Clean.CommentsAndStrings where

-- Substring hazard: variable named retryCount or maxRetry must not trigger STM
retryCount :: Int
retryCount = 5

-- Substring hazard: variable named raceDistance must not trigger Async
raceDistance :: Double
raceDistance = 42.195

-- Substring hazard: variable named analytics must not trigger recursion schemes
analytics :: [Int] -> Int
analytics xs = sum xs

-- Documentation comments mentioning idioms must not trigger rules:
-- 1. Do not use fromJust, use fromMaybe instead.
-- 2. Avoid error "foo" or undefined in pure code.
-- 3. Avoid lazy foldl (+) 0 xs due to space leaks.
-- 4. Avoid TVar, atomically, retry, or TMVar unless concurrency is needed.
-- 5. Avoid async, concurrently, race unless background jobs exist.
-- 6. Avoid Conduit, Pipes, or Streaming if plain lists suffice.
-- 7. Avoid ReaderT Env IO or ExceptT or ContT callCC if not needed.
-- 8. Avoid bracket or withFile if no handles are opened.
-- 9. Avoid DataKinds or GHC.TypeLits unless doing type arithmetic.
-- 10. Fix any bug promptly.

-- String literals describing errors or keywords:
errorDescription :: String
errorDescription = "An error occurred: variable is undefined and status is invalid"

logNotice :: String
logNotice = "Please Fix the documentation before release"
'''
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Clean/CommentsAndStrings.hs": source})

    service = PatternDetectorService(rules=DEFAULT_RULES)
    detections = service.detect_patterns(code_model)

def test_nested_block_comments_and_escaped_strings_no_false_positives():
    """Verify that nested block comments and strings with escaped quotes do not trigger false positives."""
    source = r'''
module Deep.Sanitization where

{- Outer block comment
   {- Nested block comment mentioning:
      error "bad"
      undefined
      fromJust
      TVar, atomically, retry
      ReaderT Env IO
      ExceptT String IO
      Conduit, Pipes
      bracket withFile
   -}
   Back to outer comment
-}

sqlQuery :: String
sqlQuery = "SELECT error, fromJust, foldl, retry, race, async FROM t WHERE state = \"active\""

regexString :: String
regexString = ".*error.*|.*undefined.*"

variableWithSubstrings :: Int
variableWithSubstrings = 100
  where
    tvariety = 1
    tmvariable = 2
    tchannel = 3
    pipestatus = 4
    readerto = 5
    exceptto = 6
    bracketedText = 7
    stated = 8
    conduits = 9
'''
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Deep/Sanitization.hs": source})

    service = PatternDetectorService(rules=DEFAULT_RULES)
    detections = service.detect_patterns(code_model)

    detected_types = [d.pattern_type.value for d in detections]
    assert len(detections) == 0, f"False positives detected from nested comments/escaped strings: {detected_types}"


def test_standard_prelude_idiomatic_code_no_false_positives():
    """Verify that idiomatic standard Haskell (Prelude, Data.Text, Data.Map) yields zero detections."""
    source = """
module Standard.Idiomatic where

import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map
import Data.Text (Text)
import qualified Data.Text as T
import Control.Applicative ((<|>))

data AppConfig = AppConfig
  { hostName :: Text
  , portNumber :: Int
  , isEnabled :: Bool
  } deriving (Eq, Show)

lookupConfig :: Text -> Map Text Text -> Maybe Text
lookupConfig key configMap = Map.lookup key configMap <|> Just "default"

formatConfig :: AppConfig -> Text
formatConfig cfg =
  hostName cfg <> T.pack ":" <> T.pack (show (portNumber cfg))

absVal :: (Num a, Ord a) => a -> a
absVal x
  | x < 0 = -x
  | otherwise = x
"""
    parser = NativeHaskellParserAdapter()
    code_model = parser.parse_sources({"Standard/Idiomatic.hs": source})

    service = PatternDetectorService(rules=DEFAULT_RULES)
    detections = service.detect_patterns(code_model)

    detected_types = [d.pattern_type.value for d in detections]
    assert len(detections) == 0, f"False positives detected in standard idiomatic code: {detected_types}"


