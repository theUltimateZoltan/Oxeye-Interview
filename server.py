from flask import Flask, request, jsonify
import logging
from applogic import AppLogic
from analyzer import ComponentNotFoundError, NoPathToComponentError

app = Flask(__name__)
logger = logging.getLogger(__name__)
applogic = AppLogic()
port = 8000
host = "127.0.0.1"


@app.route("/flow", methods=["GET"])
def do_get():
    if "component" not in request.args:
        return "Usage error: please specify 'component={componentId}'", 400
    try:
        flow = applogic.get_flow(int(request.args.get("component")))
    except ComponentNotFoundError:
        return "Component not found.", 404
    except NoPathToComponentError:
        return jsonify(flow=None, internetFacing=False)
    else:
        return jsonify(flow=flow, internetFacing=True)


@app.route("/component", methods=["POST"])
def do_post_component():
    if "name" not in request.args:
        return "Usage error: please specify name={componentName} in request args.", 400
    try:
        cid = applogic.add_component(request.args.get("name"))
    except:
        return jsonify(result="Internal server error"), 500
    else:
        return jsonify(result="success", componentId=cid)


@app.route("/communication", methods=["POST"])
def do_post_communication():
    if "destination" not in request.args:
        return "Usage error: please specify source={id} and destination={id}.", 400
    try:
        if "source" in request.args:
            applogic.add_communication(int(request.args.get("source")), int(request.args.get("destination")))
        else:
            applogic.add_communication(None, int(request.args.get("destination")))
    except ComponentNotFoundError:
        return jsonify(result="failed: component not found")
    except:
        return jsonify(result="Internal server error"), 500
    else:
        return jsonify(result="success")


if __name__ == "__main__":
    logger.info(f"Serving on port {port}")
    app.run(host=host, port=port)
