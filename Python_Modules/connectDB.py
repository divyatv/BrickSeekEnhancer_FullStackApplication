import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect

#### Function to connect to walmart inventory Database and fetch data.
def connect_db(sql):
    rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    return engine.execute(sql).fetchall()

#### Function to connect to target inventory database and fetch data.
def connect_target_db(sql):
    rds_connection_string = "postgres://wyscmkyadpxnpq:4035077d37da67ed9b5c3f7d5a1560ed3adfda8c7e7a875df5139b38e8e5561e@ec2-54-83-201-84.compute-1.amazonaws.com:5432/d77gdrm2h45ur9"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    return engine.execute(sql).fetchall()            

            


