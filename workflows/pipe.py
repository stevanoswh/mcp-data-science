
import requests

# This is a reference implementation of the pipeline logic.
# It is not meant to be executed directly, but rather to be used as a guide for the LLM agent.

def call_tool(tool_name, params):
    server_name, tool = tool_name.split('/')
    url = f"http://{server_name}:8000/{tool}"
    response = requests.post(url, json=params)
    response.raise_for_status()
    return response.json()

def run_pipeline(ds, tgt):
    path  = call_tool('dataops/ingest_s3', {'s3_uri': ds})
    errs  = call_tool('dataops/validate_df', {'path': path})
    if errs:
        return {'status':'invalid', 'errors':errs}
    path  = call_tool('feature/encode_cat',  {'path': path})
    path  = call_tool('feature/impute_null', {'path': path})
    model = call_tool('trainer/train',      {'path': path, 'target': tgt, 'n_estimators':300})
    met   = call_tool('trainer/evaluate',   {'model_path': model})
    if met['f1'] < 0.80:
        return {'status':'low_f1', **met}
    url   = call_tool('deployer/push_k8s',  {'model_path': model})
    return {'status':'deployed', 'url': url, **met}

if __name__ == "__main__":
    # Example usage:
    # from workflows.pipe import run_pipeline
    # result = run_pipeline("s3://acme/churn.csv", "churn")
    # print(result)
    pass
