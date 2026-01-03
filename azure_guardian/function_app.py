import json
import sys
import os
import azure.functions as func

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.main import main as guardian_main

app = func.FunctionApp()

@app.route(route="analyze_repo", auth_level=func.AuthLevel.ANONYMOUS)
def analyze_repo(req: func.HttpRequest) -> func.HttpResponse:
    try:
        repo_url = req.params.get("repo")

        result = guardian_main(
            return_json=True,
            override_repo=repo_url
        )

        return func.HttpResponse(
            json.dumps(result, indent=4),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )


