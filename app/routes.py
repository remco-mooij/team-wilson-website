import os
import secrets
from PIL import Image
from app import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request, jsonify
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewHireForm, PettyCashForm
from app.models import User, NewHire, PettyCashExp
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Your account was created successfully! You are now able to log in', 'success')
    return redirect(url_for('login'))
  return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next = request.args.get('next')
      return redirect(next) if next else redirect(url_for('home'))
    else:
      flash('Login unsuccessful. Please check email and password', 'danger')
  return render_template("login.html", form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_ext = os.path.splitext(form_picture.filename)[1]
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/users/profile_pics', picture_fn)

  i = Image.open(form_picture)
  i.thumbnail((125, 125))
  i.save(picture_path)

  return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      old_picture_fn = current_user.image_file
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
      # remove old profile picture
      old_picture_path = os.path.join(app.root_path, 'static/users/profile_pics', old_picture_fn)
      os.remove(old_picture_path)
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename='users/profile_pics/' + current_user.image_file)
  return render_template('account.html', form=form, image_file=image_file)

@app.route("/new_hires")
def new_hires():
  new_hires = NewHire.query.all()
  return render_template('new_hires.html', new_hires=new_hires)

@app.route("/enter_new_hire", methods=['GET', 'POST'])
@login_required
def enter_new_hire():
  form = NewHireForm()
  if form.validate_on_submit():
      newhire = NewHire(first_name=form.first_name.data, last_name=form.last_name.data,\
                          position=form.position.data, pay_rate=form.pay_rate.data,\
                          hire_date=form.hire_date.data, start_date=form.start_date.data,\
                          wisely_no=form.wisely_no.data, user=current_user)
      db.session.add(newhire)
      db.session.commit()
      flash('New hire was entered successfully!', 'success')
      return redirect(url_for('new_hires'))
  return render_template('enter_new_hire.html', form=form)

@app.route("/petty_cash")
def petty_cash():
  form = PettyCashForm()
  return render_template("petty_cash.html", form=form)

@app.route("/petty_cash/submit", methods=['POST'])
def petty_cash_submit():
  form = PettyCashForm()
  if form.validate_on_submit():
    pettycash_exp = PettyCashExp(date=form.date.data, receipt_no=form.receipt_no.data,\
                                  description=form.description.data, amount_deposited=form.amount_deposited.data,\
                                  amount_withdrawn=form.amount_withdrawn.data, received_by=form.received_by.data,\
                                  approved_by=form.approved_by.data, comments=form.comments.data, user=current_user)
    db.session.add(pettycash_exp)
    db.session.commit()
    # add database id to object to be returned
    id = pettycash_exp.id
    form_data = form.data
    form_data['id'] = id
    print(form_data)
    return jsonify(form_data)
  return jsonify(errors=form.errors)

@app.route("/petty_cash/table_change", methods=['POST'])
def petty_cash_table_change():
  form = PettyCashForm()
  
  id = request.form['id']
  field = request.form['field']
  value = request.form['value']

  pettycashexp = PettyCashExp.query.filter_by(id=id).first()
  pettycashexp.field = value
  db.session.commit()  

  return jsonify({'data': value})