from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dummy_users.models import dummy_users as user_models
from app.dummy_users.schema import requests as user_requests_schema
from app.dummy_users.schema import response as user_response_schema
from utils.dependencies.database import get_db
from utils.schema.response import ExceptionResponseSchema

dummy_users_router = APIRouter()


@dummy_users_router.post(
    "/",
    response_model=user_response_schema.DummyUsersResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(
    payload: user_requests_schema.DummyUserRequestSchema, db: Session = Depends(get_db)
):
    new_user = user_models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@dummy_users_router.get(
    "/",
    response_model=List[user_response_schema.DummyUsersResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(user_models.User).all()
    return users


@dummy_users_router.patch(
    "/{user_id}/",
    response_model=user_response_schema.DummyUsersResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_user(
    user_id: int,
    payload: user_requests_schema.DummyUserRequestSchema,
    db: Session = Depends(get_db),
):
    user_query = db.query(user_models.User).filter(user_models.User.id == user_id)
    user = user_query.first()

    # Raise exception if user with provided id not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with this id: {user_id} found",
        )
    update_data = payload.dict(exclude_unset=True)
    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user


@dummy_users_router.delete(
    "/{user_id}/",
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(user_models.User).filter(user_models.User.id == user_id)
    user = user_query.first()

    # Raise exception if user with provided id not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with this id: {user_id} found",
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_200_OK, content="User deleted successfully")
