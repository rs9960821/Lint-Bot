from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from crawler import crawler

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('4/fBvJvzGme3tHE7184dFfY1xptZ7I6oDP06bXyl/NTxXaVg5K5d13gcBoeeOLPPeW87LIIYEE+UqGNoh6KpjdkX/7aJK3iVg2Gum58YYwaYpkxXEVBTD7lWZZF7vEIaUK0Qwk0lmWM9GV42JC+KWQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c159f4a788241756da9e351d34cb4a44')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    if "資訊" == event.message.text:
        Dcard = crawler()
        result = Dcard.information
    else :
        Dcard = crawler()
        result = Dcard.crawl_specific_forum(event.message.text)
    message = TextSendMessage(text=result)  
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
