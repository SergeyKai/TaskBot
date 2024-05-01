from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    tasks: Mapped[list['Task']] = relationship('Task', back_populates='user')

    def __repr__(self):
        return f'<User:: id: {self.id}>'


class Task(Base):
    __tablename__ = 'tasks'
    text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates='tasks')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self):
        return f'<Task:: id: {self.id}; user: {self.user_id}>'
