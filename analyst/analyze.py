import ast
from pathlib import Path

from .analytics import Module, Name
from .analyzers import ModuleAnalyzer


def analyze_file(path: str | Path, name: str | None = None) -> Module:
    path = Path(path).resolve()
    name = name or "<string>"
    module_name = Name(tuple(name.split(".")))
    with path.open() as f:
        source = f.read()
    tree = ast.parse(source, path.name, "exec")
    module = ModuleAnalyzer.analyze(tree, None, module_name)
    return module
