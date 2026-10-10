import ast
import subprocess
from typing import List, Dict, Any


class LocalASTAnalyzer:
    """
    Analyzes local python files to extract 
    function and class definitions 
    modified in recent git commits.
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def get_staged_files(self) -> List[str]:
        """Retrieves list of git staged files for review."""
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split("\n")
        return [f for f in files if f.endswith(".py")]

    def extract_functions_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parses a Python file and extracts function metadata and source code."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_code = ast.get_source_segment(content, node)
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno,
                    "code": func_code
                })

        return functions


if __name__ == "__main__":
    analyzer = LocalASTAnalyzer()
    print("Staged files:", analyzer.get_staged_files())
