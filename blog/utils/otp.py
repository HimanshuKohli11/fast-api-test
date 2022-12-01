"""
[summary]: Utility to handle otp related operations
"""

from fastapi.openapi.models import OAuthFlowImplicit
from sqlalchemy.sql.functions import user
from .config import OTP_SIZE
import random

from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from ..models import Auth
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def save_otp(generated_otp: str, user_id: int, db: Session):
    """
    [summary]: saves the generated OTP in the database
    """
    existing_otp_entry = db.query(Auth).filter(Auth.id == user_id). first()

    if existing_otp_entry:
        existing_otp_entry.otp = generated_otp
        db.commit()
    else: 
        try:
            auth_entry = Auth(**{'user_id': user_id, 'otp': generated_otp})
            db.add(auth_entry)
            db.commit()
            db.refresh(auth_entry)
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Auth entry already exists for user id: {user_id}')

        return auth_entry


def trigger_otp(user_id: int, db: Session):
    """
    [summary]: Handles all the functions related to OTP generation, saving in the db, and sending it
    to the user's mobile
    """

    generated_otp = generate_otp()
    save_otp(generated_otp, user_id, db)
    send_otp(generated_otp)


def send_otp(generated_otp: str):
    """
    [summary]: send OTP to user's mobile number 
    """
    # TODO: Implement contacting AWS for sending OTP
    print(f'OTP {generate_otp} sent')
    pass


def generate_otp():
    """
    [summary]: Generates a numeric OTP of size defined by OTP_SIZE
    """
    otp = ""

    for i in range(OTP_SIZE):
        otp += str(random.randint(0, 9))

    return otp
