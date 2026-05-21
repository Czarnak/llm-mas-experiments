from typing import List, Optional
from math import radians, cos, sin, asin, sqrt
from ..models.parking_lot import ParkingLot


class SearchService:
    def __init__(self):
        pass

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians 
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula 
        dlat = lat2 - lat1 
        dlon = lon2 - lon1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r

    def find_nearby_parking_lots(self, target_location: dict, radius_km: float = 2.0) -> List[ParkingLot]:
        """
        Find parking lots within a specified radius of the target location.
        For this demo, we'll return a hardcoded list of parking lots.
        In a real implementation, this would query a database or external API.
        """
        # This is a mock implementation - in a real system this would query actual data
        # Mock parking lots data
        mock_parking_lots = [
            ParkingLot(
                id="parking_001",
                name="Parking Lot A",
                location={"lat": 52.2297, "lng": 21.0122},
                total_spots=100,
                available_spots=45,
                price_per_hour=15.0,
                address="ul. Warszawska 15, Warsaw, Poland",
                opening_hours={"start_time": "08:00", "end_time": "22:00"}
            ),
            ParkingLot(
                id="parking_002",
                name="Parking Lot B",
                location={"lat": 52.2323, "lng": 21.0133},
                total_spots=80,
                available_spots=20,
                price_per_hour=12.0,
                address="ul. Krakowska 22, Warsaw, Poland",
                opening_hours={"start_time": "07:00", "end_time": "23:00"}
            ),
            ParkingLot(
                id="parking_003",
                name="Parking Lot C",
                location={"lat": 52.2256, "lng": 21.0200},
                total_spots=120,
                available_spots=60,
                price_per_hour=18.0,
                address="ul. Piękna 45, Warsaw, Poland",
                opening_hours={"start_time": "09:00", "end_time": "21:00"}
            ),
            ParkingLot(
                id="parking_004",
                name="Parking Lot D",
                location={"lat": 52.2275, "lng": 21.0050},
                total_spots=60,
                available_spots=15,
                price_per_hour=20.0,
                address="ul. Gdańska 12, Warsaw, Poland",
                opening_hours={"start_time": "08:00", "end_time": "22:00"}
            )
        ]
        
        # Filter parking lots by distance
        nearby_lots = []
        for lot in mock_parking_lots:
            distance = self.haversine_distance(
                target_location["lat"],
                target_location["lng"],
                lot.location["lat"],
                lot.location["lng"]
            )
            if distance <= radius_km:
                nearby_lots.append(lot)
        
        # Sort by price per hour (ascending)
        nearby_lots.sort(key=lambda x: x.price_per_hour)
        
        return nearby_lots

    def find_parking_lots_for_hotel(self, hotel_name: str, target_location: dict) -> List[ParkingLot]:
        """
        Find parking lots near a specific hotel (in this case, we'll simulate with a hardcoded approach)
        """
        # In a real implementation, this would use a hotel database or geocoding API
        return self.find_nearby_parking_lots(target_location, radius_km=2.0)