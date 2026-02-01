from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        token = request.form.get('token').strip()
        user_id = request.form.get('user_id').strip()
        
        results = {"bot": None, "user": None, "error": None}

        # فحص التوكن
        if token:
            bot_res = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
            if bot_res.get("ok"):
                results["bot"] = bot_res["result"]
            else:
                results["error"] = "التوكن غير صالح ❌"

        # فحص الايدي (يتطلب توكن)
        if user_id and token and results["bot"]:
            user_res = requests.get(f"https://api.telegram.org/bot{token}/getChat", params={"chat_id": user_id}).json()
            if user_res.get("ok"):
                results["user"] = user_res["result"]
            else:
                results["user_error"] = "لم يتم العثور على معلومات الايدي ❌"

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
