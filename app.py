import random
from typing import Optional
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    cleaned = raw.strip()
    if "." in cleaned:
        return False, None, "Decimal numbers are not allowed. Enter a whole number."

    try:
        value = int(cleaned)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
## Inverted logic condition: FIXED
    try:
        if guess > secret:
            return "Too High", "📈 Go LOWER!"
        else:
            return "Too Low", "📉 Go HIGHER!"
    except TypeError:
        g = str(guess)
        s = str(secret)
        if g == s:
            return "Win", "🎉 Correct!"
        if g > s:
            return "Too High", "📈 Go LOWER!"
        return "Too Low", "📉 Go HIGHER!"

## New helper function: Aligning with an AI feature called Fine-Tuned or Specialized Model
## Adjusting the 'hint' component
def build_distance_hint(guess: int, secret: int, low: int, high: int) -> str:
    """Return a creative hint based on how close guess is to secret."""
    distance = abs(guess - secret)
    span = max(1, high - low)
    ratio = distance / span

    if distance == 0:
        return "🎉 Bullseye!"
    if ratio >= 0.35:
        return "You are freezing in the arctic 🥶"
    if ratio >= 0.12:
        return "The treasure is within reach... but not quite 🏴‍☠️"
    return "You're dancing around the answer 💃"

## Scoring outcomes is inconsistent: FIXED
def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High" or outcome == "Too Low":
       return current_score + 5

    return current_score

## Added a new mini game: Guess the word of the day
def get_word_pool_for_difficulty(difficulty: str):
    """Return a curated (word, topic, clue) pool aligned to the selected difficulty range."""
    low, high = get_range_for_difficulty(difficulty)

    if (low, high) == (1, 20):
        return [
            ("apple", "Fruits", "A common fruit often found in lunch boxes."),
            ("beach", "Places", "A place with sand and waves."),
            ("candle", "Household", "It gives light when the power is out."),
            ("garden", "Nature", "A place where flowers and herbs grow."),
            ("jungle", "Nature", "A dense forest full of wildlife."),
            ("kitten", "Pets", "A very young cat."),
            ("planet", "Space", "Earth is one of these."),
            ("rocket", "Space", "Used to travel beyond Earth."),
            ("sunset", "Nature", "Colorful sky scene at the end of the day."),
            ("window", "Household", "You look through it, not at a screen."),
        ]

    if (low, high) == (1, 50):
        return [
            ("algorithm", "Computing", "A step-by-step method to solve a problem."),
            ("blueprint", "Engineering", "A technical plan before building."),
            ("dinosaur", "Prehistory", "A giant creature from prehistory."),
            ("electric", "Energy", "A type of energy that powers devices."),
            ("firewall", "Cybersecurity", "A security barrier in computer networks."),
            ("notebook", "School", "A place to write notes or code cells."),
            ("parallel", "Concepts", "Things happening at the same time."),
            ("spectrum", "Science", "A range of colors or values."),
            ("treasure", "Adventure", "Something valuable that people search for."),
            ("wildlife", "Animals", "Animals in their natural habitats."),
        ]

    return [
        ("avalanche", "Weather", "A powerful rush of snow down a mountain."),
        ("backpack", "Travel", "You carry this on your shoulders for travel."),
        ("compass", "Navigation", "Helps you find north and direction."),
        ("firefly", "Insects", "A tiny insect that glows at night."),
        ("gallery", "Art", "A place where art is displayed."),
        ("harvest", "Agriculture", "Season when crops are collected."),
        ("journey", "Travel", "A trip from one place to another."),
        ("library", "School", "A quiet place full of books."),
        ("orchard", "Farming", "A farm area with fruit trees."),
        ("puzzle", "Games", "A problem or game that needs solving."),
    ]


def get_word_of_the_day(difficulty: str, previous_word: Optional[str] = None):
    """Pick a random word for the selected difficulty.

    If previous_word is provided, avoid repeating it when the pool allows.
    """
    pool = get_word_pool_for_difficulty(difficulty)
    if len(pool) == 1:
        return pool[0]

    if previous_word:
        filtered = [entry for entry in pool if entry[0] != previous_word]
        if filtered:
            return random.choice(filtered)

    return random.choice(pool)


