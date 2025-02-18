from fastapi import FastAPI

from app.api.auth.router import router as auth_router

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(auth_router)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
