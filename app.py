from flask import Flask,request,jsonify,abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage, ImageMessage, FlexMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent, LocationMessageContent
import os, json, requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
print(LINE_CHANNEL_ACCESS_TOKEN, flush=True)
print(LINE_CHANNEL_SECRET, flush=True)
# Initialize LINE API and Webhook handler
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def send_flex_message(user_id, response_text):
    token = LINE_CHANNEL_ACCESS_TOKEN
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}
    data = {"to": user_id,
            "messages": [{"type": "text",
                          "text": response_text}
                        ]
            }
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # user_message = event.message.text
    user_message = "Thank you for your reviewing. :D"
    user_id = event.source.user_id
    # send_flex_message(user_id, user_message)
    text_message = TextMessage(text=user_message)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(ReplyMessageRequest(reply_token=event.replyToken, messages=[text_message]))

@app.route('/liff_submit',methods=['POST'])
def liff_submit():
    data = request.json
    p_group = data.get('productGroup')
    p_name = data.get('productName')
    p_rating = data.get('rating')
    p_review = data.get('review')
    print(f"{p_group} - {p_name} - {p_rating} - {p_review}", flush=True)
    return jsonify({"response": f"{p_group} - {p_name} - {p_rating} - {p_review}"}), 200
    

# check health path
@app.route('/healthy',methods=['GET'])
def test_api():
    return 'Testing API is completed.', 200

@app.route('/test_post',methods=['POST'])
def test_post():
    data = request.json
    sentence = data.get('sentence')
    response = str(sentence) + ' ' + 'Thank you for your request. ^^'
    return jsonify({"response": response}), 200
    


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
