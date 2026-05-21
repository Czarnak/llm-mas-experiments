import asyncio
from typing import Dict, List, Any
import json
import datetime

# Core data structures
pets = {}
vet_appointments = {}

# Agent classes

class PetLifecycleAgent:
    """Agent responsible for monitoring pet lifecycle functions"""
    def __init__(self):
        self.name = "Pet Lifecycle Agent"
        
    def create_pet(self, pet_id: str, name: str, species: str, age: int, breed: str = "") -> Dict[str, Any]:
        """Create a new pet"""
        pet = {
            "id": pet_id,
            "name": name,
            "species": species,
            "age": age,
            "breed": breed,
            "lifecycle_stage": self._determine_lifecycle_stage(age),
            "created_at": datetime.datetime.now().isoformat()
        }
        pets[pet_id] = pet
        return pet
        
    def update_pet(self, pet_id: str, **kwargs) -> Dict[str, Any]:
        """Update pet information"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        for key, value in kwargs.items():
            if key in pets[pet_id]:
                pets[pet_id][key] = value
                
        if "age" in kwargs:
            pets[pet_id]["lifecycle_stage"] = self._determine_lifecycle_stage(kwargs["age"])
        
        return pets[pet_id]
        
    def _determine_lifecycle_stage(self, age: int) -> str:
        """Determine pet lifecycle stage based on age"""
        if age < 1:
            return "puppy/kitten"
        elif age < 3:
            return "young"
        elif age < 8:
            return "adult"
        else:
            return "senior"
        
    def get_pet(self, pet_id: str) -> Dict[str, Any]:
        """Get pet information"""
        return pets.get(pet_id, None)


class LocationTrackingAgent:
    """Agent responsible for tracking pet location"""
    def __init__(self):
        self.name = "Location Tracking Agent"
        
    def update_location(self, pet_id: str, latitude: float, longitude: float, timestamp: str = "") -> Dict[str, Any]:
        """Update pet location"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        location_data = {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp or datetime.datetime.now().isoformat()
        }
        
        if "location_history" not in pets[pet_id]:
            pets[pet_id]["location_history"] = []
        
        pets[pet_id]["location_history"].append(location_data)
        pets[pet_id]["current_location"] = location_data
        
        return location_data
        
    def get_current_location(self, pet_id: str) -> Dict[str, Any]:
        """Get current pet location"""
        pet = pets.get(pet_id)
        if pet and "current_location" in pet:
            return pet["current_location"]
        return None
        
    def get_location_history(self, pet_id: str) -> List[Dict[str, Any]]:
        """Get pet location history"""
        pet = pets.get(pet_id)
        if pet and "location_history" in pet:
            return pet["location_history"]
        return []


class BehaviorControlAgent:
    """Agent responsible for controlling pet behavior"""
    def __init__(self):
        self.name = "Behavior Control Agent"
        
    def set_behavior_rules(self, pet_id: str, rules: List[str]) -> Dict[str, Any]:
        """Set behavior rules for pet"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        pets[pet_id]["behavior_rules"] = rules
        return {"status": "rules updated", "rules": rules}
        
    def get_behavior_rules(self, pet_id: str) -> List[str]:
        """Get behavior rules for pet"""
        pet = pets.get(pet_id)
        if pet and "behavior_rules" in pet:
            return pet["behavior_rules"]
        return []
        
    def enforce_behavior_rule(self, pet_id: str, rule: str) -> Dict[str, Any]:
        """Enforce a specific behavior rule"""
        rules = self.get_behavior_rules(pet_id)
        if rule in rules:
            return {"status": "rule enforced", "rule": rule}
        else:
            return {"status": "rule not found", "rule": rule}


class HealthMonitoringAgent:
    """Agent responsible for monitoring pet health status"""
    def __init__(self):
        self.name = "Health Monitoring Agent"
        
    def update_health_status(self, pet_id: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update pet health status"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        if "health_status" not in pets[pet_id]:
            pets[pet_id]["health_status"] = {}
        
        pets[pet_id]["health_status"].update(health_data)
        
        # Check if health status requires attention
        health_issues = self._check_health_issues(pets[pet_id]["health_status"])
        if health_issues:
            pets[pet_id]["health_issues"] = health_issues
        
        return pets[pet_id]["health_status"]
        
    def get_health_status(self, pet_id: str) -> Dict[str, Any]:
        """Get pet health status"""
        pet = pets.get(pet_id)
        if pet and "health_status" in pet:
            return pet["health_status"]
        return {}
        
    def _check_health_issues(self, health_data: Dict[str, Any]) -> List[str]:
        """Check for potential health issues based on health data"""
        issues = []
        
        if health_data.get("weight") and health_data["weight"] > 30:
            issues.append("weight too high")
        
        if health_data.get("temperature") and health_data["temperature"] > 40:
            issues.append("high temperature")
            
        if health_data.get("heart_rate") and health_data["heart_rate"] > 150:
            issues.append("high heart rate")
            
        return issues


class VetAppointmentReminderAgent:
    """Agent responsible for reminding about vet appointments"""
    def __init__(self):
        self.name = "Vet Appointment Reminder Agent"
        
    def get_upcoming_appointments(self, pet_id: str) -> List[Dict[str, Any]]:
        """Get upcoming vet appointments for pet"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        if "appointments" not in pets[pet_id]:
            return []
        
        return pets[pet_id]["appointments"]
        
    def check_reminders(self) -> List[Dict[str, Any]]:
        """Check for upcoming reminders"""
        reminders = []
        
        for pet_id, pet_data in pets.items():
            if "appointments" in pet_data:
                for appointment in pet_data["appointments"]:
                    # Simple reminder logic - check if appointment date is today
                    try:
                        appointment_date = datetime.datetime.strptime(appointment["date"], "%Y-%m-%d")
                        today = datetime.datetime.now().date()
                        if appointment_date.date() == today:
                            reminders.append({
                                "pet_id": pet_id,
                                "pet_name": pet_data["name"],
                                "appointment": appointment
                            })
                    except Exception:
                        # Skip if date parsing fails
                        continue
        
        return reminders


