from fastapi import FastAPI
from user_authenication.auth_router import auth_router

app = FastAPI(
    title="Patient Managemnt System BE",
    version="0.0.1",
    description="This contains the backend logic for the Patient Managemnt System build with ptython (FastAPI)"
)

@app.get("/status")
def server_status_check():
    return "Server is up and running..."

app.include_router(auth_router)