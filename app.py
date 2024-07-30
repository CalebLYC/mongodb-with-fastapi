from fastapi import FastAPI, Body, HTTPException, status
from pydantic.functional_validators import BeforeValidator

from routers import auth_routes, students_routes, users_routes


app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

app.include_router(students_routes.router)
app.include_router(users_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Application with MongoDB!"}