from flask import Flask

app = Flask(__name__)


def run():
    app.run(host="0.0.0.0")


@app.route("/")
def home():
    return "Server is running"


# @app.route("/health", methods = ["GET"])
# def health():
#     return "OK"

# @app.route("/", methods = ["POST"])
# def

# @app.route("/", methods = ["PUT"])
# def

if __name__ == "__main__":
    run()
