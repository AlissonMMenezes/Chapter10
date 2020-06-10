#!/usr/bin/python3

from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)


def check_card(f):
    wraps(f)

    def validation(*args, **kwargs):
        data = request.get_json()
        if not data.get("status"):
            response = {"approved": False,
                        "newLimit": data.get("limit"),
                        "reason": "Blocked Card"}
            return jsonify(response)

        if data.get("limit") < data.get("transaction").get("amount"):
            response = {"approved": False,
                        "newLimit": data.get("limit"),
                        "reason": "Transaction above the limit"}
            return jsonify(response)
        return f(*args, **kwargs)

    return(validation)


@app.route("/api/transaction", methods=["POST"])
@check_card
def transaction():
    card = request.get_json()
    new_limit = card.get("limit") - card.get("transaction").get("amount")
    response = {"approved": True, "newLimit": new_limit}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
