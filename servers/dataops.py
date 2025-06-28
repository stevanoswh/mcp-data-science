from fastmcp import FastMCP

app = FastMCP()

@app.tool()
def ingest_s3(s3_uri: str) -> str:
    """Ingests data from S3 and returns the path to the downloaded data."""
    print(f"Ingesting from {s3_uri}")
    # Simulate download
    local_path = f"/tmp/{s3_uri.split('/')[-1]}"
    with open(local_path, "w") as f:
        f.write("dummy,data\n1,2\n")
    return local_path

@app.tool()
def validate_df(path: str) -> list[str]:
    """Validates the dataframe and returns a list of errors."""
    print(f"Validating {path}")
    # Simulate validation
    return []
