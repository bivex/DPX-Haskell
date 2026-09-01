"""Domain Code Model for Haskell (GHC 9.2 - 9.10+ / Haskell2010 / Haskell2021) Static Architecture and Pattern Analysis."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Sequence

from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class ConstructorModel:
    """Represents a data constructor in a Haskell data / GADT declaration."""

    name: str
    fields: list[str] = field(default_factory=list)
    return_type: str = ""
    is_gadt: bool = False


@dataclass
class TypeDeclarationModel:
    """Represents a Haskell `data`, `newtype`, `type`, or GADT declaration."""

    name: str
    params: list[str] = field(default_factory=list)
    is_data: bool = True
    is_newtype: bool = False
    is_type_alias: bool = False
    is_gadt: bool = False
    is_type_family: bool = False
    constructors: list[ConstructorModel] = field(default_factory=list)
    deriving: list[str] = field(default_factory=list)
    deriving_strategies: list[str] = field(default_factory=list)  # "stock", "newtype", "anyclass"
    location: SourceLocation | None = None


@dataclass
class TypeClassModel:
    """Represents a Haskell typeclass definition (`class ... where`)."""

    name: str
    params: list[str] = field(default_factory=list)
    superclasses: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    associated_types: list[str] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class TypeClassInstanceModel:
    """Represents an `instance ... where` declaration."""

    class_name: str
    target_type: str
    location: SourceLocation | None = None


@dataclass
class FunctionModel:
    """Represents a Haskell function or top-level value binding."""

    name: str
    type_signature: str = ""
    params: list[str] = field(default_factory=list)
    body: str = ""
    cyclomatic_complexity: int = 1
    calls: list[str] = field(default_factory=list)
    has_error: bool = False
    has_undefined: bool = False
    has_from_just: bool = False
    has_lazy_foldl: bool = False
    has_catch_all: bool = False
    has_do: bool = False
    location: SourceLocation | None = None

    @property
    def id_str(self) -> str:
        return f"{self.name}"


@dataclass
class ModuleModel:
    """Represents a Haskell module (`module Name where ...`)."""

    name: str
    file_path: str
    exports: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)  # Imported module names
    pragmas: list[str] = field(default_factory=list)  # LANGUAGE extensions, GHC options
    types: dict[str, TypeDeclarationModel] = field(default_factory=dict)
    typeclasses: dict[str, TypeClassModel] = field(default_factory=dict)
    instances: list[TypeClassInstanceModel] = field(default_factory=list)
    functions: dict[str, FunctionModel] = field(default_factory=dict)
    raw_source: str = ""
    clean_source: str = ""
    location: SourceLocation | None = None

    def find_function(self, name: str) -> FunctionModel | None:
        return self.functions.get(name)


@dataclass
class CodeModel:
    """Aggregated semantic domain model of a Haskell codebase."""

    modules: dict[str, ModuleModel] = field(default_factory=dict)
    project_path: str = ""

    def all_modules(self) -> list[ModuleModel]:
        return list(self.modules.values())

    def all_functions(self) -> list[FunctionModel]:
        res = []
        for m in self.modules.values():
            res.extend(m.functions.values())
        return res

    def find_module(self, name: str) -> ModuleModel | None:
        return self.modules.get(name)

    # -------------------------------------------------------------------------
    # Cross-Module Dependency Graph
    # -------------------------------------------------------------------------

    def build_module_import_graph(self) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = {mod_name: set() for mod_name in self.modules}

        for mod_name, mod in self.modules.items():
            for imp in mod.imports:
                if imp in self.modules and imp != mod_name:
                    graph[mod_name].add(imp)

        return graph

    def find_circular_imports(self, max_depth: int = 8, max_cycles: int = 50) -> list[list[str]]:
        graph = self.build_module_import_graph()
        cycles: list[list[str]] = []
        visited: set[str] = set()

        def _dfs(current: str, path: list[str], path_set: set[str]) -> None:
            if len(cycles) >= max_cycles:
                return
            path.append(current)
            path_set.add(current)

            for neighbor in sorted(graph.get(current, set())):
                if neighbor == path[0] and len(path) > 1:
                    canonical = tuple(path)
                    rotations = [canonical[i:] + canonical[:i] for i in range(len(canonical))]
                    min_rot = list(min(rotations))
                    if min_rot not in cycles:
                        cycles.append(min_rot)
                elif neighbor not in path_set and neighbor not in visited and len(path) < max_depth:
                    _dfs(neighbor, path, path_set)

            path.pop()
            path_set.remove(current)

        for node in sorted(graph.keys()):
            _dfs(node, [], set())
            visited.add(node)

        return cycles
