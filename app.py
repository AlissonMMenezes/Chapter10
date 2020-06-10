#!/usr/bin/python3
"""
This code is used as an example for the Chapter10 of the book DevOps With Linux

"""
from functools import wraps
from flask import Flask, request, jsonify

APP = Flask(__name__)


def check_card(func):
    """
    This function validates the credit card transactions
    """
    wraps(func)

    def validation(*args, **kwargs):
        """
          This function is a decorator,
          which will return the function corresponding to the respective action
        """
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
        return func(*args, **kwargs)

    return validation


@APP.route("/api/transaction", methods=["POST"])
@check_card
def transaction():
    """
    This function is resposible to expose the endpoint for receiving the incoming transactions
    """
    card = request.get_json()
    new_limit = card.get("limit") - card.get("transaction").get("amount")
    response = {"approved": True, "newLimit": new_limit}
    return jsonify(response)


if __name__ == '__main__':
    APP.run(debug=True)
