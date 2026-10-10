import sys
from ast_parser import LocalASTAnalyzer
from llm_client import LocalLLMClient
from patcher import CodePatcher
from sandbox import TestSandbox


def main():
    print("==================================================")
    print("🤖 Local-First Autonomous Security Agent Initialized")
    print("==================================================")

    analyzer = LocalASTAnalyzer()
    client = LocalLLMClient()

    staged_files = analyzer.get_staged_files()
    if not staged_files:
        print("[*] No staged Python files found to review. Exiting.")
        sys.exit(0)

    for file_path in staged_files:
        print(f"\n[->] Analyzing staged file: {file_path}")
        functions = analyzer.extract_functions_from_file(file_path)

        for func in functions:
            print(
                f"    Checking function: {func['name']} (Line {func['lineno']})")
            analysis = client.analyze_code_snippet(func['code'])

            if analysis.get("vulnerable", False):
                print(
                    f"    [!] VULNERABILITY DETECTED in {func['name']}! Severity: {analysis.get('severity')}")
                for issue in analysis.get("issues", []):
                    print(f"        - {issue}")

                # Apply patch
                success = CodePatcher.apply_patch(
                    file_path, func['name'], analysis.get("refactored_code"))
                if success:
                    # Verify via test sandbox
                    if not TestSandbox.run_tests():
                        print("[!] Rolling back git changes due to test failure.")
                        subprocess.run(
                            ["git", "checkout", file_path], check=True)
                        sys.exit(1)
            else:
                print(f"    [+] Function {func['name']} looks clean.")

    print("\n[+] Code review and security audit completed successfully!")


if __name__ == "__main__":
    main()
