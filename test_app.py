from app import add_numbers, calculate_user_score

def test_add_numbers():
    assert add_numbers(2, 3) == 5

def test_calculate_user_score():
    assert calculate_user_score("10 + 20") == 30