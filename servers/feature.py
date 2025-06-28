
from fastmcp import FastMCP

app = FastMCP()

@app.tool()
def encode_cat(path: str) -> str:
    """Encodes categorical features and returns the path to the processed data."""
    print(f"Encoding categorical features in {path}")
    return path

@app.tool()
def impute_null(path: str) -> str:
    """Imputes null values and returns the path to the processed data."""
    print(f"Imputing null values in {path}")
    return path
