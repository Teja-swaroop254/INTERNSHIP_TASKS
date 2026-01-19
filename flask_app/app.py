from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! Go to /convert?name=yourname"

@app.route("/convert")
def convert():
    name = request.args.get("name", "")
    return f"Your name in uppercase: {name.upper()}"

if __name__ == "__main__":
    app.run(debug=True)
