#!/usr/bin/python3
""" holds class RentbncPlace"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Boolean


class RentbncPlace(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'rentbnc_places'
        city = Column(String(128), nullable=False)
        owner_email = Column(String(128), nullable=False)
        address = Column(String(128), nullable=False)
        price = Column(Float, nullable=False)
        imageUrl = Column(String(128), nullable=False)
        description = Column(String(512), nullable=False)
        is_available = Column(Boolean, default=True, nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
