from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, db_conn


router = APIRouter(
    prefix="/player",
    tags=["Players"]
)


@router.get("/{player_id}", response_model=schemas.PlayerDetails)
def get_player(
    player_id: int,
    # user_id: int,
    db: Session = Depends(db_conn.get_db)
):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    print("player name: {0}".format(player.player_name))

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player {player_id} not found")

    print("Player details : {0}".format(vars(player)))
    return player
