import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station=Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
     """Return a list of precipitation for prior year"""
     
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).order_by(Measurement.date).all()
    
    precipitation = list(np.ravel(results))
	
   	return jsonify(precipitation)
   	
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations_list = []
    for result in stations_query:
        stations_list.append(result)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date>start_date).\
                order_by(Measurement.date).all()
    tobs_list = []
    for result in tobs_data:
        tobs_list.append(result)
    return jsonify(tobs_list)


@app.route("/api/v1.0/start/end")
def start_end():
    def calc_temps(start_date, end_date):
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <=end_date).all()
    start_date = dt.date(2017, 4, 1)
    end_date = dt.date(2017, 4, 8)
    temp_range = calc_temps(start_date, end_date)
    return jsonify( temp_range)

if __name__ == "__main__":
    app.run(debug=True)