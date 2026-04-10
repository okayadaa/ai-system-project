# System Diagram: Adding a Fine-Tuned Model

## How it works

| Step | Component | What it does |
|------|-----------|--------------|
| 1 | **Parser** | Checks the player's input is valid |
| 2 | **Checker** | Decides Win, Too High, or Too Low |
| 3 | **Fine-Tuned Model** | Generates a smart, context-aware hint *(new)* |
| 4 | **Evaluator** | Blocks any hint that leaks the secret *(new)* |
| 5 | **Fallback** | Uses old rule-based hint if model fails |
| 6 | **Scorer** | Awards points, updates game state |
| 7 | **Human Reviewer** | Rates sampled hints to build training data *(new)* |
| 8 | **Training Pipeline** | Re-trains the model on rated hints *(new)* |
| 9 | **Tests** | Must pass before a new model version goes live *(new)* |
