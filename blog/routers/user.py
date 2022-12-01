from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, db_conn


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(db_conn.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_user_by_id(user_id: int, db: Session = Depends(db_conn.get_db)):
    get_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id {0} is not available".format(user_id))

    return get_user
