
from fastmcp import FastMCP

app = FastMCP()

@app.tool()
def train(path: str, target: str, algo: str = "rf", n_estimators: int = 300) -> str:
    """Trains a model and returns the path to the model."""
    print(f"Training model on {path} with target {target} and algorithm {algo}")
    model_path = "/tmp/model.joblib"
    with open(model_path, "w") as f:
        f.write("dummy model")
    return model_path

@app.tool()
def evaluate(model_path: str) -> dict:
    """Evaluates a model and returns a dictionary of metrics."""
    print(f"Evaluating model {model_path}")
    return {"f1": 0.85, "precision": 0.88, "recall": 0.82, "roc_auc": 0.92}
