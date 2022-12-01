from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, db_conn


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.UserCreate, db: Session = Depends(db_conn.get_db)):
    new_user = models.User(**request.dict())
    try:
        db.add(new_user)
        # profile.create_default_profile(new_user.id, db)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User account {request.username} already exits')

    return new_user


# @router.get('/{user_id}', response_model=schemas.ShowUser)
# def get_user_by_id(user_id: int, db: Session = Depends(db_conn.get_db)):
#     get_user = db.query(models.User).filter(models.User.id == user_id).first()
#
#     if not get_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id {0} is not available".format(user_id))
#
#     return get_user

@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_user_by_id(user_id: int, db: Session = Depends(db_conn.get_db)):
    get_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id {0} is not available".format(user_id))

    return get_user
