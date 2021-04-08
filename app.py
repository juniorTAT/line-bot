from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    '6ri9RfSej0/9pUmHbTK504KKr71qVE4gCBKKxRKP8wS1ao6qXNO03VNyc3Ppws8GZxllhxKpeuXsmIC+SsSnROW1EtGEQfK5u6SLPxOoXOHKTj6SPfWWYMV3TsVImKY7Tc7bdanVaLRdw/U+gkQL/gdB04t89/1O/w1cDnyilFU='
)
handler = WebhookHandler('4d2209d5d04cad29ca843d1d38243cb3')


@app.route("/callback", methods=['POST'])
#當有人訪問www.line.bot.com/callback這路徑時才執行下面callback function,並觸發handler function
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
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '吃飽沒?'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=s))


if __name__ == "__main__":  #如果app.py這個檔案是直接被執行的,而不是被載入的(import)的話,才執行app.run()
    app.run()