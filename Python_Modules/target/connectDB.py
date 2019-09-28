import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
import numpy

#### Function to connect to walmart inventory Database and fetch data.
def connect_db(sql):
    rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    return engine.execute(sql).fetchall()

#### Function to connect to target inventory database and fetch data.
def connect_target_db(sql):
    rds_connection_string = "xsexllfzorcrvb:c19fdb9e7f8b1d787fd0aa79c53c274bd6b25e57c89b6d0981f8b6ad293a5c80@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dbvr413t8b1dv6"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    return engine.execute(sql).fetchall() 

            


