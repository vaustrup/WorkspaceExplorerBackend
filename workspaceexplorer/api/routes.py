from flask import Blueprint, request, jsonify
from flask_cors import CORS
import pyhf
import cabinetry

from celery import shared_task
from celery.result import AsyncResult

api_bp = Blueprint('api_bp', __name__, url_prefix='/api/v1')
CORS(api_bp)

@api_bp.route('/', methods=['GET'])
def home():
    return "Welcome to the WorkspaceExplorer API!", 200

@api_bp.route('/workspace', methods=['POST'])
def post_workspace():
    payload = request.json
    spec = payload.get("workspace")
    if not spec:
        return "FAILURE", 400
    workspace = pyhf.Workspace(spec)
    result = fit_workspace.delay(workspace.model(), workspace.data(workspace.model()))
    return {"result_id": result.id}


@api_bp.get("/workspace/<id>")
def fit_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }


@shared_task(ignore_result=False)
def fit_workspace(model, data):
    try: 
        fit_results = cabinetry.fit.fit(model, data)
        return {
                "bestfit": fit_results.bestfit.tolist(),
                "uncertainty": fit_results.uncertainty.tolist(),
                "correlations":fit_results.corr_mat.tolist(),
                "labels": fit_results.labels
                }
    except Exception as e:
        return repr(e)