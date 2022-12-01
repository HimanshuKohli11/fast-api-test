from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, db_conn


router = APIRouter(
    prefix="/game",
    tags=["Games"]
)


def is_token_id_from_the_same_user(token_data: schemas.TokenData, user_id: int):
    id_from_token = token_data.id
    return id_from_token and int(id_from_token) != user_id


@router.get("/")
# @router.get("/", response_model=List[input_schemas.GameList])
def get_all_game_details(db: Session = Depends(db_conn.get_db)):
    game_details = db.query(models.Games).all()

    if not game_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game list not found")

    return game_details


@router.get("/{game_id}")
# @router.get("/{game_id}", response_model=input_schemas.GameDetails)
def get_game_details(
    game_id: int,
    db: Session = Depends(db_conn.get_db)
):
    game_details = db.query(models.Games).filter(models.Games.id == game_id).first()
    print("Game details: {0}".format(vars(game_details)))

    if not game_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game {game_id} not found")

    return game_details
