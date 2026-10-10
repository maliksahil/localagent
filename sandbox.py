import subprocess


class TestSandbox:
    """Runs local pytest suite to verify agent patches."""

    @staticmethod
    def run_tests() -> bool:
        print("[*] Running local test suite via pytest...")
        result = subprocess.run(["pytest"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[+] All local tests passed successfully!")
            return True
        else:
            print("[!] Tests failed! Reverting changes.")
            print(result.stdout)
            return False
