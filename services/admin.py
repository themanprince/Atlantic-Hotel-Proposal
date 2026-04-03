from sqlalchemy.orm import Session
from db.db import RoomType
from fastapi import HTTPException
from random import choice

class AdminServices:
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
            return HTTPException(status_code=400, detail=f"Error in Creating RoomType\n{err}")
        
    
    @classmethod
    async def get_all_room_types(cls, session: Session):
        results = session.query(RoomType).all()
        return results