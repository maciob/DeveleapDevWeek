from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

@app.route("/provider", methods=["POST"])
def add_new_provider():
    return render_template("index.html")

@app.rout("/provider/<id>", methods=["PUT"])
def update_provider():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)