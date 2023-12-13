# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_str = last_date[0]
    date_object = datetime.strptime(date_str, '%Y-%m-%d')
    one_year_ago = date_object - timedelta(days=365)
    formatted_result = one_year_ago.strftime('%Y-%m-%d')
    year_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= formatted_result, Measurement.prcp != None).\
    order_by(Measurement.date).all()
    return jsonify(dict(year_prcp))


@app.route("/")
def welcome():
    return (f"welcome page <br/>"
           
           f" routes <br/>"
           
           f"/api/v1.0/precipitation <br/>"
           
           f"/api/v1.0/stations <br/>"
           
           f"/api/v1.0/tobs <br/>")
           

    

@app.route("/api/v1.0/stations")

def station():
    result = session.query(Station.station).all()
    st_list = list(np.ravel(result))
    return jsonify (st_list)



@app.route("/api/v1.0/tobs")

def tobs():
    tobss = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobss))
    return jsonify (tobs_list)



@app.route ("/api/v1.0/<start>/<end>")

def temps(start,end):
    findings = session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found =[] 
    for row in findings:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
           
            

if __name__ == "__main__":
   app.run(debug=True)




#################################################
# Flask Routes
#################################################
