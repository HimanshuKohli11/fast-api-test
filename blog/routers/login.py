from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, db_conn

from ..utils import oauth2
from ..utils.encrypt_util import verify_credentials
from ..utils.otp import trigger_otp


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


# @router.post("/")
# def login(request: schemas.Login, db: Session = Depends(db_conn.get_db)):
#     """
#     [summary]: Endpoint to manage user login
#     [parameters]: username, password
#     """
#     user_account = db.query(models.User).filter(models.User.username == request.username).first()
#
#     if not user_account:
#         print("User account not found")
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#
#     id_token = oauth2.create_id_token(data={oauth2.HEADER_KEY: user_account.id})
#     refresh_token = oauth2.create_refresh_token(
#         data={oauth2.HEADER_KEY: user_account.id}
#     )
#
#     return {"id": user_account.id, "id_token": id_token, "refresh_token": refresh_token}
#
#
# @router.post("/mobile", status_code=status.HTTP_202_ACCEPTED)
# def login_mobile(user_input: schemas.Mobile, db: Session = Depends(db_conn.get_db)):
#     """
#     [summary]: Endpoint to validate user's mobile number, if the account associated with the user exists then OTP will be generated.
#                Else login will be forbidden
#     """
#     # TODO Validate mobile number using regex
#
#     user_account = db.query(models.User).filter(models.User.mobile == user_input.mobile).first()
#
#     if not user_account:
#         print("user account not found")
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=f"No account found with {user_input.mobile} mobile number",
#         )
#     else:
#         if user_account.id != user_input.id:
#             print("user account not found")
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid details"
#             )
#
#     generated_otp = trigger_otp(user_input.id, db)
#
#     return {"msg": "OTP sent", "OTP": str(generated_otp)}
#
#
# @router.get("/id_token/{user_id}")
# def get_id_token(user_id: int, db: Session = Depends(db_conn.get_db), token_data: schemas.TokenData = Depends(oauth2.verify_refresh_token)):
#     """
#     [summary]: Reissues id token provided refresh token is not expired
#     """
#     id_token = None
#     user_id_from_token = token_data.id
#
#     if user_id_from_token:
#         if int(user_id_from_token) == user_id:
#             id_token = oauth2.create_id_token(data={oauth2.HEADER_KEY: token_data.id})
#         else:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")
#
#     return {"id": user_id_from_token, "id_token": id_token}
#
#
# def validate_otp(user_credentials: schemas.OTP, db: Session = Depends(db_conn.get_db)):
#     auth_entry = db.query(models.Auth).filter(models.Auth.user_id == user_credentials.id).first()
#
#     if not auth_entry:
#         print("user authentication info not found")
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Signup attempt"
#         )
#
#     else:
#         if user_credentials.otp != auth_entry.otp:
#             # auth_entry.attempts_so_far = auth_entry.attempts_so_far + 1
#             raise HTTPException(
#                 status_code=status.HTTP_410_GONE, detail=f"Incorrect OTP"
#             )
#
#     return True
#
#
# @router.post("/signup/otp", status_code=status.HTTP_202_ACCEPTED)
# def signup_with_otp(
#     user_credentials: schemas.OTP, db: Session = Depends(db_conn.get_db),
# ):
#     auth_entry = db.query(models.Auth).filter(models.Auth.user_id == user_credentials.id).first()
#
#     if not auth_entry:
#         print("user authentication info not found")
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Signup attempt"
#         )
#
#     else:
#         if user_credentials.otp != auth_entry.otp:
#             # auth_entry.attempts_so_far = auth_entry.attempts_so_far + 1
#             raise HTTPException(status_code=status.HTTP_410_GONE, detail=f"Incorrect OTP")
#
#     otp_validation_status = validate_otp(user_credentials, db)
#
#     return {"message": "Congratulations your account is active"}
#
#
# @router.post("/otp", status_code=status.HTTP_202_ACCEPTED)
# def login_with_otp(
#     user_credentials: schemas.OTP, db: Session = Depends(db_conn.get_db),
# ):
#     otp_validation_status = validate_otp(user_credentials, db)
#
#     return {"message": "Login successful"}


@router.post("/")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_conn.get_db),
):
    """
    [summary]: Endpoint to manage user login
    [parameters]: username, password
    """

    user_account = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user_account:
        print("User account not found")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not verify_credentials(user_credentials.password, user_account.password):
        print("passwords did not match")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    id_token = oauth2.create_id_token(data={oauth2.HEADER_KEY: user_account.id})
    refresh_token = oauth2.create_refresh_token(data={oauth2.HEADER_KEY: user_account.id})

    return {"id": user_account.id, "id_token": id_token, "refresh_token": refresh_token}


@router.post("/mobile", status_code=status.HTTP_202_ACCEPTED)
def login_mobile(user_input: schemas.Mobile, db: Session = Depends(db_conn.get_db)):
    """
    [summary]: Endpoint to validate user's mobile number, if the account associated with the user exists then OTP will be generated.
               Else login will be forbidden
    """
    # TODO Validate mobile number using regex

    user_account = db.query(models.User).filter(models.User.mobile == user_input.mobile).first()

    if not user_account:
        print("user account not found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No account found with {user_input.mobile} mobile number",
        )
    else:
        if user_account.id != user_input.id:
            print("user account not found")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid details"
            )

    generated_otp = trigger_otp(user_input.id, db)

    return {"msg": "OTP sent", "OTP": str(generated_otp)}


@router.get("/id_token/{user_id}")
def get_id_token(
    user_id: int,
    db: Session = Depends(db_conn.get_db),
    token_data: schemas.TokenData = Depends(oauth2.verify_refresh_token),
):
    """
    [summary]: Reissues id token provided refresh token is not expired
    """

    id_token = None
    user_id_from_token = token_data.id

    if user_id_from_token:

        if int(user_id_from_token) == user_id:
            id_token = oauth2.create_id_token(data={oauth2.HEADER_KEY: token_data.id})
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    return {"id": user_id_from_token, "id_token": id_token}


@router.post("/signup/otp", status_code=status.HTTP_202_ACCEPTED)
def signup_with_otp(user_credentials: schemas.OTP, db: Session = Depends(db_conn.get_db)):
    otp_validation_status = validate_otp(user_credentials, db)

    return {"message": "Congratulations your account is active"}


@router.post("/otp", status_code=status.HTTP_202_ACCEPTED)
def login_with_otp(
    user_credentials: schemas.OTP, db: Session = Depends(db_conn.get_db),
):
    otp_validation_status = validate_otp(user_credentials, db)

    return {"message": "Login successful"}


def validate_otp(user_credentials: schemas.OTP, db: Session = Depends(db_conn.get_db)):
    auth_entry = db.query(models.Auth).filter(models.Auth.user_id == user_credentials.id).first()

    if not auth_entry:
        print("user authentication info not found")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Signup attempt")

    else:
        if user_credentials.otp != auth_entry.otp:
            # auth_entry.attempts_so_far = auth_entry.attempts_so_far + 1
            raise HTTPException(status_code=status.HTTP_410_GONE, detail=f"Incorrect OTP")

    return True


