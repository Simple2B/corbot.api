import json

from flask import render_template, Blueprint, request

from app.controllers.dispatcher import dispatch
from app.forms import TestingForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=['GET'])
def index():
    form = TestingForm()
    return render_template("index.html", form=form)


@main_blueprint.route("/api", methods=['POST'])
def api():
    if request.json:
        json_data = request.json  # dict
        return json.dumps(dispatch(json_data))
    form = TestingForm()
    if form.validate_on_submit():
        data = json.loads(form.Data.data)
        res = {"request": form.Method.data, "data": data}
        return json.dumps(dispatch(res))