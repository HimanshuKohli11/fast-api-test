from typing import List
from uuid import uuid4, UUID
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

import models
from db_conn import SessionLocal


app = FastAPI()


class User(BaseModel):
    id: Optional[int]
    name: str
    description: str

    class Config:
        orm_mode = True


# db: List[User] = [
#     User(
#         id='1',
#         name="A",
#         description="P",
#     ),
#     User(
#         id='2',
#         name="B",
#         description="Q",
#     )
# ]
db = SessionLocal()


@app.get("/", response_model=List[User], status_code=200)
def get_user():
    # return db
    user_list = db.query(models.User).all()
    return user_list


@app.post("/creating", response_model=User, status_code=status.HTTP_201_CREATED)
def post_user(user: User):
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User already exists!")

    new_user = models.User(
        name=user.name,
        description=user.description
    )

    db.add(new_user)
    db.commit()

    return new_user


@app.put("/updating/{uid}", response_model=User, status_code=status.HTTP_200_OK)
def put_user(uid: int, user: User):
    # db.append(user)
    new_user = db.query(models.User).filter(models.User.id==uid).first()
    new_user.name = user.name
    new_user.description = user.description

    db.commit()

    return new_user
    # return {'name': user.name}


@app.delete("/deleting/{uid}")
def deleting_user(uid: int):
    db_user = db.query(models.User).filter(models.User.id == uid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User doesn't exists!")

    db.delete(db_user)
    db.commit()

    return db_user
