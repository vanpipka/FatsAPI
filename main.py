from fastapi import FastAPI
import services as _services

app = FastAPI()
_services.create_database()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