def parse_word_guess(raw: str):
    if raw is None:
        return False, None, "Enter a word guess."

    cleaned = raw.strip().lower()
    if cleaned == "":
        return False, None, "Enter a word guess."

    if not cleaned.isalpha():
        return False, None, "Only letters are allowed for word guesses."

    return True, cleaned, None


def check_word_guess(guess: str, secret: str):
    if guess == secret:
        return "Win", "🎉 Correct word!"

    if guess > secret:
        return "Too High", "🔤 Your guess is alphabetically AFTER the secret word."

    return "Too Low", "🔤 Your guess is alphabetically BEFORE the secret word."


def build_word_hint(guess: str, secret: str, topic: str, clue: str, attempt_number: int):
    """Build progressively stronger hints so early attempts stay challenging."""
    hints = []
    secret_len = len(secret)

    # Early game: keep hints broad and strategic.
    if attempt_number <= 2:
        hints.append(f"The word has {secret_len} letters.")
        hints.append("Think of common words in this topic before trying niche ones.")

    # Mid game: introduce clue and lightweight signal.
    elif attempt_number <= 4:
        hints.append(f"Clue: {clue}")
        vowel_count = sum(1 for ch in secret if ch in "aeiou")
        hints.append(f"It contains {vowel_count} vowel(s).")

    # Late game: reveal targeted details.
    else:
        hints.append(f"Clue: {clue}")
        hints.append(f"It starts with '{secret[0].upper()}'.")
        if secret_len > 3:
            hints.append(f"It ends with '{secret[-1].upper()}'.")

    if guess:
        common_letters = len(set(guess) & set(secret))
        hints.append(f"Your guess shares {common_letters} unique letters with the secret.")

    return "\n".join(hints)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)
##Incorrect range displayed: FIXED
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state or st.session_state.get("difficulty") != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.difficulty = difficulty
    st.session_state.score = 0
    st.session_state.attempts = 1
    st.session_state.status = "playing"
    st.session_state.history = []

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "debug_unlocked" not in st.session_state:
    st.session_state.debug_unlocked = False

st.subheader("Make A Guess")
st.caption("An AI-generated guessing game. Can you find the secret number?")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
## Debug info is too easily accessible for user: FIXED with password protection
with st.expander("Developer Debug Info"):
    if st.session_state.debug_unlocked:
        if st.button("Lock debug info"):
            st.session_state.debug_unlocked = False
            st.rerun()
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)
    else:
        debug_password = st.text_input(
            "Enter debug password",
            type="password",
            key="debug_password_input",
        )
        if debug_password == "1234":
            st.session_state.debug_unlocked = True
            st.rerun()
        elif debug_password:
            st.error("Incorrect password. Try again.")
        else:
            st.caption("Password required to view debug info.")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

if submit and st.session_state.status == "playing":
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            if outcome == "Win":
                st.success("Correct")
            else:
                hint_message = build_distance_hint(
                    guess=guess_int,
                    secret=st.session_state.secret,
                    low=low,
                    high=high,
                )
                st.warning(hint_message)
        else:
            if outcome == "Win":
                st.success("Correct")
            else:
                st.error("Incorrect")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# ---------------------------
# Mini Game 2: Guess Word of the Day
# ---------------------------
st.divider()
st.subheader("Guess Word of the Day")

word_attempt_limit = attempt_limit_map[difficulty]

if "word_secret" not in st.session_state or st.session_state.get("word_difficulty") != difficulty:
    previous_word = st.session_state.get("word_secret")
    word_secret, word_topic, word_clue = get_word_of_the_day(difficulty, previous_word=previous_word)
    st.session_state.word_secret = word_secret
    st.session_state.word_topic = word_topic
    st.session_state.word_clue = word_clue
    st.session_state.word_difficulty = difficulty
    st.session_state.word_score = 0
    st.session_state.word_attempts = 1
    st.session_state.word_status = "playing"
    st.session_state.word_history = []

if "word_attempts" not in st.session_state:
    st.session_state.word_attempts = 1

if "word_score" not in st.session_state:
    st.session_state.word_score = 0

if "word_status" not in st.session_state:
    st.session_state.word_status = "playing"

