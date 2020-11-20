from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from utils import bmi_classify, parse_bmi_native

app = FastAPI()

origins = ["http://localhost", "http://localhost:8080"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return "Call requests on the /native or /numpy ednpoints using post request"

@app.post("/native")
def something(request: Request, items=Form(...)):
    """
    curl -X POST "http://127.0.0.1:8000/native" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "items=[{\"Gender\":\"Male\",\"HeightCm\":171,\"WeightKg\":96},{\"Gender\":\"Male\",\"HeightCm\":161,\"WeightKg\":85},{\"Gender\":\"Male\",\"HeightCm\":180,\"WeightKg\":77},{\"Gender\":\"Female\",\"HeightCm\":166,\"WeightKg\":62},{\"Gender\":\"Female\",\"HeightCm\":150,\"WeightKg\":70},{\"Gender\":\"Female\",\"HeightCm\":167,\"WeightKg\":82}]"

    """
    data = eval(items.replace("\n", "").replace(" ", ""))
    a, b = parse_bmi_native(data)
    return f"The number of people that are Overweight are: {b}"
