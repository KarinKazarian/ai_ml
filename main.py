from fastapi import FastAPI, Request, Form, Body, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import uvicorn
from skforecast.utils import load_forecaster
import pandas as pd
# from pydantic.tools import parse_obj_as
import plotly.express as px
import plotly
import plotly.graph_objects as go
import csv
from io import StringIO
from utils import get_multi_series_data, get_prediction, get_plot_html

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, input_data: UploadFile = File(...), steps: str = Form()):
    content = await input_data.read()

    # Convert the file content to a StringIO object (which pandas can read)
    stringio = StringIO(content.decode('utf-8'))

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(stringio)
    
    # format the data
    df_formatted,_ = get_multi_series_data(df)

    # print(_)
    for key, dff in df_formatted.items():
        print(f"Series ID: {key}, Frequency: {dff.index.freq}")
    # print(df_formatted.index.freq )
    prediction= get_prediction(df_formatted, int(steps))

    graph_html = get_plot_html(prediction)
    return templates.TemplateResponse("index.html", {"request": request, "graph_html": graph_html })

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)