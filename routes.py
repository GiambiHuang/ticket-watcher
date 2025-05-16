from flask import Flask, request
import requests
import json
import os
from dotenv import load_dotenv

# 讀取 .env
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
GROUP_ID = os.getenv("GROUP_ID")

app = Flask(__name__)

def reply_message(reply_token, messages):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    body = {
        'replyToken': reply_token,
        'messages': messages
    }
    response = requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=body)
    print(f"Reply status: {response.status_code}, {response.text}")

# @app.route("/webhook", methods=['POST'])
# def webhook():
#     body = request.json
#     print("📥 Received:", json.dumps(body, indent=2))

#     events = body.get("events", [])
#     for event in events:
#         if event.get("type") == "message":
#             reply_token = event["replyToken"]
#             user_message = event["message"].get("text", "")
#             group_id = event["source"].get("groupId", "N/A")

#             print(f"👤 Group: {group_id} | Message: {user_message}")

#             reply_message(reply_token, [{
#                 "type": "text",
#                 "text": f"你說了：「{user_message}」，這是來自群組：{group_id}"
#             }])
#     return "OK", 200

@app.route("/push", methods=["POST"])
def push_to_group():
    data = request.json
    group_id = GROUP_ID
    text = data["text"]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }

    body = {
        "to": group_id,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }

    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=body)
    return {"status": response.status_code, "detail": response.text}, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)