def calculate_user_score(expression: str) -> float:
    """
    Evaluates a math expression provided by the user.
    WARNING: Intentional vulnerability (Remote Code Execution via eval).
    """
    # This is extremely dangerous because eval() allows executing arbitrary Python code!
    return eval(expression)

def add_numbers(a: int, b: int) -> int:
    return a + b