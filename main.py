from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from NwdafRow import NwdafRow, NwdafRowList
import numpy as np
import uvicorn
from skforecast.utils import load_forecaster
import pandas as pd
import json
from pydantic.tools import parse_obj_as
import plotly.express as px
import plotly
import plotly.graph_objects as go

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

file_name = '000_multi_serie_forecaster.pickle'
forecaster = load_forecaster(file_name, verbose=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post('/lag/10/predict')
# def predict_car_type(data: NwdafRowList):
#     return {
#         'prediction': data
#     }

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, input_data: str = Form(...), steps: str = Form()):
    # Assume the input_data is a JSON string representing an array of objects
    parsed_data = json.loads(input_data)
    # data_model = NwdafRowList(**parsed_data)
    # NwdafRowList.__pydantic_model__.parse_raw(parsed_data)
    # user = parse_obj_as(NwdafRowList, parsed_data)
    # print(parsed_data)
    df = pd.DataFrame.from_records(parsed_data)
    print(df)
    print(steps)
    
    # prediction = model_predict(input_array)
    # predictions = forecaster.predict(steps=steps, exog=exog)

    fig = px.scatter(x=range(10), y=range(10))
    graph_html  =  plotly.io.to_html(fig, full_html=False, include_plotlyjs ='cdn' )
    return templates.TemplateResponse("index.html", {"request": request, "graph_html": graph_html })

# def model_predict(steps=steps, exog=exog):
#     predictions = forecaster.predict(steps=steps, exog=exog)
#     return predictions

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1')