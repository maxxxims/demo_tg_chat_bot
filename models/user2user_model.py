from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, DATE, BOOLEAN, TIME, TIMESTAMP
from sqlalchemy import ForeignKey
from datetime import datetime
from settings import Base
from sqlalchemy.orm import Mapped, mapped_column


class User2User(Base):
    __tablename__ = 'users2users'

    id:                Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), 
                                                   primary_key=True, index=True)
    topic:             Mapped[str] = mapped_column(VARCHAR(50), index=True, nullable=True, default=None)
    companion:         Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"),
                                                   default=None, nullable=True)
    is_searching:      Mapped[str] = mapped_column(BOOLEAN, default=True, nullable=False)
    start_searching:   Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_activity:     Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
