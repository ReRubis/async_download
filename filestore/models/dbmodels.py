import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Identity
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import (as_declarative, declarative_base,
                                        declared_attr)
from sqlalchemy.sql import func


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    # id = Column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     nullable=False,
    #     index=True
    # )

    id = Column(
        Integer,
        Identity(start=1, increment=1),
        primary_key=True,
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    removed_at = Column(DateTime(timezone=True))


class User(Base):

    username = Column(String, nullable=False, unique=True)
    hashedpassword = Column(String, nullable=False)
    current_plan = Column(String, default='default')


class SavedFile(Base):

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    file_location = Column(String)
    privacy_level = Column(String, default=None)
