# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

#establishing MetaData to contain all of the Schema constructs
metadata = MetaData()

# reflect an existing database into a new model
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base(metadata.reflect(engine))

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################

# Calculate the date one year from the last date in data set.
most_recent_dt = dt.datetime.strptime(recent_date[0],'%Y-%m-%d')
year_from_recent_dt = dt.date(most_recent_dt.year - 1, most_recent_dt.month, most_recent_dt.day)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def api_routes():
        return (
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
        )
    
@app.route('/api/v1.0/precipitation')
def precipitation():
    #Create our session
    session = Session(engine)
    
    # Perform a query to retrieve the data and precipitation scores
    measurement_table = [Measurement.date,Measurement.prcp]
    measurement_query = session.query(*measurement_table).\
        filter(Measurement.date >= year_from_recent_dt).all()
    session.close()
    
    #Convert list to Dictionary
    prcp_list = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)
    
@app.route('/api/v1.0/stations')
def stations():
    #Create our session
    session = Session(engine)
    
    # Perform a query to retrieve the station data
    station_table = [Station.date]
    station_query = session.query(*station_table).\
        order_by(Station.station).all()
    session.close()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
  
    return jsonify(prcp_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Perform a query to retrieve the TOBS data
    tobs_table = [Measurement.date, Measurement.tobs, Measurement.prcp]
    tobs_query = session.query(*tobs_table).\
        filter(Measurement.date >= year_from_recent_dt).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    
    session.close()
    
    #Convert list to Dictionary
    tobs_list = []
    for date,prcp,tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['prcp'] = prcp
        tobs_dict['tobs'] = tobs
        
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

    

@app.route('/api/v1.0/<start>')
def temp_start(start):
    session = Session(engine)
    queryresult = session.\
        query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
  
    tobs_list = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>/<stop>')
def temp_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query.\
        (func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    
    session.close()

    tobs_list = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)