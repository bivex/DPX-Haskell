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

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
