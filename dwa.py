from flask import *
from modules import db_connect as db

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__" :
    app.run(host='0.0.0.0', port=8000, debug=True)