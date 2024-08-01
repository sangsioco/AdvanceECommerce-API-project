from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Role(Base):
    __tablename__ = "Roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)