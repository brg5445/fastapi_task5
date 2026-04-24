from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.locations import LocationRepository
from ....schemas.locations import LocationOut, LocationUpdateAndCreate

from src.core.exceptions.domain_exceptions import LocationNotFoundByNameException, LocationIsNotUniqueException
from src.core.exceptions.database_exceptions import LocationNotFoundException, LocationAlreadyExistsException


class MethodsForLocation:
    def __init__(self):
        self._repo = LocationRepository()

    def get(self, DataBase: Session, skip: int, limit: int) -> List[LocationOut]:
        return [LocationOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, name: str) -> LocationOut:
        try:
            location_model = self._repo.get_detail(DataBase, name)
        except LocationNotFoundException:
            raise LocationNotFoundByNameException(name)
        return LocationOut.model_validate(location_model)

    def create(self, DataBase: Session, payload: LocationUpdateAndCreate) -> LocationOut:
        try:
            location_model = self._repo.create(DataBase, payload)
        except LocationAlreadyExistsException:
            raise LocationIsNotUniqueException(payload.name)
        return LocationOut.model_validate(location_model)

    def update(self, DataBase: Session, name: str, payload: LocationUpdateAndCreate) -> LocationOut:
        try:
            location_model = self._repo.update(DataBase, name, payload)
        except LocationNotFoundException:
            raise LocationNotFoundByNameException(name)
        except LocationAlreadyExistsException:
            raise LocationIsNotUniqueException(payload.name)
        return LocationOut.model_validate(location_model)
    
    def destroy(self, DataBase: Session, name: str):
        try:
            self._repo.destroy(DataBase, name)
        except LocationNotFoundException:
            raise LocationNotFoundByNameException(name)