from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

# ============= check_guess tests =============
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# ============= parse_guess tests =============
def test_parse_guess_valid_integer():
    # Valid integer input
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_guess_reject_decimal():
    # Decimal input should fail because guesses must be whole numbers
    ok, value, error = parse_guess("42.7")
    assert ok is False
    assert value is None
    assert error == "Decimal numbers are not allowed. Enter a whole number."

def test_parse_guess_none():
    # None input should fail
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_guess_empty_string():
    # Empty string should fail
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_guess_invalid_input():
    # Non-numeric input should fail
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

# ============= update_score tests =============
def test_update_score_win_first_attempt():
    # Winning on first attempt should award maximum points (100)
    score = update_score(0, "Win", 1)
    assert score == 100

def test_update_score_win_later_attempt():
    # Winning on later attempt should deduct points (100 - 10 * (5-1) = 60)
    score = update_score(0, "Win", 5)
    assert score == 60

def test_update_score_win_many_attempts():
    # If attempts are high enough, should floor at 10 points minimum
    score = update_score(0, "Win", 10)
    assert score == 10

def test_update_score_too_high():
    # "Too High" outcome should award 5 points
    score = update_score(0, "Too High", 1)
    assert score == 5

def test_update_score_too_low():
    # "Too Low" outcome should award 5 points
    score = update_score(0, "Too Low", 3)
    assert score == 5

def test_update_score_accumulated():
    # Test score accumulation
    score = 10
    score = update_score(score, "Too High", 1)
    score = update_score(score, "Too Low", 2)
    score = update_score(score, "Win", 3)
    assert score == 10 + 5 + 5 + 80

# ============= get_range_for_difficulty tests =============
def test_range_easy():
    # Easy difficulty should return 1-20
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_normal():
    # Normal difficulty should return 1-100
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_range_hard():
    # Hard difficulty should return 1-50
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_range_invalid_difficulty():
    # Invalid difficulty should default to 1-100
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100
