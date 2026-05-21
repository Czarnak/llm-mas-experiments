import asyncio
import aiosqlite
from typing import List, Optional
from .message_types import Request, AvailableMaterials, MatchInformation
import uuid
from datetime import datetime


class Database:
    def __init__(self, db_path: str = "crisis_transport.db"):
        self.db_path = db_path
        
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    id TEXT PRIMARY KEY,
                    requester_id TEXT,
                    resource_type TEXT,
                    quantity INTEGER,
                    location TEXT,
                    timestamp TEXT,
                    status TEXT
                )''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS available_materials (
                    id TEXT PRIMARY KEY,
                    provider_id TEXT,
                    resource_type TEXT,
                    quantity INTEGER,
                    location TEXT,
                    timestamp TEXT,
                    status TEXT
                )''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id TEXT PRIMARY KEY,
                    request_id TEXT,
                    available_materials_id TEXT,
                    matched_quantity INTEGER,
                    timestamp TEXT,
                    status TEXT
                )''')
            
            await db.commit()
            
    async def add_request(self, request: Request):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR REPLACE INTO requests 
                (id, requester_id, resource_type, quantity, location, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                request.id,
                request.requester_id,
                request.resource_type,
                request.quantity,
                request.location,
                request.timestamp.isoformat(),
                request.status
            ))
            await db.commit()
            
    async def get_requests(self) -> List[Request]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM requests")
            rows = await cursor.fetchall()
            return [Request(
                id=row[0],
                requester_id=row[1],
                resource_type=row[2],
                quantity=row[3],
                location=row[4],
                timestamp=datetime.fromisoformat(row[5]),
                status=row[6]
            ) for row in rows]
            
    async def add_available_materials(self, materials: AvailableMaterials):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR REPLACE INTO available_materials 
                (id, provider_id, resource_type, quantity, location, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                materials.id,
                materials.provider_id,
                materials.resource_type,
                materials.quantity,
                materials.location,
                materials.timestamp.isoformat(),
                materials.status
            ))
            await db.commit()
            
    async def get_available_materials(self) -> List[AvailableMaterials]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM available_materials")
            rows = await cursor.fetchall()
            return [AvailableMaterials(
                id=row[0],
                provider_id=row[1],
                resource_type=row[2],
                quantity=row[3],
                location=row[4],
                timestamp=datetime.fromisoformat(row[5]),
                status=row[6]
            ) for row in rows]
            
    async def add_match(self, match: MatchInformation):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR REPLACE INTO matches 
                (id, request_id, available_materials_id, matched_quantity, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?)''', (
                match.id,
                match.request_id,
                match.available_materials_id,
                match.matched_quantity,
                match.timestamp.isoformat(),
                match.status
            ))
            await db.commit()
            
    async def get_matches(self) -> List[MatchInformation]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM matches")
            rows = await cursor.fetchall()
            return [MatchInformation(
                id=row[0],
                request_id=row[1],
                available_materials_id=row[2],
                matched_quantity=row[3],
                timestamp=datetime.fromisoformat(row[4]),
                status=row[5]
            ) for row in rows]
            
    async def update_request_status(self, request_id: str, status: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE requests SET status = ? WHERE id = ?", (status, request_id))
            await db.commit()
            
    async def update_available_materials_status(self, materials_id: str, status: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE available_materials SET status = ? WHERE id = ?", (status, materials_id))
            await db.commit()
            
    async def update_match_status(self, match_id: str, status: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE matches SET status = ? WHERE id = ?", (status, match_id))
            await db.commit()
