import asyncio
from parking_mas.system import ParkingMAS

async def main():
    # Create and run the parking MAS
    mas = ParkingMAS()
    await mas.run_demo()
    
    print("\n=== Demo completed ===")

if __name__ == "__main__":
    asyncio.run(main())