from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///sqlite3.db"  # Replace with your database URL
)
db = SQLAlchemy(app)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "jeemannu90@gmail.com"
app.config["MAIL_PASSWORD"] = "icbh jolb cnuv dnbq"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True


mail = Mail(app)
mail.init_app(app)

with app.app_context():
    db.create_all()


class Detail_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Mobile = db.Column(db.String(10), nullable=False)
    Message = db.Column(db.Text, nullable=False)
    Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Details {self.Name} {self.Date}>"


class Email_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
            details = Detail_Model(Name=name, Email=email, Mobile=mobile, Message=msg)
            db.session.add(details)
            db.session.commit()
            try:
                from Auto_mail import send_mail
                send_mail(name, email, mobile, msg)
            except Exception as e:
                print(f"An error occurred: {e}")
            return render_template("Thank-You.html")
        except:
            email = request.form["email"]
            print("Only single mail is running")
            from Auto_mail import single_mail
            single_mail(email)
            e = Email_Model(Email=email)
            db.session.add(e)
            db.session.commit()        
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
