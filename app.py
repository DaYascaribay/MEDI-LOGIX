from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_folder="static", template_folder="templates")

# Configuración de JWT
app.config["JWT_SECRET_KEY"] = "medilogix140725"
jwt = JWTManager(app)

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1019)
