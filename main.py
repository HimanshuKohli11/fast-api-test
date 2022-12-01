from fastapi import FastAPI
from blog import models
from blog.db_conn import engine
from blog.routers import user


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(user.router)


@app.get("/", status_code=200)
def get_user():
    return {'message': 'Success'}
