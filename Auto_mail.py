from app import mail, Message, app

with app.app_context():
    def send_mail(name, email, mobile, msg):
        try:
            submission_msg = Message(
                subject="New Submission",
                sender="support@speechcare.in",
                recipients=["kumarjha94@gmail.com","support@speechcare.in","speechcare.in@gmail.com"],
            )
            submission_msg.body = f"Dear Team,\n\nYou have received a new submission from {name}:\n\nSubmission Details:\n{msg}\n\nContact Information:\nEmail: {email}\nMobile: {mobile}\n\nBest regards,\nSpeech Care"
            mail.send(submission_msg)
            autoreply_msg = Message(
                subject="Thank You for the Submission",
                sender="support@speechcare.in",
                recipients=[email],
            )
            autoreply_msg.body = f"Dear {name},\n\nThank you for your submission. Our team will review it and get back to you soon.\n\nThanks and regards,\nSpeech Care"
            mail.send(autoreply_msg)
            return True
        except Exception as e:
            return f"Error sending emails: {e}"
    def single_mail(email):
        autoreply_msg = Message(
                subject="Thank You for the Submission",
                sender="support@speechcare.in",
                recipients=[f"{email}","kumarjha94@gmail.com","support@speechcare.in","speechcare.in@gmail.com"],
            )
        autoreply_msg.body = f"Thank you for Sharing your Email. Our team will review it and get back to you soon.\n\nThanks and regards,\nSpeech Care"
        mail.send(autoreply_msg)
        return True


