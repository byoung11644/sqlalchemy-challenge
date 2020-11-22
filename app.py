

# Create an `app.py`, and make the necessary imports.

from flask import Flask, jsonify, url_for
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

from ipynb.fs.full.climate_analysis import *

app = Flask(__name__)

from app import app

@app.route("/")
def index():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    date_list = [element[0] for element in precip_query]
    precip_list = [element[1] for element in precip_query]
    precip_dict = dict(zip(date_list, precip_list))
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():

    return jsonify(stations_df['Station'])

@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement


    tobs_query = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                filter(Measurement.station == stations_df['Station'][0]).\
                filter(Measurement.date >= year_query_date).all()
    session.close()
    return jsonify(tobs_query)

@app.route("/api/v1.0/<start>")
def start(start):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement

    start_date = dt.date(start)

    TMIN = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).all()
    TMAX = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).all()
    TAVG = session.query(Measurement.station, Measurement.date, func.avg(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).all()
    
    session.close()
    return jsonify(TMIN, TMAX, TAVG)

@app.route("/api/v1.0/<start>/<end>")
def duration(start, end):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement

    start_date = dt.date(start).strftime('%Y-%m-%d')
    end_date = dt.date(end).strftime('%Y-%m-%d')

    DMIN = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    DMAX = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    DAVG = session.query(Measurement.station, Measurement.date, func.avg(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    
    session.close()
    return jsonify(DMIN, DMAX, DAVG)




if __name__ == "__main__":
    app.run(debug=True)
