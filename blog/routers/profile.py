import random
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, db_conn


router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)


def construct_profile(user, user_profile):
    """
    [summary]: constructs the profile object for returning to the client
    """
    profile = {**vars(user_profile), **vars(user)}
    print("profile: {0}".format(profile))
    profile["name"] = profile["first_name"] + " " + profile["last_name"]
    print("success")
    return profile


@router.get("/{user_id}", response_model=schemas.UserProfile)
def get_profile(user_id: int, db: Session = Depends(db_conn.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Profile for {user_id} not found")

    print("queries are successful!")
    return construct_profile(user, user_profile)


def create_default_profile(user_id, db: Session):
    default_profile = get_default_profile()
    default_profile['user_id'] = user_id

    new_profile = models.Profile(**default_profile)
    try:
        db.add(new_profile)

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User profile for {user_id} already exits')


def get_default_profile():
    """
    [summary]: Method to provide default profile information
    """
    profile = {}
    try:
        profile['team_name'] = 'Dream Team ' + str(random.randint(10, 100))
        profile['address'] = 'Somewhere in India'
        print("Default profile successfully created!")

    except Exception as e:
        print("Exception in get_default_profile: {0}".format(e))

    return profile


@router.put("/{user_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.ProfileUpdate)
def update_profile(user_id: int, response: schemas.ProfileUpdate, db: Session = Depends(db_conn.get_db)):
    """
    [summary]: Endpoint to use for the creation as well as updation of user profile
    """
    update_query = db.query(models.Profile).filter(models.Profile.user_id == user_id)
    current_profile = update_query.first()

    if not current_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile {user_id} not found")
    else:
        updated_req_dict = dict()
        for k, v in vars(response).items():
            if v is not None:
                updated_req_dict[k] = v

        update_query.update(updated_req_dict)
        db.commit()

    return current_profile
