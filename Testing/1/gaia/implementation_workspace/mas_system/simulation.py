import random
from datetime import datetime, timedelta
from .agents.animal_registry_agent import AnimalRegistryAgent
from .agents.staff_management_agent import StaffManagementAgent
from .agents.task_generation_agent import TaskGenerationAgent
from .agents.task_tracking_agent import TaskTrackingAgent
from .agents.admission_and_adoption_agent import AdmissionAndAdoptionAgent
from .agents.emergency_response_agent import EmergencyResponseAgent
from .agents.fair_rotation_agent import FairRotationAgent
from .utils.messaging_system import MessagingSystem
from .models.animal import Animal
from .models.staff import StaffMember
from .models.task import Task


def run_simulation():
    print("Starting Multi-Agent System Simulation for Animal Shelter")
    
    # Initialize messaging system
    messaging_system = MessagingSystem()
    
    # Create agents
    animal_registry = AnimalRegistryAgent("animal_registry_001", "Animal Registry")
    staff_management = StaffManagementAgent("staff_management_001", "Staff Management")
    task_generation = TaskGenerationAgent("task_generation_001", "Task Generation")
    task_tracking = TaskTrackingAgent("task_tracking_001", "Task Tracking")
    admission_adoption = AdmissionAndAdoptionAgent("admission_adoption_001", "Admission & Adoption")
    emergency_response = EmergencyResponseAgent("emergency_response_001", "Emergency Response")
    fair_rotation = FairRotationAgent("fair_rotation_001", "Fair Rotation")
    
    # Register agents with messaging system
    messaging_system.register_agent(animal_registry)
    messaging_system.register_agent(staff_management)
    messaging_system.register_agent(task_generation)
    messaging_system.register_agent(task_tracking)
    messaging_system.register_agent(admission_adoption)
    messaging_system.register_agent(emergency_response)
    messaging_system.register_agent(fair_rotation)
    
    print("Agents registered successfully")
    
    # Simulate animal admission
    print("\n=== Simulating Animal Admission ===")
    animal_data = {
        "id": "animal_001",
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "gender": "Male",
        "health_status": "healthy",
        "adoption_status": "pending"
    }
    
    # Process animal admission
    result = messaging_system.send_message(
        "admission_adoption_001", 
        "animal_registry_001", 
        "ProcessAnimalAdmission", 
        {"AdmissionData": animal_data}
    )
    
    print(f"Animal admission processed: {result.content if result else 'Failed'}")
    
    # Register staff members
    print("\n=== Registering Staff Members ===")
    staff_data = [
        {
            "id": "staff_001",
            "name": "John Smith",
            "role": "caretaker",
            "skills": ["dog_care", "feeding"],
            "preferences": {"shift": "morning"}
        },
        {
            "id": "staff_002",
            "name": "Sarah Johnson",
            "role": "cleaner",
            "skills": ["cleaning"],
            "preferences": {"shift": "afternoon"}
        }
    ]
    
    for staff in staff_data:
        result = messaging_system.send_message(
            "admission_adoption_001", 
            "animal_registry_001", 
            "RegisterStaffMember", 
            {"StaffProfile": staff}
        )
        print(f"Staff member registered: {staff['name']} - {result.content if result else 'Failed'}")
    
    # Generate tasks
    print("\n=== Generating Care Tasks ===")
    
    # Generate feeding task
    result = messaging_system.send_message(
        "task_generation_001", 
        "task_tracking_001", 
        "GenerateCareTask", 
        {"TaskDefinition": {
            "type": "feeding",
            "animal_id": "animal_001",
            "priority": "high",
            "details": {"food_type": "premium_dog_food", "amount": "2 cups"}
        }}
    )
    print(f"Feeding task generated: {result.content if result else 'Failed'}")
    
    # Generate cleaning task
    result = messaging_system.send_message(
        "task_generation_001", 
        "task_tracking_001", 
        "GenerateCleaningTask", 
        {"CleaningRequirements": {
            "animal_id": "animal_001",
            "room": "Kennel 1",
            "type": "daily"
        }}
    )
    print(f"Cleaning task generated: {result.content if result else 'Failed'}")
    
    # Simulate task status updates
    print("\n=== Updating Task Status ===")
    
    # Update task status
    result = messaging_system.send_message(
        "staff_management_001", 
        "task_tracking_001", 
        "UpdateTaskStatus", 
        {"TaskID": "task_1", "StatusReport": {"status": "completed", "timestamp": datetime.now()}}
    )
    print(f"Task status updated: {result.content if result else 'Failed'}")
    
    # Simulate emergency response
    print("\n=== Simulating Emergency Response ===")
    result = messaging_system.send_message(
        "emergency_response_001", 
        "task_tracking_001", 
        "HandleEmergency", 
        {"EmergencyEvent": "new_animal_arrival"}
    )
    print(f"Emergency handled: {result.content if result else 'Failed'}")
    
    print("\n=== Simulation Complete ===")
    
    # Display final state
    print("\nFinal State:")
    print(f"Animals: {len(animal_registry.get_all_animals())}")
    print(f"Staff: {len(staff_management.get_all_staff())}")
    print(f"Tasks: {len(task_generation.get_all_tasks())}")
    
    return messaging_system

if __name__ == "__main__":
    run_simulation()