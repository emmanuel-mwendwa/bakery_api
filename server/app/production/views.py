from flask import jsonify
from . import production

@production.route("/")
def production():
    return jsonify({"message": "Welcome to the production home page"}) 