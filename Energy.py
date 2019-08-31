from flask import Flask, request
from flask_restful import Resource, Api

from flask_restful import reqparse

from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

from flasgger import Swagger
from flasgger.utils import swag_from
from flask_restful_swagger import swagger
import requests
import ast
import pandas as pd


app = Flask(__name__)
api = Api(app)


limiter = Limiter(app,key_func=get_remote_address)
limiter.init_app(app)

api = swagger.docs(Api(app), apiVersion='1', api_spec_url="/doc")

class MyAPI(Resource):

    decorators = [limiter.limit("100/day")]
    @swagger.model
    @swagger.operation(notes='some really good notes')

    def get(self, state="Connecticut"):
        if len(state) >2:
            obj = Master()
            data = obj.get(state=state)
            return data
        else:
            return "Error"


class Master(object):
    def __init__(self):
        pass

    def get(self, state="Connecticut"):
        """
        Input: Takes a string Usually String
        Return: Json Data
        """

        columns=['State', 'Residential-2019', 'Residential-2018', 'Commercial-2019',
       'Commercial.2018', 'Industrial-2019', 'Industrial.2018', 'Transportation-2019',
       'Transportation-2018', 'All Sectors-2019', 'All Sectors-2018']

        df = pd.read_html("https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a", header=0)[1][1:].set_axis(columns, axis=1, inplace=False).sort_values(by=["State"])
        tem = df[df["State"]== state]
        my_data = tem.to_json()
        data_json = ast.literal_eval(my_data)
        return data_json

    def get_all(self):
        df = pd.read_html("https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a", header=0)[1][1:].set_axis(columns, axis=1, inplace=False).sort_values(by=["State"])
        my_data = df.to_json()
        data_json = ast.literal_eval(my_data)
        return data_json



api.add_resource(MyAPI, '/rate/<string:state>')

if __name__ == '__main__':
    app.run(debug=True)
