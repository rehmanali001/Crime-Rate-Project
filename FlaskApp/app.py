import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/crime-rate.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
crime_rate_metadata = Base.classes.crime_rates
income_rate_metadata = Base.classes.income_rates


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/metadata/year/<year>")
def crime_rates_by_year(year):
    sel = [
        crime_rate_metadata.State,
        getattr(crime_rate_metadata, 'Y_'+year),
    ]

    results = db.session.query(*sel).all()

    sel2 = [
        income_rate_metadata.State,
        getattr(income_rate_metadata, 'Y_'+year)
    ]
    results_ir = db.session.query(*sel2).all()

    # Format the data to send as json
    data = {
        "states": [result[0] for result in results],
        "crime_rates": [result[1] for result in results],
        "income_rates": [result[1] for result in results_ir]
    }

    return jsonify(data)


@app.route("/metadata/state/<state>")
def crime_rates_by_state(state):

    stmt = db.session.query(crime_rate_metadata).statement
    ir_stmt = db.session.query(income_rate_metadata).statement

    df = pd.read_sql_query(stmt, db.session.bind)
    df_ir = pd.read_sql_query(ir_stmt, db.session.bind)

    sample_data = df.loc[df['State'] == state, :]
    sample_data_ir = df_ir.loc[df_ir['State'] == state, :]

    years = [ year.split('_')[-1] for year in sample_data.columns.values[2:]]

    crime_rates = sample_data.values[0][2:]
    income_rates = sample_data_ir.values[0][2:]

    data = {
        'year': years,
        'crime_rates': crime_rates.tolist(),
        'income_rates': income_rates.tolist()
    }

    return jsonify(data)


@app.route("/states")
def states():
    sel = [crime_rate_metadata.State]

    states = [state[0] for state in db.session.query(*sel).all()]

    return jsonify(states)


@app.route("/years")
def years():
    stmt = db.session.query(crime_rate_metadata).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    sample_data = df.loc[:,:]

    years = [year.split('_')[-1] for year in sample_data.columns.values[2:]]

    return jsonify(years)


if __name__ == "__main__":
    app.run()