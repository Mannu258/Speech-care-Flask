from app import Message, app, mail

with app.app_context():

    def send_mail(name, email, mobile, msg):
        try:
            submission_msg = Message(
                subject="New Submission",
                sender="support@speechcare.in",
                recipients=[
                    "kumarjha94@gmail.com",
                    "support@speechcare.in",
                    "speechcare.in@gmail.com",
                ],
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
            recipients=[
                f"{email}",
                "kumarjha94@gmail.com",
                "support@speechcare.in",
                "speechcare.in@gmail.com",
            ],
        )
        autoreply_msg.body = f"Thank you for Sharing your Email. Our team will review it and get back to you soon.\n\nThanks and regards,\nSpeech Care"
        mail.send(autoreply_msg)
        return True

    def assessment_mail(name, email, sum):
        Score = ""
        if sum == 0:
            Score = "Normal"
        elif sum > 0 and sum <= 10:
            Score = "Mild"
        elif sum > 10 and sum <= 20:
            Score = "Moderate"
        elif sum > 20 and sum <= 30:
            Score = "severe"

        try:
            autoreply_msg = Message(
                subject="Thank You for the Assessment",
                sender="support@speechcare.in",
                recipients=[
                    "kumarjha94@gmail.com",
                    "support@speechcare.in",
                    "speechcare.in@gmail.com",
                    f"{email}",
                ],
            )
            autoreply_msg.body = f"""
Dear {name},

Thank you for completing the self-assessment for stuttering on Speechcare.in.

Your initial diagnosis based on the self-assessment is as follows Your Stuttering Level: **{Score}**

Please note that this self-assessment is for preliminary purposes only and may not provide a fully accurate diagnosis. For a comprehensive evaluation and personalized treatment plan, we recommend consulting with a licensed speech therapist or visiting Speechcare.in.

If you have any questions or would like to schedule a professional consultation, please feel free to reply to this email or visit our website.

Thank you for choosing Speechcare.in.

Best regards,
Speechcare.in Team
speechcare.in

---

*Disclaimer: The self-assessment results are not a substitute for professional evaluation and advice. Always consult with a qualified healthcare provider for personalized guidance.*
"""
            mail.send(autoreply_msg)
            return True
        except Exception as e:
            return f"{e}"
