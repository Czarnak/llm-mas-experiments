import os
from models.system import WasteCollectionSystem
from services.operation_service import OperationService

def main():
    # Initialize the waste collection system
    system = WasteCollectionSystem()
    
    # Initialize the operation service
    operation_service = OperationService(system)
    
    # Run the simulation
    try:
        result = operation_service.run_simulation()
        print("\n=== SIMULATION COMPLETED SUCCESSFULLY ===")
        return result
    except Exception as e:
        print(f"\n=== SIMULATION ERROR ===")
        print(f"Error occurred during simulation: {str(e)}")
        return None

if __name__ == "__main__":
    main()