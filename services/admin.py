from sqlalchemy.orm import Session
from db.db import Room, RoomType
from fastapi import HTTPException
from sqlite3 import IntegrityError
from random import choice

class AdminServices:
    @classmethod
    async def get_dashboard_statistics(cls, session: Session):
        room_types = len(session.query(RoomType).all())
        all_rooms = session.query(Room).all()
        reserved_rooms = len([room for room in all_rooms if room.reserved is True])
        booked_rooms = len([room for room in all_rooms if room.booked is True])
        total_rooms = len(all_rooms)
    
        return dict(reserved_rooms = reserved_rooms, booked_rooms = booked_rooms, total_rooms=total_rooms, room_types=room_types)
    

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