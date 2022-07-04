from bcrypt import checkpw
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app.database import models, schemas


def register(data: schemas.UserData, db: Session):
    db_data = db.query(models.Users).filter(models.Users.login == data.login).first()
    if db_data is None:
        try:
            max_id = db.query(func.max(models.Users.id)).scalar() + 1
        except TypeError:
            max_id = 1
        data = models.Users(id=max_id, login=data.login, password=data.password, email=data.email,
                            status=False, theme="light")
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    else:
        return False


def login(user_data: schemas.UserData, db: Session):
    db_data = db.query(models.Users).filter(models.Users.login == user_data.login).first()
    if db_data is None:
        return None
    else:
        if checkpw(user_data.password.encode('utf-8'), db_data.password.encode('utf-8')):
            return db_data
        else:
            return False


def update_user(user: str, data: schemas.UpdateUser, db: Session):
    db_data = db.query(models.Users).filter(models.Users.login == user).first()
    if data.pubkey is not None:
        db_data.pubkey = data.pubkey
    db.commit()
    return True
