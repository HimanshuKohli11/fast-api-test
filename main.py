from fastapi import FastAPI
from blog import models
from blog.db_conn import engine
from blog.routers import user, profile, login, player, team, game


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


# app routers
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(login.router)
app.include_router(player.router)
app.include_router(team.router)
app.include_router(game.router)


@app.get("/", status_code=200)
def get_user():
    return {'message': 'Success'}
