# 🔷 DPX-Haskell: Static Architecture, Typeclass Idiom, Monad Transformer & Safety Analyzer for Haskell

[![CI](https://github.com/bivex/DPX-Haskell/actions/workflows/ci.yml/badge.svg)](https://github.com/bivex/DPX-Haskell/actions)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20Ports%20%26%20Adapters-purple.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
[![GHC: 9.2 - 9.10+](https://img.shields.io/badge/GHC-9.2%20--%209.10+-orange.svg)](https://www.haskell.org/ghc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**DPX-Haskell** is a high-performance, deterministic static architecture and design pattern analysis engine built specifically for **Haskell (GHC 9.2 - 9.10+ / Haskell2010 / Haskell2021 / Cabal / Stack)**.

Designed with **Hexagonal Architecture (Ports & Adapters)** and **Domain-Driven Design (DDD)**, DPX-Haskell audits Haskell codebases for **26 architectural patterns, typeclass idioms, monad transformer stacks, STM concurrency, and space leak hazards**.

---

## 🚀 Key Features

* **⚡ Ultra-Fast Layout-Aware Parser:** Parses pure Haskell files, language pragmas (`{-# LANGUAGE #-}`), GADTs, type families, typeclasses, and monad pipelines in microseconds.
* **🛡️ 26 Specialized Rules:** Comprehensive static pattern detection spanning Typeclass Systems, Monad Architecture, Functional Optics, STM Concurrency, and Space Leak Hazards.
* **📁 Directory Exclusions (`-e / --exclude`):** Prunes `.stack-work`, `dist-newstyle`, `test`, `benchmarks` on the fly.
* **📊 Multi-Format Reporting:** Instant interactive **Dark HTML Dashboards**, **OASIS SARIF v2.1.0** (GitHub Code Scanning), **JSON**, **Markdown**, and **LLM XML prompt context**.

---

## 🎯 26 Supported Haskell Design Patterns & Safety Rules

```
                      🔷 Haskell Architecture & Pattern Matrix
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Category                   ┃ Pattern Identifier     ┃ Haskell Idiom / Technique                      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. Typeclasses &           │ TYPECLASS_ADAPTER      │ class Transport t where ...                    │
│    Polymorphism (6)        │ TYPE_FAMILY_ASSOCIATED │ type family Element c :: *                     │
│                            │ EXISTENTIAL_QUANT      │ data AnyWidget = forall w. Widget w => Any w   │
│                            │ GADTS_TYPE_SAFE_AST    │ data Expr a where I :: Int -> Expr Int         │
│                            │ NEWTYPE_STRONG_TYPING  │ newtype UserId = UserId Text                   │
│                            │ DERIVING_STRATEGIES    │ deriving stock / newtype / anyclass            │
├────────────────────────────┼────────────────────────┼────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┤
│ 2. Functional Architecture │ READER_T_DESIGN_PAT    │ ReaderT Env IO a / newtype App = App (ReaderT) │
│    & Monad Stacks (8)      │ MONAD_TRANSFORMER_STCK │ ExceptT AppError (ReaderT Env IO) a            │
│                            │ FREE_MONAD_INTERPRETER │ Free DSLF a / liftF / iterM                    │
│                            │ TAGLESS_FINAL_STYLE    │ class Monad m => MonadDB m where ...           │
│                            │ RAILWAY_DO_NOTATION    │ do notation / >>= / Applicative (<$>, <*>)     │
│                            │ LENS_PRISM_OPTICS      │ makeLenses / (^.) / (.~) / preview / %~        │
│                            │ CONTINUATION_MONAD     │ ContT / callCC / runCont                       │
│                            │ SMART_CONSTRUCTOR_MOD  │ mkType :: ... -> Either Error Type             │
├────────────────────────────┼────────────────────────┼────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┤
│ 3. Concurrency, Streams    │ STM_TRANSACTIONAL_MEM  │ TVar / atomically / retry / orElse             │
│    & Parallelism (4)       │ ASYNC_CONCURRENT_FLOW  │ async / concurrently / race / wait             │
│                            │ STREAM_PROCESSING_PIPE │ Conduit / Pipes / Streaming (.|)               │
│                            │ CHAN_MVAR_MAILBOX      │ TQueue / TChan / Chan / MVar                   │
├────────────────────────────┼────────────────────────┼────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┤
│ 4. Type Safety, Space      │ UNCHECKED_BOTTOM_ERROR │ error "msg" / undefined / head []              │
│    Leaks & Quality (8)     │ UNCHECKED_FROM_JUST    │ fromJust on Nothing (unsafe partial call)      │
│                            │ LAZY_SPACE_LEAK_RISK   │ foldl (unforced thunk) / lazy State monad      │
│                            │ CATCH_ALL_SOME_EXCEPT  │ catch (_ :: SomeException) swallowing kills    │
│                            │ GOD_MODULE_SRP         │ Single Responsibility Violation (≥30 decls)    │
│                            │ CYCLOMATIC_COMPLEX_KISS│ Pattern matching / Case branches (≥12)         │
│                            │ DUPLICATE_CODE_DRY     │ Duplicate function logic across modules        │
│                            │ CIRCULAR_MODULE_IMPORT │ Circular import dependency cycles              │
└━━━━━━━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┘
```

---

## ⚡ Performance Benchmarks on Real-World Haskell Repositories

| Open-Source Project | Files Scanned | Architectural Detections | Scan Time (s) | Typeclasses | Monad Stacks | STM / Async | Safety / Leaks |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [**aeson**](https://github.com/haskell/aeson) *(JSON engine)* | 129 | 161 | **0.312s** | 53 | 2 | 0 | 30 |
| [**wai**](https://github.com/yesodweb/wai) *(Web server engine)* | 204 | 166 | **0.295s** | 2 | 5 | 23 | 16 |
| [**rio**](https://github.com/commercialhaskell/rio) *(Standard Library)* | 86 | 42 | **0.120s** | 9 | 3 | 1 | 2 |
| [**megaparsec**](https://github.com/mrkkrp/megaparsec) *(Parser combinators)* | 42 | 64 | **0.166s** | 11 | 9 | 1 | 5 |
| [**scotty**](https://github.com/scotty-web/scotty) *(Web Framework)* | 31 | 27 | **0.115s** | 3 | 4 | 4 | 5 |
| **TOTAL** | **492** | **460** | **1.009s** | **78** | **23** | **29** | **58** |

---

## 🛠️ Installation & Usage

```bash
# Clone the repository
git clone https://github.com/bivex/DPX-Haskell.git
cd DPX-Haskell

# Install dependencies using uv
uv sync

# Scan a Haskell project directory
uv run dpx-haskell scan /path/to/haskell/project

# Scan with directory exclusion and export interactive HTML report
uv run dpx-haskell scan /path/to/haskell/project -e test -e .stack-work -H reports/dashboard.html

# Export SARIF for GitHub Code Scanning CI/CD
uv run dpx-haskell scan . -S reports/results.sarif

# Generate AI / LLM Context
uv run dpx-haskell scan . --llm
```

---

## 🏗️ Architecture: Hexagonal (Ports & Adapters)

```
┌────────────────────────────────────────────────────────┐
│                   Driving Adapters                     │
│    CLI (Typer + Rich)   │    API / In-Memory           │
└──────────────────────────┬─────────────────────────────┘
                           │ uses
┌──────────────────────────▼─────────────────────────────┐
│                 Inbound Ports Layer                    │
│      ScannerPort         │       DetectorPort          │
└──────────────────────────┬─────────────────────────────┘
                           │ implemented by
┌──────────────────────────▼─────────────────────────────┐
│                 Application Services                   │
│   ScanningService        │    PatternDetectorService   │
└────────────┬─────────────────────────────┬─────────────┘
             │ operates on                 │ delegates to
┌────────────▼────────────────┐ ┌──────────▼─────────────┐
│        Domain Model         │ │   26 Haskell Rules     │
│ CodeModel, ModuleModel,     │ │ Typeclasses, ReaderT,  │
│ TypeClass, GADT, Function   │ │ STM, Optics, Hazards   │
└─────────────────────────────┘ └────────────────────────┘
             │ uses
┌────────────▼───────────────────────────────────────────┐
│                 Outbound Ports Layer                   │
│  SourceProviderPort │ ParserPort │ ReportFormatterPort │
└────────────┬───────────────────────┬───────────────────┘
             │ implemented by        │ implemented by
┌────────────▼──────────────┐ ┌──────▼───────────────────┐
│     Driven Adapters       │ │       Persistence        │
│ NativeHaskellParserAdapter│ │ HTML, SARIF, JSON, MD    │
│ FileSourceProvider        │ │ FileResultRepository     │
└───────────────────────────┘ └──────────────────────────┘
```

---

## 🌐 The DPX Suite Family

Cross-language architectural static analysis across all modern programming languages:

| Repository | Language / Ecosystem | Primary Paradigms & Focus |
|---|---|---|
| **[`DPX-Huff`](https://github.com/bivex/DPX-Huff)** | **Huff / EVM Stack Assembly** (0.3.x+ / Cancun) | **Macros, Stack Layout, Jumpdest Labels, Selector Dispatchers, GoF 23** |
| **[`DPX-Yul`](https://github.com/bivex/DPX-Yul)** | **Yul / EVM Assembly** (0.8.x - 0.8.28+ / Cancun) | **Memory Management, Storage Packing, Transient Storage (EIP-1153), GoF 23** |
| **[`DPX-Cairo`](https://github.com/bivex/DPX-Cairo)** | **Cairo** (Cairo 1.0 - 2.8+ / Starknet) | **Components, Storage Mapping, Syscalls, Account Abstraction, Upgrades, GoF 23** |
| **[`DPX-Move`](https://github.com/bivex/DPX-Move)** | **Move** (Move 2024 / Aptos / Sui) | **Linear Resources, Abilities, Sui Objects, Hot Potato, Prover, GoF 23** |
| **[`DPX-Lua`](https://github.com/bivex/DPX-Lua)** | **Lua / Luau** (5.1 - 5.4 / LuaJIT) | **Metatable OOP, Coroutines, LuaJIT FFI, GameDev (Roblox/Neovim), GoF 23** |
| **[`DPX-Solidity`](https://github.com/bivex/DPX-Solidity)** | **Solidity** (0.8.x - 0.8.28+) | **EVM Gas Optimization, Proxies, CEI Reentrancy, Yul, GoF 23, Security** |
| **[`DPX-Zig`](https://github.com/bivex/DPX-Zig)** | **Zig** (0.11 - 0.14+) | **Comptime Generics, Allocator RAII, Defer Cleanup, SIMD, GoF 23** |
| **[`DPX-Gleam`](https://github.com/bivex/DPX-Gleam)** | **Gleam** (1.0 - 1.8+) | **Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23** |
| **[`DPX-Mojo`](https://github.com/bivex/DPX-Mojo)** | **Mojo** (24.x - 25.x+) | **SIMD Vectorization, Ownership, Memory Safety, GoF 23, AI Acceleration** |
| **[`DPX-Julia`](https://github.com/bivex/DPX-Julia)** | **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
| **[`DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin)** | **Kotlin** (1.8 - 2.0+) | **Coroutines, Flow, Jetpack Compose, Multiplatform, GoF 23** |
| **[`DPX-Swift`](https://github.com/bivex/DPX-Swift)** | **Swift** (5.5 - 6.0+) | **Protocol-Oriented, Actor Concurrency, SwiftUI, ARC Safety** |
| **[`DPX-CSharp`](https://github.com/bivex/DPX-CSharp)** | **C#** (10 - 13 / .NET 8-9) | **Clean Architecture, CQRS MediatR, Channel Pipelines** |
| **[`DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript)** | **TypeScript / JavaScript** | **Hexagonal DI, Decorator Meta, Reactive Streams, React/NestJS** |
| **[`DPX-Rust`](https://github.com/bivex/DPX-Rust)** | **Rust** (Edition 2021/2024) | **Zero-Cost Abstractions, RAII Lifetimes, Typestate Pattern** |
| **[`DPX-Go`](https://github.com/bivex/DPX-Go)** | **Go** (1.18 - 1.24+) | **Goroutine Channels, CSP Concurrency, Pipeline Streaming** |
| **[`DPX-Py`](https://github.com/bivex/DPX-Py)** | **Python** (3.8 - 3.13+) | **Multi-Paradigm Hexagonal, Data Flow Engine, AsyncIO** |
| **[`DPX-Php`](https://github.com/bivex/DPX-Php)** | **PHP** (8.1 - 8.4+) | **Attribute-driven DDD, Fiber Concurrency, Laravel/Symfony** |
| **[`DPX-Haskell`](https://github.com/bivex/DPX-Haskell)** | **Haskell** (GHC 9.2 - 9.12+) | **Category Theory, Monad Transformers, Free Monads, Optics** |
| **[`DPX-OCaml`](https://github.com/bivex/DPX-OCaml)** | **OCaml** (4.14 - 5.3+ Multicore) | **Functor Modules, Effect Handlers, GADTs, Railway Monads** |
| **[`DPX-Elixir`](https://github.com/bivex/DPX-Elixir)** | **Elixir** (OTP 25 - 27+) | **GenServer, DynamicSupervisor, Actor Fault Tolerance** |
| **[`DPX-Erlang`](https://github.com/bivex/DPX-Erlang)** | **Erlang/OTP** (24 - 27+) | **OTP Behaviors, Supervision Trees, Message Passing** |
| **[`DPX-C`](https://github.com/bivex/DPX-C)** | **C** (C99 - C23) | **Opaque Structs, VTables, MISRA/CERT Safety, Arena Allocators** |
| **[`DPX-Cpp`](https://github.com/bivex/DPX-Cpp)** | **C++** (C++14 - C++20) | **CRTP, Policy-Based Design, RAII Memory Safety, ANTLR4 AST** |
| **[`DPX-Java`](https://github.com/bivex/DPX-Java)** | **Java** (17 - 23+) | **Virtual Threads, Spring Boot / Jakarta EE, GoF Patterns** |
| **[`DPX`](https://github.com/bivex/DPX)** | **Clojure** / Meta Engine | **Pure Functional, Multimethods, Homoiconic Macro Architecture** |
---

## 📄 License

MIT License. Copyright (c) 2026 Bivex.
