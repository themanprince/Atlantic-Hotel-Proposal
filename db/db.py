from sqlalchemy import create_engine, Column, ForeignKey, Integer, Float, String, Boolean, Date, DateTime
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship
from datetime import date, datetime

DATABASE_URL = "sqlite:///./db_file.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ENTITIES
class Guest(Base):
    __tablename__ = "guest"

    guest_id = Column(Integer(), primary_key=True, index=True)
    first_name = Column(String())
    last_name = Column(String())
    date_of_birth = Column(Date())
    address = Column(String())
    phone = Column(String())
    email = Column(String())
    next_of_kin_name = Column(String())
    next_of_kin_phone_number = Column(String())
    married = Column(Boolean())


class RoomType(Base):
    __tablename__ = "room_type"

    room_type_id = Column(Integer(), primary_key=True, index=True)
    room_type_name = Column(String(), index=True)
    description = Column(String())
    price = Column(Float())
    capacity = Column(Integer())

    rooms = relationship("Room", back_populates="room_type")


class Room(Base):
    __tablename__ = "room"

    room_number = Column(Integer(), primary_key=True, index=True)
    room_type_id = Column(Integer(), ForeignKey("room_type.room_type_id"))
    available = Column(Boolean())

    room_type = relationship("RoomType", back_populates="rooms", uselist=False)


class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer(), primary_key=True, index=True)
    guest_id = Column(Integer(), ForeignKey("guest.guest_id"))
    room_number = Column(Integer(), ForeignKey("room.room_number"))
    price = Column(Float())
    check_in_date = Column(Date(), default=date.today)
    check_out_date = Column(Date())
    payment_id = Column(Integer(), ForeignKey("Payment")) #this column can be used to ascertain payment status for this column i.e. if null, then payment has not been made

    guest = relationship("Guest")
    room = relationship("Room")
    payment = relationship("Payment", backref="booking", uselist=False)


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer(), primary_key=True, index=True)
    booking_id = Column(Integer(), ForeignKey("booking.booking_id"))
    amount = Column(Float())
    payment_timestamp = Column(DateTime(), default=datetime.now())
    payment_method = Column(String())

    booking = relationship("Booking", backref="payment", uselist=False)



Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()