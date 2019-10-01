import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect

#### Function to conect to walmart inventory and fetch data.
def connect_db(sql):
    rds_connection_string = "bedlgjelgbrcba:HIDING THE PASSWORD@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    return engine.execute(sql).fetchall()

#### Function to connect to target inventory and fetch data.
def connect_target_db(sql):
    rds_connection_string = "xsexllfzorcrvb:HIDING THE PASSWORD@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dbvr413t8b1dv6"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    return engine.execute(sql).fetchall()
      

            


