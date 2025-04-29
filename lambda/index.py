import json
import os
import urllib.request

# FastAPIのエンドポイントURL
FASTAPI_URL = os.environ.get("FASTAPI_URL", "https://0dec-35-231-30-134.ngrok-free.app/predict")  # ColabのURLに置き換える

def lambda_handler(event, context):
    try:
        # ユーザーのメッセージを取得
        message = event.get("message", "こんにちは")

        # 会話履歴はとりあえず空にして、ユーザーメッセージだけ送る
        request_payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": message}]
                }
            ]
        }

        # FastAPIにPOSTリクエスト
        req = urllib.request.Request(
            FASTAPI_URL,
            data=json.dumps(request_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as res:
            response_body = json.loads(res.read().decode("utf-8"))

        print("FastAPI response:", json.dumps(response_body))

        # 応答の取り出し（FastAPIの戻り形式に応じて変更）
        if not response_body.get("response"):
            raise Exception("Invalid response")

        assistant_response = response_body["response"]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": assistant_response
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }

