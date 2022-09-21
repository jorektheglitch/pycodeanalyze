from __future__ import annotations

import ast
from abc import ABC
from dataclasses import dataclass

from typing import Any, MutableSequence, NewType

Name = NewType("Name", tuple[str, ...])


@dataclass
class BaseValue(ABC):
    parent: BaseValue | None
    type: Class | None
    dependencies: MutableSequence[BaseValue]


@dataclass
class Module(BaseValue, dict[str, BaseValue]):
    parent: Module | None
    name: Name
    type: Class | None
    dependencies: MutableSequence[BaseValue]

    def __init__(
        self,
        parent: Module | None,
        name: Name,
        dependencies: MutableSequence[BaseValue],
        *args: Any, **kwargs: Any
    ):
        from .builtin_types import module_type
        dict.__init__(self, *args, **kwargs)
        super().__init__(parent, module_type, dependencies)
        self.parent = parent
        self.name = name


@dataclass
class Value(BaseValue):
    parent: Module | Function | Class
    type: Class | None
    dependencies: MutableSequence[BaseValue]
    definition: ast.expr


@dataclass
class Function(BaseValue):
    parent: Module | Function | Class
    type: Class | None
    dependencies: list[BaseValue]
    definition: ast.FunctionDef


@dataclass
class Class(BaseValue, dict[str, BaseValue]):
    parent: Module | Function | Class
    type: Class | None
    dependencies: list[BaseValue]
    definition: ast.ClassDef
