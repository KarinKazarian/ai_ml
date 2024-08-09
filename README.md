# Deploy FastAPI on Render

Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.

See https://render.com/docs/deploy-fastapi or follow the steps below:

## Manual Steps

1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
2. Create a new Web Service on Render.
3. Specify the URL to your new repository or this repository.
4. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
5. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

6. Click Create Web Service.

Or simply click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

## Thanks

Thanks to [Harish](https://harishgarg.com) for the [inspiration to create a FastAPI quickstart for Render](https://twitter.com/harishkgarg/status/1435084018677010434) and for some sample code!

# APP
## Create the requirements.txt file
`pip freeze > requirements.txt`

## Start the Server
`uvicorn app:app`
`uvicorn app:app --reload`

## Versions
`pip install scikit-learn==1.3.2`
`pip install skforecast==0.12.0`
`pip install uvicorn fastapi joblib`
`pip install pandas==2.1.4`
`pip install plotly==5.15.0`
`pip install Jinja2`
`pip install python-multipart`

## Create python env
`python -m venv venv`
`source venv/Scripts/activate`