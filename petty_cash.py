import os
from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify, Response

# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()

# class pettyCash(Base):
#     __tablename__ = "pettyCash"
#     id = Column(Integer, primary_key=True)
#     date = Column(String)
#     receipt_number = Column(Integer)
#     description = Column(String)
#     amount_deposited = Column(Integer)
#     amount_withdrawn = Column(Integer)
#     amount_receivedby = Column(String)
#     amount_approvedby = Column(String)
#     comments = Column(String)

# engine = create_engine("sqlite:///petty_cash.sqlite")
# Base.metadata.create_all(engine)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('petty_cash.html')

@app.route('/submit', methods=['POST'])
def submit():

    # session = Session(engine)

    expDate = request.form['expDate']
    expReceipt = request.form['expReceipt']
    expDescr = request.form['expDescr']
    expAmountDep = request.form['expAmountDep']
    expAmountWith = request.form['expAmountWith']
    expReceived = request.form['expReceived']
    expApproved = request.form['expApproved']
    expComments = request.form['expComments']


    if expDate:
        session.add(pettyCash(date=expDate, receipt_number=expReceipt,\
            description=expDescr, amount_deposited=expAmountDep,\
                amount_withdrawn=expAmountWith, amount_receivedby=expReceived,\
                    amount_approvedby=expApproved, comments=expComments))
        session.commit()
        newDate = expDate[::-1]
        return jsonify({'message': newDate})

    return jsonify({'error': 'Missing data!'})


    
    

if __name__ == '__main__':
    app.run(debug=True)