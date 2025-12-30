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
        result = guardian_main(return_json=True)
        return func.HttpResponse(
            json.dumps(result, indent=4),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