if "word_history" not in st.session_state:
    st.session_state.word_history = []

if "word_topic" not in st.session_state:
    _, word_topic, _ = get_word_of_the_day(difficulty)
    st.session_state.word_topic = word_topic

if "word_debug_unlocked" not in st.session_state:
    st.session_state.word_debug_unlocked = False

st.caption(f"Topic: {st.session_state.word_topic}")

st.info(
    f"Guess the word of the day for {difficulty} mode. "
    f"Attempts left: {word_attempt_limit - st.session_state.word_attempts}"
)

with st.expander("Developer Debug Info (Word Game)"):
    if st.session_state.word_debug_unlocked:
        if st.button("Lock word debug info", key="word_debug_lock"):
            st.session_state.word_debug_unlocked = False
            st.rerun()
        st.write("Secret:", st.session_state.word_secret)
        st.write("Attempts:", st.session_state.word_attempts)
        st.write("Score:", st.session_state.word_score)
        st.write("Difficulty:", difficulty)
        st.write("Topic:", st.session_state.word_topic)
        st.write("History:", st.session_state.word_history)
    else:
        word_debug_password = st.text_input(
            "Enter word debug password",
            type="password",
            key="word_debug_password_input",
        )
        if word_debug_password == "4321":
            st.session_state.word_debug_unlocked = True
            st.rerun()
        elif word_debug_password:
            st.error("Incorrect password. Try again.")
        else:
            st.caption("Password required to view word debug info.")

raw_word_guess = st.text_input(
    "Enter your word guess:",
    key=f"word_guess_input_{difficulty}"
)

word_col1, word_col2, word_col3 = st.columns(3)
with word_col1:
    word_submit = st.button("Submit Word Guess 🧠", key="word_submit")
with word_col2:
    word_new_game = st.button("New Word Game 🔁", key="word_new_game")
with word_col3:
    word_show_hint = st.checkbox("Show word hint", value=True, key="word_show_hint")

if word_new_game:
    previous_word = st.session_state.get("word_secret")
    word_secret, word_topic, word_clue = get_word_of_the_day(difficulty, previous_word=previous_word)
    st.session_state.word_secret = word_secret
    st.session_state.word_topic = word_topic
    st.session_state.word_clue = word_clue
    st.session_state.word_attempts = 1
    st.session_state.word_score = 0
    st.session_state.word_status = "playing"
    st.session_state.word_history = []
    st.success("New word game started.")
    st.rerun()

if st.session_state.word_status != "playing":
    if st.session_state.word_status == "won":
        st.success("You already solved the word. Start a new word game to play again.")
    else:
        st.error("Word game over. Start a new word game to try again.")
else:
    if word_submit:
        st.session_state.word_attempts += 1

        ok, guess_word, err = parse_word_guess(raw_word_guess)

        if not ok:
            st.session_state.word_history.append(raw_word_guess)
            st.error(err)
        else:
            st.session_state.word_history.append(guess_word)
            outcome, message = check_word_guess(guess_word, st.session_state.word_secret)

            if word_show_hint:
                if outcome == "Win":
                    st.success(message)
                else:
                    hint_message = build_word_hint(
                        guess=guess_word,
                        secret=st.session_state.word_secret,
                        topic=st.session_state.word_topic,
                        clue=st.session_state.word_clue,
                        attempt_number=st.session_state.word_attempts,
                    )
                    st.warning(hint_message)
            else:
                if outcome == "Win":
                    st.success(message)
                else:
                    st.error("Incorrect word.")

            st.session_state.word_score = update_score(
                current_score=st.session_state.word_score,
                outcome=outcome,
                attempt_number=st.session_state.word_attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.word_status = "won"
                st.success(
                    f"You won! The secret word was '{st.session_state.word_secret}'. "
                    f"Final score: {st.session_state.word_score}"
                )
            else:
                st.info(message)
                if st.session_state.word_attempts >= word_attempt_limit:
                    st.session_state.word_status = "lost"
                    st.error(
                        f"Out of attempts! "
                        f"The secret word was '{st.session_state.word_secret}'. "
                        f"Score: {st.session_state.word_score}"
                    )
