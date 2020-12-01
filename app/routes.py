import os
import secrets
from PIL import Image
import xlsxwriter
from app import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request, jsonify, send_file
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewHireForm, NewHireFilterForm, PettyCashForm, PettyCashFilterForm
from app.models import User, NewHire, PettyCashExp, PettyCashExpSchema
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
      if old_picture_fn != "default.png":
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

@app.route("/new_hires", methods=['GET', 'POST'])
def new_hires():
  new_hires = NewHire.query.all()
  form = NewHireFilterForm()
  if form.validate_on_submit():
    if form.from_date.data and form.to_date.data != "":
      new_hires = NewHire.query.filter(NewHire.date_entered >= form.from_date.data).\
        filter(NewHire.date_entered <= form.to_date.data).order_by(NewHire.date_entered.desc()).all()
  return render_template('new_hires.html', new_hires=new_hires, form=form)

@app.route("/new_hire/<int:newhire_id>/delete", methods=['POST'])
def delete_new_hire(newhire_id):
  new_hire = NewHire.query.get_or_404(newhire_id)
  db.session.delete(new_hire)
  db.session.commit()
  return redirect(url_for('new_hires'))

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
  filter_form = PettyCashFilterForm()
  return render_template("petty_cash.html", form=form, filter_form=filter_form)

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
    # if form.receipt.data:
      # receipt = form.receipt.data
      # print(receipt.filename)
      # random_hex = secrets.token_hex(8)
      # f_ext = os.path.splitext(form.receipt.data.filename)[1]
      # receipt_fn = random_hex + f_ext
      # receipt_path = os.path.join(app.root_path, 'static/receipts', receipt_fn)
      # receipt.save(receipt_path)
      # pettycash_exp.receipt = receipt_fn
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

@app.route("/petty_cash/filter", methods=['POST'])
def petty_cash_filter():
  form = PettyCashFilterForm()
  if form.validate_on_submit():
    results = PettyCashExp.query.filter(PettyCashExp.date >= form.from_date.data).\
      filter(PettyCashExp.date <= form.to_date.data).order_by(PettyCashExp.date.desc()).all()
    
    workbook = xlsxwriter.Workbook('app/static/users/petty_cash_reports/petty_cash_report.xlsx')
    date_format = workbook.add_format({'num_format': 'mm/dd/yy'})
    worksheet = workbook.add_worksheet()

    columns = PettyCashExp.__table__.columns.keys()
    for i in range(len(columns)):
      excel_col = chr(ord('A') + i)
      worksheet.write(f'{excel_col}1', columns[i])

    for i in range(len(results)):
      row_no = 2 + i
      worksheet.write(f'A{row_no}', results[i].id)
      worksheet.write(f'B{row_no}', results[i].date, date_format)
      worksheet.write(f'C{row_no}', results[i].receipt_no)
      worksheet.write(f'D{row_no}', results[i].description)
      worksheet.write(f'E{row_no}', results[i].amount_deposited)
      worksheet.write(f'F{row_no}', results[i].amount_withdrawn)
      worksheet.write(f'G{row_no}', results[i].received_by)
      worksheet.write(f'H{row_no}', results[i].approved_by)
      worksheet.write(f'I{row_no}', results[i].comments)
      worksheet.write(f'J{row_no}', results[i].receipt)
      worksheet.write(f'K{row_no}', results[i].date_entered, date_format)
      worksheet.write(f'L{row_no}', results[i].user_id)      

    workbook.close()
    
    schema = PettyCashExpSchema(many=True)
    output = schema.dump(results)    

    return jsonify(output)
  return jsonify(errors=form.errors)

@app.route("/petty_cash/download", methods=['GET'])
def petty_cash_download():
  print("hello")
  file_path = os.path.join(app.root_path, 'static/users/petty_cash_reports/petty_cash_report.xlsx')
  return send_file(file_path, as_attachment=True)
  