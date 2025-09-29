from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Render a simple page so we can verify Flask + templating works
    return render_template("index.html", greeting="Good Morning")

if __name__ == "__main__":
    app.run(debug=True)
