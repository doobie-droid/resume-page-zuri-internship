# this is the main server file for an interactive resume page that contains a form
import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import smtplib

app = Flask(__name__)

gmail_address = os.environ.get("gmail_address")
gmail_password = os.environ.get("gmail_password")
receiver_address = "lesliedouglas23@gmail.com"
app.config['SECRET_KEY'] = "werwefasd"
Bootstrap(app)


class ContactMe(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email_address = StringField("Email Address", validators=[DataRequired()])
    body = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Contact Me")


@app.route('/', methods=['POST', 'GET'])
def home():
    form = ContactMe()
    if form.validate_on_submit():
        name1, email_address1, body1 = form.name.data, form.email_address.data, form.body.data
        with smtplib.SMTP('smtp.gmail.com') as email_protocol:
            email_protocol.starttls()
            email_protocol.login(user=gmail_address, password=gmail_password)
            email_protocol.sendmail(from_addr=gmail_address, to_addrs=receiver_address,
                                    msg=f"Subject:Contact Via your Resume Page\n\n{name1} with the email address: {email_address1} says '{body1}'")
        title = 'Message Delivered'
        subtitle = 'Thank you for reaching out'
        return render_template('index.html', form=form, title=title, subtitle=subtitle)
    else:
        if request.method == 'POST':
            title = "Sorry about this"
            subtitle = 'Your message could not be delivered'
        else:
            title = "Online Resume"
            subtitle = 'Curated by Doobie'
        return render_template('index.html', form=form, title=title, subtitle=subtitle)


if __name__ == "__main__":
    app.run(debug=True)
