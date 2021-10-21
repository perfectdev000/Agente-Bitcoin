import base64
from urllib.parse import quote
import requests
from flask import Flask, jsonify
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

twilio_service = "VAd7c480e8f3c167a10eff93c51d5a1ef8"
twilio_user = "ACe087d242a484e3031f1cc6e764fc4fab"
twilio_secret = "ba78b9c85109c0a9bd7b0405780288c3"

headers = CaseInsensitiveDict()
auth_bearer = str(base64.b64encode(f"{twilio_user}:{twilio_secret}".encode("utf-8")), "utf-8")
headers["Authorization"] = f"Basic {auth_bearer}"
headers["Content-Type"] = "application/x-www-form-urlencoded"


def twilio_send_code(to, channel):
    url = f"https://verify.twilio.com/v2/Services/{twilio_service}/Verifications"
    data = f"To={quote(to)}&Channel={channel}"
    try:
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if "status" in response_json:
            if response_json["status"] == "pending":
                return response_json
            else:
                return {"error": response_json["message"]}
        else:
                return {"error": response_json}
    except  Exception as e:
        return {"error": e.__str__()}

def twilio_view_verification(sid):
    url = f"https://verify.twilio.com/v2/Services/{twilio_service}/Verifications/{sid}"
    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if "status" in response_json:
            if response_json["status"] == "pending":
                return response_json
            else:
                return {"error": response_json["message"]}
        else:
                return {"error": response_json}
    except  Exception as e:
        return {"error": e.__str__()}

def twilio_verify_code(to, code):
    url = f"https://verify.twilio.com/v2/Services/{twilio_service}/VerificationCheck"
    data = f"To={quote(to)}&Code={code}"
    try:
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if "status" in response_json:
            if response_json["status"] == "approved":
                return response_json
            else:
                return {"error": response_json["message"]}
        else:
                return {"error": response_json}
    except  Exception as e:
        return {"error": e.__str__()}
