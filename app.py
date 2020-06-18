import os
from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify, Response, send_from_directory, abort, config

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

app.config["PETTY_CASH_LOGS"] = "C:/Users/Remco/tmt/team-wilson-website/static/logs"

@app.route('/')
def index():
    return "it works!"

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_from_directory(
            directory=app.config["PETTY_CASH_LOGS"], filename=filename, as_attachment=True
            )
    except FileNotFoundError:
        abort(404)

    
if __name__ == '__main__':
    app.run(debug=True)
