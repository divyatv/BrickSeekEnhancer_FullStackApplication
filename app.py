import os
import numpy
import pandas as pd

import sqlalchemy

from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import Session

from sqlalchemy.ext.automap import automap_base

from sqlalchemy import create_engine, inspect


rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
engine = create_engine(f'postgresql://{rds_connection_string}')

# inspector = inspect(engine)
# columns = inspector.get_columns('zip')
# for column in columns:
#     print(column)

# zip=[engine.execute('select zip from city_zip_data')]
# for i in zip:
#  print(i)

# Make db calls



sku=625412161
zip=[27713]

# cmd='curl --url https://brickseek.com/walmart-inventory-checker?sku=625412161&zip=27713 >> output.html'
# #http://brickseek.com/walmart-inventory-checker/?sku={}'.format(str(SKU)), 
# os.system(cmd)

for item in zip:
 cmd='curl --data "sku=${sku}&zip=${zip}" https://brickseek.com/walmart-inventory-checker >> output.html'
 os.system(cmd)

