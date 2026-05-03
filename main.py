from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user_authenication.auth_router import auth_router
from docter.router import docter_endpoint
from patient.router import  patient_endpoint
from users.user_router import user_endpoint
from appointments.app_router import appointment_endpoint
from next_of_kin.kin_router import kin_endpoint
from Queue_.q_route import queue_endpoint

app = FastAPI(
    title="Patient Managemnt System BE",
    version="0.0.1",
    description="This contains the backend logic for the Patient Managemnt System build with ptython (FastAPI)"
)

origin = ["http://localhost:5173","http://localhost:5173/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def server_status_check():
    return "Server is up and running..."

app.include_router(auth_router)
app.include_router(docter_endpoint)
app.include_router(patient_endpoint)
app.include_router(kin_endpoint)
app.include_router(user_endpoint)
app.include_router(appointment_endpoint)
app.include_router(queue_endpoint)