from sqlalchemy.orm import Session
from db.db import Room, RoomType, Booking, Guest, Payment
from fastapi import HTTPException
from sqlite3 import IntegrityError
from random import choice
from typing import Dict
from datetime import date

class AdminServices:
    @classmethod
    async def get_dashboard_statistics(cls, session: Session):
        room_types = len(session.query(RoomType).all())

        all_rooms = session.query(Room).all()
        available_rooms = len([room for room in all_rooms if room.available]) #type: ignore
        total_rooms = len(all_rooms)

        all_bookings = session.query(Booking).all()
        pending_payments = len([booking for booking in all_bookings if not booking.payment]) #type: ignore
    
        return dict(available_rooms = available_rooms, total_rooms=total_rooms, room_types=room_types, pending_payments=pending_payments)
    

    @classmethod
    async def new_room_type(cls, session: Session, room_type_name:str, description:str, price:float, capacity:int):
        
        thumbnail_urls = [
            "/static/assets/room-1.jpg",
            "/static/assets/room-2.jpg",
            "/static/assets/room-3.jpg",
        ]
        random_thumbnail_url_idx = choice([*range(len(thumbnail_urls))])
        thumbnail_img_url = thumbnail_urls[random_thumbnail_url_idx]

        try:
            session.add(RoomType(
                room_type_name = room_type_name,
                description = description,
                price = price,
                capacity = capacity,
                thumbnail_img_url = thumbnail_img_url
            ))
            session.commit()
            return {"status": "success"}
        except Exception as err:
            raise HTTPException(status_code=400, detail=f"{err}")
        
    
    @classmethod
    async def get_all_room_types(cls, session: Session):
        results = session.query(RoomType).all()
        return results
    

    @classmethod
    async def new_room(cls, session: Session, room_number: int, room_type_id:int):
        try:
            existing_room =  await cls.get_room(room_number=room_number, session=session)
            
            if existing_room:
                raise IntegrityError(f"Room with number {room_number} already exists")

            session.add(Room(
                room_number = room_number,
                room_type_id = room_type_id,
            ))
            session.commit()
            return {"status": "success"}
        except Exception as err:
            raise HTTPException(status_code=400, detail=f"{err}")

    
    @classmethod
    async def get_room(cls, room_number:int, session: Session):
        return session.query(Room).filter_by(room_number = room_number).first()

    
    @classmethod
    async def get_all_rooms(cls, session: Session):
        return session.query(Room).order_by(Room.room_type_id).all()
    

    @classmethod
    async def create_booking(cls, session: Session, guest_info: Dict, other_info: Dict):
        room_type_id = other_info["room_type_id"]
        check_in_date = date.fromisoformat(other_info["arrival"])

        all_rooms_of_type = session.query(Room).filter_by(room_type_id = room_type_id).all()
        available_rooms = [room for room in all_rooms_of_type if room.available] #type:ignore
        available_rooms_count = len(available_rooms)
       
        if(available_rooms_count < 1):
            return {"error": "This type of room is no longer available. Please select another room type"}
        
        first_name, last_name = guest_info["full_name"].split()
        address = guest_info["address"]
        phone = guest_info["phone_number"]
        email = guest_info["email"]

        guest = Guest(
            first_name = first_name,
            last_name = last_name,
            address = address,
            phone = phone,
            email = email
        )

        session.add(guest)
        session.flush()

        guest_id = guest.guest_id
        random_available_room = choice(available_rooms)
        room_type = session.query(RoomType).filter_by(room_type_id = room_type_id).first()
        price = room_type.price #type: ignore

        booking = Booking(
            guest_id = guest_id,
            room_number = random_available_room.room_number,
            price = price,
            check_in_date = check_in_date
        )

        session.add(booking)
        session.flush()

        random_available_room.available = False #type:ignore

        session.commit()
        return {"booking_id": booking.booking_id, "price": price}
    

    @classmethod
    async def booking_payment(cls, session: Session, booking_id, amount, payment_method):
        booking = session.query(Booking).filter_by(booking_id = booking_id).all()
        if not booking:
            raise HTTPException(status_code=400, detail="Booking does not exist on server")
        
        payment = Payment(
            booking_id = booking_id,
            amount = amount,
            payment_method = payment_method
        )

        session.add(payment)
        session.commit()
        
        return {"status": "success", "payment_id": payment.payment_id}