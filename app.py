from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '389c4704e2873f77fa5ecad8fe3e4046e1925c4d'

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  return render_template("register.html", form=form)

@app.route("/login")
def login():
  form = LoginForm()
  return render_template("login.html", form=form)

@app.route("/petty_cash")
def petty_cash():
  return render_template("petty_cash.html")


if __name__ == '__main__':
  app.run(debug=True)