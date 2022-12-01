from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, db_conn


router = APIRouter(
    prefix="/team",
    tags=["Teams"]
)


def is_token_id_from_the_same_user(token_data: schemas.TokenData, user_id: int):
    id_from_token = token_data.id
    return id_from_token and int(id_from_token) != user_id


@router.get("/{team_id}", response_model=schemas.TeamDetails)
def get_team(team_id: int, db: Session = Depends(db_conn.get_db)):
    team_data = db.query(models.Teams).filter(models.Teams.id == team_id).first()

    if not team_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found"
        )

    return team_data


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TeamDetails)
def create_team(user_id: int, team: schemas.TeamCreate, db: Session = Depends(db_conn.get_db)):
    """
    [summary]:
    """
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    team.team_name = user_profile.team_name

    new_team = models.Teams(**team.dict())
    try:
        db.add(new_team)
        db.commit()
        db.refresh(new_team)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Team already exits')

    return new_team


@router.put("/{team_id}", status_code=status.HTTP_201_CREATED)
def update_team(team_id: int, request: schemas.TeamUpdate, db: Session = Depends(db_conn.get_db)):
    """
    [summary]:
    """
    update_team_query = db.query(models.Teams).filter(models.Teams.id == team_id)
    current_team = update_team_query.first()

    if not current_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")
    else:
        updated_req_dict = dict()
        for k, v in vars(request).items():
            if v is not None:
                updated_req_dict[k] = v
        print("updated_req_dict: {0}".format(updated_req_dict))

        update_team_query.update(updated_req_dict)

        db.commit()

    return current_team
