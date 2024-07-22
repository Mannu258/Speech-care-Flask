from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///sqlite3.db"  # Replace with your database URL
)
db = SQLAlchemy(app)


app.config["MAIL_SERVER"] = "smtp.hostinger.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "support@speechcare.in"
app.config["MAIL_PASSWORD"] = "Mannu$123"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True


mail = Mail(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

class Detail_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60), nullable=False)
    Email_ID = db.Column(db.String(120), nullable=False)
    Mobile = db.Column(db.String(10), nullable=False)
    Message = db.Column(db.Text, nullable=False)
    def get_ist_now():
        return datetime.utcnow() + timedelta(hours=5, minutes=30)
    Date = db.Column(db.DateTime, nullable=False, default=get_ist_now())

    def __repr__(self):
        return f"<Details {self.Name} {self.Date}>"


class Crediantials(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.username}"


class Email_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    def get_ist_now():
        return datetime.utcnow() + timedelta(hours=5, minutes=30)
    Date = db.Column(db.DateTime, nullable=False, default=get_ist_now())

    def __repr__(self):
        return f"<Email {self.Email} {self.Date}>"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            mobile = request.form["mobile"]
            msg = request.form["msg"]
            print("All details is running")
            try:
                details = Detail_Model(
                    Name=name, Email_ID=email, Mobile=mobile, Message=msg
                )
                db.session.add(details)
                db.session.commit()
            except Exception as e:
                print(e)
            try:
                from Auto_mail import send_mail

                mail = send_mail(name, email, mobile, msg)
                if mail:
                    pass
                else:
                    return "An unexpected error occurred. Please try again later."
            except Exception as e:
                print(f"An error occurred: {e}")
            return render_template("Thank-You.html")
        except:
            email = request.form["email"]
            print("Only single mail is running")
            try:
                e = Email_Model(Email=email)
                db.session.add(e)
                db.session.commit()
            except Exception as e:
                print(e)
            try:
                from Auto_mail import single_mail

                mail = single_mail(email)
                if mail:
                    pass
                else:
                    return "An unexpected error occurred. Please try again later."
            except Exception:
                return "An unexpected error occurred. Please try again later."

    return render_template("index.html")


@app.route("/administrator", methods=["POST", "GET"])
def Admin():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["password"]
        admi = Crediantials.query.filter_by(
            username=username, password=password
        ).first()
        if admi:
            email = Email_Model.query.all()
            details = Detail_Model.query.all()
            return render_template("Database.html", details=details,email=email)
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
