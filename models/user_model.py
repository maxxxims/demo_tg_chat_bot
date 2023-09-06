from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, DATE
from datetime import datetime
from settings import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    id:                Mapped[str] = mapped_column(VARCHAR(15), primary_key=True, index=True)
    username:          Mapped[str] = mapped_column(VARCHAR(50), index=True, default=None, nullable=True)
    age:               Mapped[int] = mapped_column(INTEGER, default=None, nullable=True)
    gender:            Mapped[str] = mapped_column(VARCHAR(10), default=None, nullable=True)
    bio:               Mapped[str] = mapped_column(VARCHAR(500), default=None, nullable=True)
    registration_date: Mapped[datetime] = mapped_column(DATE, default=datetime.utcnow, nullable=False)
