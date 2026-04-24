from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.location_models import LocationModel
from ....schemas.locations import LocationUpdateAndCreate

from src.core.exceptions.database_exceptions import LocationNotFoundException, LocationAlreadyExistsException

class LocationRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, skip: int, limit: int) -> List[LocationModel]:
        return DataBase.query(LocationModel).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, name: str) -> LocationModel:
        location = DataBase.query(LocationModel).filter(
            LocationModel.name == name
        ).first()
        if not location:
            raise LocationNotFoundException()
        return location

    def create(self, DataBase: Session, payload: LocationUpdateAndCreate) -> LocationModel:
        location = LocationModel(**payload.model_dump())
        try:
            DataBase.add(location)
            DataBase.commit()
        except IntegrityError:
            raise LocationAlreadyExistsException()
        DataBase.refresh(location)
        return location

    def update(self, DataBase: Session, name: str, payload: LocationUpdateAndCreate) -> LocationModel:
        location = DataBase.query(LocationModel).filter(
            LocationModel.name == name
        ).first()
        if not location:
            raise LocationNotFoundException()
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(location, field, value)
        try:
            DataBase.commit()
        except IntegrityError:
            raise LocationAlreadyExistsException()
        DataBase.refresh(location)
        return location

    def destroy(self, DataBase: Session, name: str):
        location = DataBase.query(LocationModel).filter(
            LocationModel.name == name
        ).first()
        if not location:
            raise LocationNotFoundException()
        DataBase.delete(location)
        DataBase.commit()