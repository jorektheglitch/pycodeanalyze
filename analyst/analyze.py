import ast
from pathlib import Path

from .analytics import Module
from .analyzers import ModuleAnalyzer


def analyze_file(path: str | Path) -> Module:
    path = Path(path).resolve()
    with path.open() as f:
        source = f.read()
    tree = ast.parse(source, path.name, "exec")
    module = ModuleAnalyzer.analyze(tree, None, None)
    return module
