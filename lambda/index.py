import json, urllib.request, ssl

FASTAPI_URL = "https://23a7-35-232-13-38.ngrok-free.app/generate"
CTX = ssl.create_default_context()
TIMEOUT = 30

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        prompt = body["message"]

        payload = json.dumps({
            "prompt": prompt,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }).encode()

        req = urllib.request.Request(
            FASTAPI_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, context=CTX, timeout=TIMEOUT) as r:
            reply = json.loads(r.read())["generated_text"]

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"success": True, "response": reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"success": False, "error": str(e)})
        }

