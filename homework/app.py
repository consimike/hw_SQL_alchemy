import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def hi():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )
################

@app.route("/api/v1.0/precipitation")

def precipitation():
    """Precipitation Values"""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    

    first_date =  dt.date(2017,8,23) - dt.timedelta(days=365)

    sel = [Measurement.date, 
       Measurement.prcp]
   
    range_last12 = session.query(*sel).\
    filter(Measurement.date >=first_date).\
    order_by(Measurement.date).all()
    
    precip = []

    for date,prcp in range_last12:
        precipe = {}
        precipe["date"] = date
        precipe["prcp"] = prcp
        precip.append(precipe)

    return jsonify(precip)

##########

@app.route("/api/v1.0/stations")

def stations():

    "All Stations Listed Below"

    stationss = session.query(Measurement.station).\
    distinct().count()

    return jsonify(f"There are: {stationss} stations")

#########

@app.route("/api/v1.0/tobs")

def tobs():
    "Temperature from the last year, all stations"

    first_date =  dt.date(2017,8,23) - dt.timedelta(days=365)

    active_station = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= first_date).all()

    tempp = []

    for date,tobs in active_station:
        temperaturess = {}
        temperaturess['date'] = date
        temperaturess['tobs'] = tobs
        tempp.append(temperaturess)

    return jsonify(tempp)


@app.route ("/api/v1.0/<start>")

def trip(start):
    "Temp min, Temp max, Temp avg"

    trip_weather = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    trips = []

    for tobs in trip_weather:
        tripsss = {}
        tripsss['tobs'] = tobs
        trips.append(tripsss)

    return jsonify(trips)


@app.route("/api/v1.0/<start>/<end>")

def trippy(start,end):
    "Temp min, Temp max, Temp avg"

    trip_weather = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date<= end).\
        all()

    trips = []

    for tobs in trip_weather:
        tripsss = {}
        tripsss['tobs'] = tobs
        trips.append(tripsss)

    return jsonify(trips)




if __name__ == '__main__':
    app.run(debug=True)
