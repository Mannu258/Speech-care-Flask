from datetime import datetime, timedelta

from flask import Flask, render_template, request, send_from_directory
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

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


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Mobile = db.Column(db.String(10), nullable=False)
    Email = db.Column(db.Text, nullable=False)

    def get_ist_now():
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

    Date = db.Column(db.DateTime, nullable=False, default=get_ist_now())

    Q1 = db.Column(db.Integer, nullable=False)
    Q2 = db.Column(db.Integer, nullable=False)
    Q3 = db.Column(db.Integer, nullable=False)
    Q4 = db.Column(db.Integer, nullable=False)
    Q5 = db.Column(db.Integer, nullable=False)
    Q6 = db.Column(db.Integer, nullable=False)
    Q7 = db.Column(db.Integer, nullable=False)
    Q8 = db.Column(db.Integer, nullable=False)
    Q9 = db.Column(db.Integer, nullable=False)
    Q10 = db.Column(db.Integer, nullable=False)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


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
            email = Email_Model.query.order_by(Email_Model.id.desc()).all()
            details = Detail_Model.query.order_by(Detail_Model.id.desc()).all()
            return render_template("Database.html", details=details, email=email)
        else:
            return render_template("403.html")
    return render_template("login.html")


@app.route("/assessment-admin", methods=["POST", "GET"])
def Assessmentadmin():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["password"]
        try:
            admi = Crediantials.query.filter_by(
                username=username, password=password
            ).first()
        except Exception as e:
            print(e)
        if admi:
            Ques = Questions.query.order_by(Questions.id.desc()).all()
            return render_template("a-Database.html", Ques=Ques)
        else:
            return render_template("403.html")
    return render_template("a-login.html")


@app.route("/speech-care-Assessment", methods=["POST", "GET"])
def Assessment():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        Mobile = request.form["phone"]
        email = request.form["email"]
        Q1 = request.form["q1"]
        Q2 = request.form["q2"]
        Q3 = request.form["q3"]
        Q4 = request.form["q4"]
        Q5 = request.form["q5"]
        Q6 = request.form["q6"]
        Q7 = request.form["q7"]
        Q8 = request.form["q8"]
        Q9 = request.form["q9"]
        Q10 = request.form["q10"]
        print(name, age, Mobile, email)
        print(Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10)
        sum = (
            int(Q1)
            + int(Q2)
            + int(Q3)
            + int(Q4)
            + int(Q5)
            + int(Q6)
            + int(Q7)
            + int(Q8)
            + int(Q9)
            + int(Q10)
        )
        print(sum)
        try:
            from Auto_mail import assessment_mail

            Que = Questions(
                Name=name,
                Age=age,
                Mobile=Mobile,
                Email=email,
                Q1=Q1,
                Q2=Q2,
                Q3=Q3,
                Q4=Q4,
                Q5=Q5,
                Q6=Q6,
                Q7=Q7,
                Q8=Q8,
                Q9=Q9,
                Q10=Q10,
            )
            db.session.add(Que)
            db.session.commit()
            mail = assessment_mail(name, email, sum)
            if mail:
                return render_template("Thank-You.html")
            else:
                return f"{mail}"
        except Exception as e:
            print(e)
    return render_template("Assisment.html")

@app.route("/speech-care-tutorial")
def Tutorial():
    return render_template("Video.html")


@app.route("/robots.txt")
@app.route("/sitemap.xml")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":
    app.run(debug=True, port=8000)
