from system_coordinator import SystemCoordinator
import sys


def main():
    try:
        # Initialize the system coordinator
        coordinator = SystemCoordinator()
        
        # Display system information
        status = coordinator.get_system_status()
        print("=== Pet Health Multi-Agent System ===")
        print(f"Agents: {', '.join(status['agents'])}")
        print(f"Protocols: {', '.join(status['protocols'])}")
        print(f"Services: {', '.join(status['services'])}")
        print()
        
        # Run the simulation
        coordinator.run_simulation()
        
        print("\n=== System Operation Complete ===")
        
    except Exception as e:
        print(f"Error running system: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()