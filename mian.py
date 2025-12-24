from fastapi import FastAPI

app = FastAPI(
    title="Patient Managemnt System BE",
    version="0.0.1",
    description="This contains the backend logic for the Patient Managemnt Syste build with ptython (FastAPI)"
)

@app.get("/status")
def server_status_check():
    return "Server is up and running..."