class VetAppointmentSchedulingAgent:
    """Agent responsible for scheduling vet appointments"""
    def __init__(self):
        self.name = "Vet Appointment Scheduling Agent"
        
    def schedule_appointment(self, pet_id: str, appointment_type: str, date: str, time: str, vet: str = "Dr. Smith") -> Dict[str, Any]:
        """Schedule a vet appointment"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        appointment = {
            "id": f"apt_{len(pets.get(pet_id, {}).get('appointments', [])) + 1}",
            "type": appointment_type,
            "date": date,
            "time": time,
            "vet": vet,
            "status": "scheduled"
        }
        
        if "appointments" not in pets[pet_id]:
            pets[pet_id]["appointments"] = []
        
        pets[pet_id]["appointments"].append(appointment)
        
        return appointment
        
    def cancel_appointment(self, pet_id: str, appointment_id: str) -> Dict[str, Any]:
        """Cancel a vet appointment"""
        if pet_id not in pets:
            raise ValueError(f"Pet with ID {pet_id} not found")
        
        if "appointments" in pets[pet_id]:
            for i, appointment in enumerate(pets[pet_id]["appointments"]):
                if appointment["id"] == appointment_id:
                    pets[pet_id]["appointments"].pop(i)
                    return {"status": "appointment cancelled"}
        
        return {"status": "appointment not found"}


class PetManagementSystem:
    """Main Pet Management System coordinating all agents"""
    def __init__(self):
        self.lifecycle_agent = PetLifecycleAgent()
        self.location_agent = LocationTrackingAgent()
        self.behavior_agent = BehaviorControlAgent()
        self.health_agent = HealthMonitoringAgent()
        self.reminder_agent = VetAppointmentReminderAgent()
        self.scheduling_agent = VetAppointmentSchedulingAgent()
        
    def initialize_system(self):
        """Initialize the system with some sample data"""
        # Create sample pets
        self.lifecycle_agent.create_pet("pet1", "Buddy", "Dog", 2, "Golden Retriever")
        self.lifecycle_agent.create_pet("pet2", "Whiskers", "Cat", 1, "Persian")
        
        # Set up behavior rules
        self.behavior_agent.set_behavior_rules("pet1", ["no jumping on furniture", "sit on command"])
        self.behavior_agent.set_behavior_rules("pet2", ["use litter box", "no scratching furniture"])
        
        # Update health status
        self.health_agent.update_health_status("pet1", {
            "weight": 25,
            "temperature": 38.5,
            "heart_rate": 120
        })
        
        self.health_agent.update_health_status("pet2", {
            "weight": 4,
            "temperature": 38.2,
            "heart_rate": 180
        })
        
        # Schedule some appointments
        self.scheduling_agent.schedule_appointment("pet1", "annual checkup", "2023-01-01", "10:00", "Dr. Johnson")
        self.scheduling_agent.schedule_appointment("pet2", "vaccination", "2023-01-02", "14:00", "Dr. Smith")
        
        print("System initialized with sample data")
        
    def run_simulation(self):
        """Run a simulation of the system"""
        print("\n=== Pet Management System Simulation ===")
        
        # Get pet information
        pet1 = self.lifecycle_agent.get_pet("pet1")
        print(f"Pet 1: {pet1}")
        
        # Update location
        self.location_agent.update_location("pet1", 52.52, 13.40, "2023-01-01T10:00:00Z")
        print(f"Pet 1 location updated")
        
        # Get health status
        health = self.health_agent.get_health_status("pet1")
        print(f"Pet 1 health: {health}")
        
        # Get upcoming appointments
        appointments = self.reminder_agent.get_upcoming_appointments("pet1")
        print(f"Pet 1 appointments: {appointments}")
        
        # Check reminders
        reminders = self.reminder_agent.check_reminders()
        print(f"Reminders: {reminders}")
        
        print("\n=== Simulation Complete ===")
        
    def get_all_pets(self) -> Dict[str, Any]:
        """Get all pets in the system"""
        return pets

# Create the system
system = PetManagementSystem()

if __name__ == "__main__":
    system.initialize_system()
    system.run_simulation()