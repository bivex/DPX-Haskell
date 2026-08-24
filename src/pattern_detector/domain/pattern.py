"""Pattern metadata, catalog definitions, and architectural descriptions for Haskell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternCatalogEntry:
    """Catalog entry describing a Haskell pattern, typeclass idiom, monad transformer, or rule."""

    pattern_type: PatternType
    category: PatternCategory
    name: str
    description: str
    idiomatic_example: str


PATTERN_CATALOG: Mapping[PatternType, PatternCatalogEntry] = {
    # Typeclasses & Polymorphism (6)
    PatternType.TYPECLASS_ADAPTER: PatternCatalogEntry(
        pattern_type=PatternType.TYPECLASS_ADAPTER,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Typeclass Interface Adapter",
        description="Ad-hoc polymorphism via Haskell typeclasses (`class Storage s where ...`) enabling decoupled adapter implementations across data types.",
        idiomatic_example="class Transport t where\n  sendMsg :: t -> Message -> IO ()\n  recvMsg :: t -> IO Message",
    ),
    PatternType.TYPE_FAMILY_ASSOCIATED: PatternCatalogEntry(
        pattern_type=PatternType.TYPE_FAMILY_ASSOCIATED,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Type Families & Associated Types",
        description="Type-level computation and indexed associated types (`type family Key a :: *`) computing output types directly from input type parameters.",
        idiomatic_example="class Container c where\n  type Element c\n  insert :: Element c -> c -> c",
    ),
    PatternType.EXISTENTIAL_QUANTIFICATION: PatternCatalogEntry(
        pattern_type=PatternType.EXISTENTIAL_QUANTIFICATION,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Existential Heterogeneous Wrapper",
        description="Existential type quantification (`data AnyHandler = forall h. Handler h => AnyHandler h`) for storing heterogeneous types satisfying a typeclass.",
        idiomatic_example="data AnyWidget = forall w. Widget w => AnyWidget w\nrenderAll :: [AnyWidget] -> IO ()",
    ),
    PatternType.GADTS_TYPE_SAFE_AST: PatternCatalogEntry(
        pattern_type=PatternType.GADTS_TYPE_SAFE_AST,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="GADT Type-Safe AST Evaluator",
        description="Generalized Algebraic Data Types (`data Expr a where I :: Int -> Expr Int`) ensuring compile-time type preservation during interpretation.",
        idiomatic_example="data Expr a where\n  I :: Int -> Expr Int\n  Add :: Expr Int -> Expr Int -> Expr Int\neval :: Expr a -> a",
    ),
    PatternType.NEWTYPE_STRONG_TYPING: PatternCatalogEntry(
        pattern_type=PatternType.NEWTYPE_STRONG_TYPING,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Newtype Domain Value Object",
        description="Zero-cost runtime strong typing (`newtype UserId = UserId Text`) preventing accidental parameter transposition bugs at zero runtime penalty.",
        idiomatic_example="newtype Email = Email { unEmail :: Text }\nnewtype UserId = UserId { unUserId :: UUID }",
    ),
    PatternType.DERIVING_STRATEGIES: PatternCatalogEntry(
        pattern_type=PatternType.DERIVING_STRATEGIES,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Deriving Strategies Specification",
        description="Explicit deriving strategies (`deriving stock`, `deriving newtype`, `deriving anyclass`) preventing ambiguous typeclass instance generation.",
        idiomatic_example="newtype Meter = Meter Double\n  deriving stock (Show, Eq)\n  deriving newtype (Num, Real)",
    ),

    # Functional Architecture, Monads & Transformers (8)
    PatternType.READER_T_DESIGN_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.READER_T_DESIGN_PATTERN,
        category=PatternCategory.MONAD_ARCHITECTURE,
        name="The ReaderT Design Pattern",
        description="Standard production Haskell application architecture (`ReaderT Env IO a` or `newtype App a = App (ReaderT Env IO a)`) for dependency injection.",
        idiomatic_example="type AppM = ReaderT AppEnv IO\nrunApp :: AppEnv -> AppM a -> IO a\nrunApp env m = runReaderT m env",
    ),
    PatternType.MONAD_TRANSFORMER_STACK: PatternCatalogEntry(
        pattern_type=PatternType.MONAD_TRANSFORMER_STACK,
        category=PatternCategory.MONAD_ARCHITECTURE,
        name="Monad Transformer Stack",
        description="Layered monad transformers (`ExceptT AppError (StateT AppState (ReaderT Env IO)) a`) composing distinct computational capabilities.",
        idiomatic_example="type AppStack a = ExceptT ServiceError (ReaderT Config IO) a",
    ),
    PatternType.FREE_MONAD_INTERPRETER: PatternCatalogEntry(
        pattern_type=PatternType.FREE_MONAD_INTERPRETER,
        category=PatternCategory.MONAD_ARCHITECTURE,
        name="Free Monad DSL Interpreter",
        description="Decoupling program description from interpretation via Free Monads (`Free DSLF a`), enabling pure testing, logging, and multiple backends.",
        idiomatic_example="data StorageF next = Save Key Value next | Load Key (Value -> next)\ntype StorageDSL = Free StorageF",
    ),
    PatternType.TAGLESS_FINAL_STYLE: PatternCatalogEntry(
        pattern_type=PatternType.TAGLESS_FINAL_STYLE,
        category=PatternCategory.MONAD_ARCHITECTURE,
        name="Tagless Final Capability Style",
        description="MTL / Tagless Final capability classes (`class MonadDB m where fetchUser :: UserId -> m User`) for extensible, mockable dependency contracts.",
        idiomatic_example="class Monad m => MonadDB m where\n  queryUser :: UserId -> m (Maybe User)\n  saveUser  :: User -> m ()",
    ),
    PatternType.RAILWAY_DO_NOTATION: PatternCatalogEntry(
        pattern_type=PatternType.RAILWAY_DO_NOTATION,
        category=PatternCategory.FUNCTIONAL_IDIOM,
        name="Railway Do-Notation Flow",
        description="Monadic railway composition in `do` blocks chaining `Either`/`ExceptT` or Applicative `<$>` / `<*>` without manual error branching.",
        idiomatic_example="registerUser raw = do\n  user <- validateUser raw\n  token <- authenticate user\n  pure token",
    ),
    PatternType.LENS_PRISM_OPTICS: PatternCatalogEntry(
        pattern_type=PatternType.LENS_PRISM_OPTICS,
        category=PatternCategory.OPTICS_LENSES,
        name="Functional Optics (Lenses & Prisms)",
        description="Composable lenses, prisms, and traversals (`makeLenses`, `(^.)`, `(.~)`, `preview`) for deep immutable record inspection and modification.",
        idiomatic_example="user & address . street . number .~ 42\nlet currentCity = user ^. address . city",
    ),
    PatternType.CONTINUATION_MONAD: PatternCatalogEntry(
        pattern_type=PatternType.CONTINUATION_MONAD,
        category=PatternCategory.MONAD_ARCHITECTURE,
        name="Continuation Monad (ContT/callCC)",
        description="Explicit continuation-passing transformations via `ContT` and `callCC` for advanced control flow, coroutines, and early exits.",
        idiomatic_example="evalCont = callCC (\\exit -> do\n  when invalid (exit False)\n  pure True)",
    ),
    PatternType.SMART_CONSTRUCTOR_MODULE: PatternCatalogEntry(
        pattern_type=PatternType.SMART_CONSTRUCTOR_MODULE,
        category=PatternCategory.FUNCTIONAL_IDIOM,
        name="Smart Constructor Encapsulation",
        description="Opaque data export with smart constructor validation function (`mkAge :: Int -> Either Error Age`) guaranteeing internal domain invariants.",
        idiomatic_example="module Age (Age, mkAge, unAge) where\nnewtype Age = Age Int\nmkAge n = if n >= 0 then Right (Age n) else Left \"Negative age\"",
    ),
    PatternType.RECURSION_SCHEMES: PatternCatalogEntry(
        pattern_type=PatternType.RECURSION_SCHEMES,
        category=PatternCategory.FUNCTIONAL_IDIOM,
        name="Recursion Schemes (Catamorphisms)",
        description="Abstracting recursive data structure traversals into pure morphisms (`cata`, `ana`, `hylo`, `Data.Functor.Foldable`) eliminating explicit recursion boilerplate.",
        idiomatic_example="evalAST = cata (\\case LitF n -> n; AddF a b -> a + b)",
    ),
    PatternType.BRACKET_RESOURCE_MANAGEMENT: PatternCatalogEntry(
        pattern_type=PatternType.BRACKET_RESOURCE_MANAGEMENT,
        category=PatternCategory.RESILIENCE,
        name="Bracket Resource Management (RAII)",
        description="Deterministic acquire-release resource life-cycle management (`bracket acquire release inside`) guaranteeing cleanup even under asynchronous thread interruption.",
        idiomatic_example="withHandle h = bracket (openFile h ReadMode) hClose (\\handle -> ...)",
    ),
    PatternType.TYPE_LEVEL_LITERALS: PatternCatalogEntry(
        pattern_type=PatternType.TYPE_LEVEL_LITERALS,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Type-Level Computation (DataKinds/TypeLits)",
        description="Compile-time numeric and string type-level computing (`KnownNat n`, `KnownSymbol s`, `DataKinds`) ensuring dimensional and protocol correctness.",
        idiomatic_example="data Vector (n :: Nat) a = Vector [a]\naddVec :: KnownNat n => Vector n Double -> Vector n Double -> Vector n Double",
    ),
    PatternType.PHANTOM_TYPES: PatternCatalogEntry(
        pattern_type=PatternType.PHANTOM_TYPES,
        category=PatternCategory.TYPECLASS_SYSTEM,
        name="Phantom Types Invariant Verification",
        description="Parameterized types carrying phantom type variables (`newtype Query state = Query Text`) verifying state machine transitions at compile time.",
        idiomatic_example="newtype Form state = Form Text\nvalidate :: Form Unvalidated -> Maybe (Form Validated)",
    ),


    # Concurrency, Parallelism & Streams (4)
    PatternType.STM_TRANSACTIONAL_MEMORY: PatternCatalogEntry(
        pattern_type=PatternType.STM_TRANSACTIONAL_MEMORY,
        category=PatternCategory.CONCURRENCY_STM,
        name="Software Transactional Memory (STM)",
        description="Composable, lock-free, deadlock-free transactional concurrency via `TVar`, `TMVar`, `atomically`, `retry`, and `orElse`.",
        idiomatic_example="transfer fromVar toVar amount = atomically $ do\n  fromBal <- readTVar fromVar\n  if fromBal < amount then retry else ...",
    ),
    PatternType.ASYNC_CONCURRENT_FLOW: PatternCatalogEntry(
        pattern_type=PatternType.ASYNC_CONCURRENT_FLOW,
        category=PatternCategory.CONCURRENCY_STM,
        name="Structured Async Concurrency",
        description="Structured concurrent tasks (`async`, `wait`, `concurrently`, `race`) with automatic cancellation and exception propagation.",
        idiomatic_example="(res1, res2) <- concurrently (fetchRemoteA url1) (fetchRemoteB url2)",
    ),
    PatternType.STREAM_PROCESSING_PIPELINE: PatternCatalogEntry(
        pattern_type=PatternType.STREAM_PROCESSING_PIPELINE,
        category=PatternCategory.FUNCTIONAL_IDIOM,
        name="Stream Processing Pipeline (Conduit/Pipes)",
        description="Constant-memory streaming pipelines (`Conduit`, `Pipes`, `Streaming`) with deterministic resource management and backpressure.",
        idiomatic_example="sourceFile \"input.txt\" .| C.lines .| C.filter isValid .| sinkFile \"output.txt\"",
    ),
    PatternType.CHAN_MVAR_MAILBOX: PatternCatalogEntry(
        pattern_type=PatternType.CHAN_MVAR_MAILBOX,
        category=PatternCategory.CONCURRENCY_STM,
        name="Actor Mailbox Channel (Chan/TQueue)",
        description="Concurrent actor-style message queues using `TQueue`, `TChan`, or `MVar` synchronizing concurrent worker pools.",
        idiomatic_example="workerLoop queue = do\n  msg <- atomically $ readTQueue queue\n  process msg\n  workerLoop queue",
    ),

    # Type Safety, Space Leaks, Clean Code & SOLID (8)
    PatternType.UNCHECKED_BOTTOM_ERROR: PatternCatalogEntry(
        pattern_type=PatternType.UNCHECKED_BOTTOM_ERROR,
        category=PatternCategory.TYPE_SAFETY,
        name="Unchecked Bottom / Panic (error/undefined)",
        description="Introducing runtime bottom crashes (`error`, `undefined`, `head`, `tail`) instead of typed total handling (`Maybe`/`Either`).",
        idiomatic_example="Use `Maybe` or `Either` instead of throwing `error \"bad state\"`.",
    ),
    PatternType.UNCHECKED_FROM_JUST: PatternCatalogEntry(
        pattern_type=PatternType.UNCHECKED_FROM_JUST,
        category=PatternCategory.TYPE_SAFETY,
        name="Unsafe fromJust Partial Function",
        description="Calling `fromJust` which throws an uncatchable exception when encountering `Nothing`; use `maybe`, `fromMaybe`, or pattern match.",
        idiomatic_example="Use `fromMaybe defaultValue opt` or `case opt of Just x -> ...` instead of `fromJust`.",
    ),
    PatternType.LAZY_SPACE_LEAK_RISK: PatternCatalogEntry(
        pattern_type=PatternType.LAZY_SPACE_LEAK_RISK,
        category=PatternCategory.RESILIENCE,
        name="Lazy Space Leak Hazard (foldl/lazy State)",
        description="Unforced thunk accumulation in lazy operations (`foldl` instead of `foldl'`, lazy `Control.Monad.State` instead of strict `State.Strict`).",
        idiomatic_example="Use `Data.List.foldl'` and strict monads `Control.Monad.State.Strict` to avoid OOM space leaks.",
    ),
    PatternType.CATCH_ALL_SOME_EXCEPTION: PatternCatalogEntry(
        pattern_type=PatternType.CATCH_ALL_SOME_EXCEPTION,
        category=PatternCategory.RESILIENCE,
        name="Catch-All SomeException Anti-Pattern",
        description="Catching `SomeException` without rethrowing async exceptions (`ThreadKilled`, `UserInterrupt`), breaking graceful shutdown.",
        idiomatic_example="Catch specific exception types or use `safe-exceptions` / `unliftio`.",
    ),
    PatternType.GOD_MODULE_SRP: PatternCatalogEntry(
        pattern_type=PatternType.GOD_MODULE_SRP,
        category=PatternCategory.PRINCIPLE,
        name="Single Responsibility (God Module)",
        description="Monolithic Haskell module defining excessive functions, instances, and types (≥30 declarations or ≥800 LOC).",
        idiomatic_example="Split large modules into focused domain components.",
    ),
    PatternType.CYCLOMATIC_COMPLEXITY_KISS: PatternCatalogEntry(
        pattern_type=PatternType.CYCLOMATIC_COMPLEXITY_KISS,
        category=PatternCategory.PRINCIPLE,
        name="KISS Complexity (Pattern Matching)",
        description="Function with excessive pattern matches, guards, or deep nested `case ... of` branches (≥12 branches).",
        idiomatic_example="Decompose complex case branches into smaller pure helper functions.",
    ),
    PatternType.DUPLICATE_CODE_DRY: PatternCatalogEntry(
        pattern_type=PatternType.DUPLICATE_CODE_DRY,
        category=PatternCategory.PRINCIPLE,
        name="Don't Repeat Yourself (DRY)",
        description="Duplicated function implementations across modules.",
        idiomatic_example="Extract shared logic into a shared module or generalized typeclass.",
    ),
    PatternType.CIRCULAR_MODULE_IMPORT: PatternCatalogEntry(
        pattern_type=PatternType.CIRCULAR_MODULE_IMPORT,
        category=PatternCategory.PRINCIPLE,
        name="Circular Module Import Cycle",
        description="Cyclic cross-module `import` dependencies requiring `.hs-boot` files.",
        idiomatic_example="Decouple modules using abstract typeclasses or domain entity modules.",
    ),
}
