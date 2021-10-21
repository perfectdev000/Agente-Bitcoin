import requests

def coindesk_get_BPI(currencyCode):
    url = f"https://api.coindesk.com/v1/bpi/currentprice/{currencyCode}.json"
    try:
        response = requests.get(url)
        response_json = response.json()
        if "bpi" in response_json:
            return response_json["bpi"]
        else:
            return {"error": response_json}
    except  Exception as e:
        return {"error": e.__str__()}
