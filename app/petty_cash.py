import os
from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify, Response, send_from_directory, abort
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class pettyCash(Base):
    __tablename__ = "pettyCash"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    receipt_number = Column(Integer)
    description = Column(String)
    amount_deposited = Column(Integer)
    amount_withdrawn = Column(Integer)
    amount_receivedby = Column(String)
    amount_approvedby = Column(String)
    comments = Column(String)

engine = create_engine("sqlite:///petty_cash.sqlite")
Base.metadata.create_all(engine)


app = Flask(__name__)

app.config["PETTY_CASH_LOGS"] = "C:/Users/Remco/tmt/team-wilson-website/static/logs"

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/petty_cash')
def petty_cash():
    
    # remove any previously downloaded logs
    log_files = os.listdir('static/logs')
    if log_files:
        for log in log_files:
            os.remove(os.path.join(app.config["PETTY_CASH_LOGS"], log))

    session = Session(engine)

    form_data = session.query(pettyCash)

    return render_template('petty_cash.html', form_data=form_data)

@app.route('/submit', methods=['POST'])
def submit():

    session = Session(engine)

    expDate = request.form['expDate']
    expReceipt = request.form['expReceipt']
    expDescr = request.form['expDescr']
    expAmountDep = request.form['expAmountDep']
    expAmountWith = request.form['expAmountWith']
    expReceived = request.form['expReceived']
    expApproved = request.form['expApproved']
    expComments = request.form['expComments']


    if (expDate and expReceipt and expDescr and expReceived and expApproved)\
        and (expAmountDep or expAmountWith):

        session.add(pettyCash(date=expDate, receipt_number=expReceipt,\
            description=expDescr, amount_deposited=expAmountDep,\
                amount_withdrawn=expAmountWith, amount_receivedby=expReceived,\
                    amount_approvedby=expApproved, comments=expComments))
        session.commit()

        return jsonify({'transDate': expDate,
                        'receipt': expReceipt,
                        'descr': expDescr,
                        'amountDep': expAmountDep,
                        'amountWith': expAmountWith,
                        'received': expReceived,
                        'approved': expApproved,
                        'comments': expComments})

    else:
        return jsonify({'error': 'Missing data!'})

@app.route('/filter', methods=['POST'])
def filter():
    
    session = Session(engine)

    fromDate = request.form['fromDate']
    toDate = request.form['toDate']

    # query and return results between 'from date' and 'to date'
    if (fromDate and toDate):
        results = session.query(pettyCash.date, pettyCash.receipt_number, pettyCash.description,\
                        pettyCash.amount_deposited, pettyCash.amount_withdrawn, pettyCash.amount_receivedby,\
                        pettyCash.amount_approvedby, pettyCash.comments)\
                        .filter(pettyCash.date >= fromDate).filter(pettyCash.date <= toDate).order_by(pettyCash.date).all()
        
        # remove any previously downloaded logs
        log_files = os.listdir('static/logs')
        if log_files:
            for log in log_files:
                os.remove(os.path.join(app.config["PETTY_CASH_LOGS"], log))

        # export query results to excel
        results_df = pd.DataFrame(results)
        results_df.to_excel('static/logs/output.xlsx', index=False)

        return jsonify({'result': results})

    # elif fromDate:

    else:
        return jsonify({'error': 'Missing data!'})


@app.route('/download')
def download():

    log_files = os.listdir('static/logs')
    for log in log_files:
        try:
            return send_from_directory(
                directory=app.config["PETTY_CASH_LOGS"], filename=log, as_attachment=True
                )
        except FileNotFoundError:
            abort(404)
  
    
if __name__ == '__main__':
    app.run(debug=True)