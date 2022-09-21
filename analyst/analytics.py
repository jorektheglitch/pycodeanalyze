from __future__ import annotations

import ast
from abc import ABC
from dataclasses import dataclass

from typing import Any, NewType

Name = NewType("Name", tuple[str, ...])


@dataclass
class Value(ABC):
    type: Class | None
    dependencies: list[Value]


@dataclass
class Module(Value, dict[str, Value]):
    parent: Module | None
    name: Name
    type: Class | None
    dependencies: list[Value]

    def __init__(
        self,
        parent: Module | None,
        name: Name,
        dependencies: list[Value],
        *args: Any, **kwargs: Any
    ):
        from .builtin_types import module_type
        dict.__init__(self, *args, **kwargs)
        super().__init__(module_type, dependencies)
        self.parent = parent
        self.name = name


class Variable(Value):
    parent: Module | Function | Class
    type: Class | None
    dependencies: list[Value]
    definition: ast.expr


class Function(Value):
    parent: Module | Function | Class
    type: Class | None
    dependencies: list[Value]
    definition: ast.FunctionDef


class Class(Value, dict[str, Value]):
    parent: Module | Function | Class
    type: Class | None
    dependencies: list[Value]
    definition: ast.ClassDef
