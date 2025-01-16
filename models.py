from datetime import datetime
from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Client(db.Model):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    credit_card: Mapped[str] = mapped_column(String(50), nullable=True)
    car_number: Mapped[str] = mapped_column(String(10), nullable=True)

    def __repr__(self):
        return f"Client {self.name} {self.surname}, credit card - {self.credit_card}, car number {self.car_number}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = "parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(100))
    opened: Mapped[bool]
    count_places: Mapped[int]
    count_available_places: Mapped[int]

    def __repr__(self):
        return f"Parking address {self.address}, opened {self.opened}, count places {self.count_places}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Client_Parking(db.Model):
    __tablename__ = "client_parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    parking_id: Mapped[int] = mapped_column(ForeignKey("parking.id"))
    time_in: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=True)
    time_out: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=True)

    UniqueConstraint("client_id", "parking_id", name="unique_client_parking")
    client = db.relationship("Client", backref="client_parking")
    parking = db.relationship("Parking", backref="client_parking")

    def __repr__(self):
        return f"Client {self.client_id} in parking {self.parking_id} from {self.time_in} until {self.time_out}"

    def to_json(self) -> Dict[str, Any]:
        json_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        json_data["parking"] = self.parking.to_json()
        json_data["client"] = self.client.to_json()
        return json_data
