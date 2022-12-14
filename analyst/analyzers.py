import ast
import sys

from typing import Any, overload

from .analytics import Module, Value, Name


class ModuleAnalyzer(ast.NodeVisitor):

    variables: dict[str, Value]
    module: Module

    def __init__(self, parent: Module | None, name: Name) -> None:
        self.module = Module(parent, name, [])

    @classmethod
    def analyze(
        cls,
        node: ast.Module,
        parent: Module | None,
        name: Name
    ) -> Module:
        analyzer = cls(parent, name)
        if not isinstance(node, ast.Module):
            raise TypeError
        for stmt in node.body:
            analyzer.visit(stmt)
        return analyzer.module

    @overload
    def visit(self, node: ast.expr) -> Value: ...
    if sys.version_info < (3, 9):
        @overload
        def visit(self, node: ast.Slice) -> Value: ...
    @overload  # noqa: E301
    def visit(self, node: ast.stmt) -> None: ...
    @overload
    def visit(self, node: ast.AST) -> Any: ...  # type: ignore

    def visit(self, node: ast.AST) -> Any:  # type: ignore
        return super().visit(node)

    # processing all the kinds of expr

    def visit_BoolOp(self, boolop: ast.BoolOp) -> Value:
        return Value(
            self.module, None,
            dependencies=[self.visit(value) for value in boolop.values],
            definition=boolop
        )

    def visit_BinOp(self, binop: ast.BinOp) -> Value:
        left = self.visit(binop.left)
        right = self.visit(binop.right)
        return Value(
            self.module, None,
            dependencies=[left, right],
            definition=binop
        )

    def visit_UnaryOp(self, unaryop: ast.UnaryOp) -> Value:
        operand = self.visit(unaryop.operand)
        return Value(
            self.module, None,
            dependencies=[operand],
            definition=unaryop
        )

    def visit_Lambda(self, lambda_: ast.Lambda) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=lambda_
        )

    def visit_IfExp(self, ifexp: ast.IfExp) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=ifexp
        )

    def visit_Dict(self, dict: ast.Dict) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=dict
        )

    def visit_Set(self, set: ast.Set) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=set
        )

    def visit_ListComp(self, listcomp: ast.ListComp) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=listcomp
        )

    def visit_SetComp(self, setcomp: ast.SetComp) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=setcomp
        )

    def visit_DictComp(self, dictcomp: ast.DictComp) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=dictcomp
        )

    def visit_GeneratorExp(self, generatorexp: ast.GeneratorExp) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=generatorexp
        )

    def visit_Await(self, await_: ast.Await) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=await_
        )

    def visit_Yield(self, yield_: ast.Yield) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=yield_
        )

    def visit_YieldFrom(self, yieldfrom: ast.YieldFrom) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=yieldfrom
        )

    def visit_Compare(self, compare: ast.Compare) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=compare
        )

    def visit_Call(self, call: ast.Call) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=call
        )

    def visit_FormattedValue(self, formatted: ast.FormattedValue) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=formatted
        )

    def visit_JoinedStr(self, joinedstr: ast.JoinedStr) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=joinedstr
        )

    if sys.version_info < (3, 8):
        def visit_Num(self, num: ast.Num):
            return Value(
                self.module, None,
                dependencies=[],
                definition=num
            )

        def visit_Constant(self, constant: ast.Constant):
            return Value(
                self.module, None,
                dependencies=[],
                definition=constant
            )

    if sys.version_info >= (3, 8):
        def visit_NamedExpr(self, namedexpr: ast.NamedExpr) -> Value:
            return Value(
                self.module, None,
                dependencies=[],
                definition=namedexpr
            )

        def visit_Attribute(self, attribute: ast.Attribute) -> Value:
            return Value(
                self.module, None,
                dependencies=[],
                definition=attribute
            )

    # there is a something complex with Slice
    # TODO: fix complex things with Slice
    def visit_Slice(self, slice_: ast.Slice) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=slice_
        )

    if sys.version_info < (3, 9):
        def visit_ExtSlice(self, extslice: ast.ExtSlice) -> Value:
            return Value(
                self.module, None,
                dependencies=[],
                definition=extslice
            )

        def visit_Index(self, index: ast.Index) -> Value:
            return Value(
                self.module, None,
                dependencies=[],
                definition=index
            )

    def visit_Subscript(self, subscript: ast.Subscript) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=subscript
        )

    def visit_Starred(self, starred: ast.Starred) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=starred
        )

    def visit_Name(self, name: ast.Name) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=name
        )

    def visit_List(self, list: ast.List) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=list
        )

    def visit_Tuple(self, tuple: ast.Tuple) -> Value:
        return Value(
            self.module, None,
            dependencies=[],
            definition=tuple
        )

    # processing all the kidns of stmt

    def visit_FunctionDef(self, functiondef: ast.FunctionDef) -> None:
        pass

    def visit_AsyncFunctionDef(self, asyncfunctiondef: ast.AsyncFunctionDef) -> None:
        pass

    def visit_ClassDef(self, classdef: ast.ClassDef) -> None:
        pass

    def visit_Return(self, ret: ast.Return) -> None:
        pass

    def visit_Delete(self, delete: ast.Delete) -> None:
        pass

    def visit_Assign(self, assign: ast.Assign) -> None:
        value = self.visit(assign.value)
        for target in assign.targets:
            pass

    def visit_AugAssign(self, augassign: ast.AugAssign) -> None:
        pass

    def visit_AnnAssign(self, annassign: ast.AnnAssign) -> None:
        pass

    def visit_For(self, for_: ast.For) -> None:
        pass

    def visit_AsyncFor(self, asyncfor: ast.AsyncFor) -> None:
        pass

    def visit_While(self, while_: ast.While) -> None:
        pass

    def visit_If(self, if_: ast.If) -> None:
        pass

    def visit_With(self, with_: ast.With) -> None:
        pass

    def visit_AsyncWith(self, asyncwith: ast.AsyncWith) -> None:
        pass

    def visit_Raise(self, raise_: ast.Raise) -> None:
        pass

    def visit_Try(self, try_: ast.Try) -> None:
        pass

    if sys.version_info >= (3, 11):
        def visit_TryStar(self, trystar: ast.TryStar) -> None:
            pass

    def visit_Assert(self, assert_: ast.Assert) -> None:
        pass

    def visit_Import(self, import_: ast.Import) -> None:
        pass

    def visit_ImportFrom(self, importfrom: ast.ImportFrom) -> None:
        pass

    def visit_Global(self, global_: ast.Global) -> None:
        pass

    def visit_Nonlocal(self, nonlocal_: ast.Nonlocal) -> None:
        pass

    def visit_Expr(self, expr: ast.Expr) -> None:
        pass

    def visit_Pass(self, pass_: ast.Pass) -> None:
        pass

    def visit_Break(self, break_: ast.Break) -> None:
        pass

    def visit_Continue(self, continue_: ast.Continue) -> None:
        pass
