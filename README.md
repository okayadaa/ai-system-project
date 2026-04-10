# 🎮 Game Glitch: The Impossible Guesser

## Updated Version:
-> Guess parsing was tightedn to reject decimals specifically<br>
-> Guess comparisons logic was corrected and made safer<br>
-> Check_guess is reliably returns win, too high, and too low including generating messages<br> 
-> Session state reset and initialization behavior has improved (preventing a stale state)<br>
-> Developer debug panel was gated behind a password<br>
-> Hint system was upgraded with distance based feedback<br>
-> Second mini game was added<br>

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## Evaluation:
Based on the automated test, 17 tests passed and 1 test failed. The update_score_accumulated failed due to an AssertionError. The calculation was a bit off since ideally the update_score function relies on 100 - 10 * (attempt_number - 1). For example, if user is one attempt number 3 then the result would be 80. And I noticed in the test asserts, there's a value 70. Which that value is only on attempt number 4. However, with the adjustment I would have to change the value to 80 rather than 70. In addition, the 17 tests that did passed, confirming on number comparisons, input parsing, score updates, and difficulty ranges are functioning as expected.   

## 📸 Demo: Before & After

<img width="1324" height="690" alt="Screenshot 2026-03-01 at 7 47 54 PM" src="https://github.com/user-attachments/assets/bb14fe13-ae9a-49ec-9734-f007948cceb5" />



<img width="1263" height="706" alt="Screenshot 2026-04-10 at 10 43 56 AM" src="https://github.com/user-attachments/assets/85e8159a-dfa3-4f45-aacc-5191a37dea92" />



