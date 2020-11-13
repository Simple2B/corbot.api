import json

from flask import render_template, Blueprint, request

from app.controllers.dispatcher import dispatch
from app.controllers.ip_auth import ip_auth
from app.forms import TestingForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=['GET'])
@ip_auth
def index():
    form = TestingForm()
    return render_template("index.html", form=form)


@main_blueprint.route("/api", methods=['POST'])
@ip_auth
def api():
    if request.json:
        json_data = request.json  # automatically converted to dict
        # dispatch does all work, except converting to json
        return json.dumps(dispatch(json_data), indent=4, sort_keys=True, default=str)
    form = TestingForm()  # form to test from admin dashboard
    if form.validate_on_submit():
        data = json.loads(form.Data.data)  # json is entered to TextArea field called Data
        # then it it is converted to json to simulate real application
        res = {"request": form.Method.data, "data": data}
        return json.dumps(dispatch(res))
    return {}
