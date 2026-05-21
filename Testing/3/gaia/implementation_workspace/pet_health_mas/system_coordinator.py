from agents.pet_owner_agent import PetOwnerAgent
from agents.pet_agent import PetAgent
from agents.veterinary_clinic_agent import VeterinaryClinicAgent
from agents.health_monitoring_agent import HealthMonitoringAgent
from agents.behavioral_analysis_agent import BehavioralAnalysisAgent
from agents.location_tracking_agent import LocationTrackingAgent
from agents.appointment_scheduling_agent import AppointmentSchedulingAgent
from services.protocol_manager import ProtocolManager
from services.service_manager import ServiceManager
from utils.data_models import *
from typing import Dict, Any
import uuid
import time


class SystemCoordinator:
    """
    Main coordinator for the Pet Health Multi-Agent System
    """
    
    def __init__(self):
        self.protocol_manager = ProtocolManager()
        self.service_manager = ServiceManager()
        self.agents = {}
        self.setup_agents()
        self.setup_protocols()
        self.setup_services()
        
    def setup_agents(self):
        """Initialize all agents and register them with the protocol manager"""
        agents = [
            PetOwnerAgent(),
            PetAgent(),
            VeterinaryClinicAgent(),
            HealthMonitoringAgent(),
            BehavioralAnalysisAgent(),
            LocationTrackingAgent(),
            AppointmentSchedulingAgent()
        ]
        
        for agent in agents:
            self.agents[agent.name] = agent
            self.protocol_manager.register_agent(agent)
            
    def setup_protocols(self):
        """Define all communication protocols based on GAIA documentation"""
        protocols = {
            "RecordPhysiologicalData": {
                "description": "HealthMonitor sends physiological data to PetOwner for review and storage.",
                "initiator": "HealthMonitoringAgent",
                "responder": "PetOwnerAgent",
                "inputs": ["EntityID: Pet", "Data: PhysiologicalData"],
                "outputs": []
            },
            "RecordLocation": {
                "description": "LocationTracker sends current location data to PetOwner for tracking.",
                "initiator": "LocationTrackingAgent",
                "responder": "PetOwnerAgent",
                "inputs": ["EntityID: Pet", "Data: LocationData"],
                "outputs": []
            },
            "AnalyzeBehavior": {
                "description": "BehavioralAnalyzer sends behavioral insights to PetOwner for awareness.",
                "initiator": "BehavioralAnalysisAgent",
                "responder": "PetOwnerAgent",
                "inputs": ["EntityID: Pet", "Data: BehaviorData"],
                "outputs": []
            },
            "MonitorHealthStatus": {
                "description": "HealthMonitor sends health status updates to VeterinaryClinic for consultation.",
                "initiator": "HealthMonitoringAgent",
                "responder": "VeterinaryClinicAgent",
                "inputs": ["EntityID: Pet", "Data: HealthStatus"],
                "outputs": []
            },
            "SendHealthAlert": {
                "description": "HealthMonitor notifies PetOwner about abnormal health indicators.",
                "initiator": "HealthMonitoringAgent",
                "responder": "PetOwnerAgent",
                "inputs": ["EntityID: Pet", "Data: AlertData"],
                "outputs": []
            },
            "ScheduleAppointment": {
                "description": "PetOwner requests an appointment with VeterinaryClinic through AppointmentScheduler.",
                "initiator": "PetOwnerAgent",
                "responder": "AppointmentSchedulingAgent",
                "inputs": ["EntityID: Pet", "Data: AppointmentRequest"],
                "outputs": ["Data: AppointmentConfirmation"]
            },
            "SendVetReminder": {
                "description": "AppointmentScheduler sends appointment reminders to PetOwner.",
                "initiator": "AppointmentSchedulingAgent",
                "responder": "PetOwnerAgent",
                "inputs": ["EntityID: Pet", "Data: ReminderData"],
                "outputs": []
            }
        }
        
        for protocol_name, protocol_info in protocols.items():
            self.protocol_manager.register_protocol(protocol_name, protocol_info)
            
    def setup_services(self):
        """Define all services provided by agents"""
        services = {
            "RecordPhysiologicalData": {
                "provided_by": "HealthMonitoringAgent",
                "derived_from": "RecordPhysiologicalData",
                "inputs": ["EntityID: Pet", "Data: PhysiologicalData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "PhysiologicalData != Null"
            },
            "RecordLocation": {
                "provided_by": "LocationTrackingAgent",
                "derived_from": "RecordLocation",
                "inputs": ["EntityID: Pet", "Data: LocationData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "LocationData != Null"
            },
            "AnalyzeBehavior": {
                "provided_by": "BehavioralAnalysisAgent",
                "derived_from": "AnalyzeBehavior",
                "inputs": ["EntityID: Pet", "Data: BehaviorData"],
                "outputs": ["Data: BehaviorData"],
                "pre_condition": "UniqueID(Pet) != Null AND BehaviorData != Null",
                "post_condition": "BehaviorData != Null"
            },
            "MonitorHealthStatus": {
                "provided_by": "HealthMonitoringAgent",
                "derived_from": "MonitorHealthStatus",
                "inputs": ["EntityID: Pet", "Data: HealthStatus"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "HealthStatus != Null"
            },
            "SendHealthAlert": {
                "provided_by": "HealthMonitoringAgent",
                "derived_from": "SendHealthAlert",
                "inputs": ["EntityID: Pet", "Data: AlertData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "AlertData != Null"
            },
            "ScheduleAppointment": {
                "provided_by": "AppointmentSchedulingAgent",
                "derived_from": "ScheduleAppointment",
                "inputs": ["EntityID: Pet", "Data: AppointmentRequest"],
                "outputs": ["Data: AppointmentConfirmation"],
                "pre_condition": "UniqueID(Pet) != Null AND AppointmentRequest != Null",
                "post_condition": "AppointmentConfirmation != Null"
            },
            "SendVetReminder": {
                "provided_by": "AppointmentSchedulingAgent",
                "derived_from": "SendVetReminder",
                "inputs": ["EntityID: Pet", "Data: ReminderData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "ReminderData != Null"
            },
            "ReviewPhysiologicalData": {
                "provided_by": "PetOwnerAgent",
                "derived_from": "ReviewPhysiologicalData",
                "inputs": ["EntityID: Pet", "Data: PhysiologicalData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND PhysiologicalData != Null",
                "post_condition": "PhysiologicalData != Null"
            },
            "ReviewLocationData": {
                "provided_by": "PetOwnerAgent",
                "derived_from": "ReviewLocationData",
                "inputs": ["EntityID: Pet", "Data: LocationData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND LocationData != Null",
                "post_condition": "LocationData != Null"
            },
            "ReviewBehaviorData": {
                "provided_by": "PetOwnerAgent",
                "derived_from": "ReviewBehaviorData",
                "inputs": ["EntityID: Pet", "Data: BehaviorData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND BehaviorData != Null",
                "post_condition": "BehaviorData != Null"
            },
            "ReceiveHealthAlert": {
                "provided_by": "PetOwnerAgent",
                "derived_from": "ReceiveHealthAlert",
                "inputs": ["EntityID: Pet", "Data: AlertData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND AlertData != Null",
                "post_condition": "AlertData != Null"
            },
            "ReceiveVetReminder": {
                "provided_by": "PetOwnerAgent",
                "derived_from": "ReceiveVetReminder",
                "inputs": ["EntityID: Pet", "Data: ReminderData"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND ReminderData != Null",
                "post_condition": "ReminderData != Null"
            },
            "ConsultPetHealth": {
                "provided_by": "VeterinaryClinicAgent",
                "derived_from": "ConsultPetHealth",
                "inputs": ["EntityID: Pet", "Data: HealthStatus"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND HealthStatus != Null",
                "post_condition": "HealthStatus != Null"
            },
            "ProvideTreatment": {
                "provided_by": "VeterinaryClinicAgent",
                "derived_from": "ProvideTreatment",
                "inputs": ["EntityID: Pet", "Data: HealthStatus"],
                "outputs": [],
                "pre_condition": "UniqueID(Pet) != Null AND HealthStatus != Null",
                "post_condition": "HealthStatus != Null"
            },
            "CollectPhysiologicalData": {
                "provided_by": "HealthMonitoringAgent",
                "derived_from": "CollectPhysiologicalData",
                "inputs": ["EntityID: Pet"],
                "outputs": ["Data: PhysiologicalData"],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "PhysiologicalData != Null"
            },
            "AnalyzePhysiologicalData": {
                "provided_by": "HealthMonitoringAgent",
                "derived_from": "AnalyzePhysiologicalData",
                "inputs": ["EntityID: Pet", "Data: PhysiologicalData"],
                "outputs": ["Data: HealthStatus"],
                "pre_condition": "UniqueID(Pet) != Null AND PhysiologicalData != Null",
                "post_condition": "HealthStatus != Null"
            },
            "DetectHealthAnomaly": {
                "provided_by": "HealthMonitoringAgent",
                "derived_from": "DetectHealthAnomaly",
                "inputs": ["EntityID: Pet", "Data: HealthStatus"],
                "outputs": ["Data: AlertData"],
                "pre_condition": "UniqueID(Pet) != Null AND HealthStatus != Null",
                "post_condition": "AlertData != Null"
            },
            "CollectBehaviorData": {
                "provided_by": "BehavioralAnalysisAgent",
                "derived_from": "CollectBehaviorData",
                "inputs": ["EntityID: Pet"],
                "outputs": ["Data: BehaviorData"],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "BehaviorData != Null"
            },
            "AnalyzeBehaviorPattern": {
                "provided_by": "BehavioralAnalysisAgent",
                "derived_from": "AnalyzeBehaviorPattern",
                "inputs": ["EntityID: Pet", "Data: BehaviorData"],
                "outputs": ["Data: BehaviorData"],
                "pre_condition": "UniqueID(Pet) != Null AND BehaviorData != Null",
                "post_condition": "BehaviorData != Null"
            },
            "CollectLocationData": {
                "provided_by": "LocationTrackingAgent",
                "derived_from": "CollectLocationData",
                "inputs": ["EntityID: Pet"],
                "outputs": ["Data: LocationData"],
                "pre_condition": "UniqueID(Pet) != Null",
                "post_condition": "LocationData != Null"
            },
            "ProcessAppointmentRequest": {
                "provided_by": "AppointmentSchedulingAgent",
                "derived_from": "ProcessAppointmentRequest",
                "inputs": ["EntityID: Pet", "Data: AppointmentRequest"],
                "outputs": ["Data: AppointmentConfirmation"],
                "pre_condition": "UniqueID(Pet) != Null AND AppointmentRequest != Null",
                "post_condition": "AppointmentConfirmation != Null"
            },
            "GenerateReminder": {
                "provided_by": "AppointmentSchedulingAgent",
                "derived_from": "GenerateReminder",
                "inputs": ["EntityID: Pet", "Data: AppointmentRequest"],
                "outputs": ["Data: ReminderData"],
                "pre_condition": "UniqueID(Pet) != Null AND AppointmentRequest != Null",
                "post_condition": "ReminderData != Null"
            }
        }
        
        for service_name, service_info in services.items():
            self.service_manager.register_service(service_name, service_info)
            
            # Register that the agent provides this service
            agent_name = service_info["provided_by"]
            self.service_manager.register_agent_service(agent_name, service_name)
            
    def run_simulation(self):
        """Run a simulation of the system working with sample data"""
        print("=== Starting Pet Health Multi-Agent System Simulation ===")
        
        # Create sample pet data
        pet_data = PetData(
            pet_id="PET001",
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            age=3,
            weight=25.5
        )
        
        print(f"\nCreated pet: {pet_data.name} ({pet_data.breed})")
        
        # Simulate physiological data collection and analysis
        print("\n--- Health Monitoring Simulation ---")
        physiological_data = PhysiologicalData(
            pet_id=pet_data.pet_id,
            heart_rate=72,
            temperature=38.5,
            respiratory_rate=20,
            blood_pressure="120/80",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Health monitor collects data
        result = self.protocol_manager.send_message(
            "HealthMonitoringAgent",
            "PetOwnerAgent",
            "RecordPhysiologicalData",
            physiological_data.dict()
        )
        print(f"Result: {result['result']}")
        
        # Health monitor analyzes data
        health_status = HealthStatus(
            pet_id=pet_data.pet_id,
            status="normal",
            description="All vitals within normal range",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        result = self.protocol_manager.send_message(
            "HealthMonitoringAgent",
            "VeterinaryClinicAgent",
            "MonitorHealthStatus",
            health_status.dict()
        )
        print(f"Result: {result['result']}")
        
        # Simulate location tracking
        print("\n--- Location Tracking Simulation ---")
        location_data = LocationData(
            pet_id=pet_data.pet_id,
            latitude=52.2297,
            longitude=21.0122,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        result = self.protocol_manager.send_message(
            "LocationTrackingAgent",
            "PetOwnerAgent",
            "RecordLocation",
            location_data.dict()
        )
        print(f"Result: {result['result']}")
        
        # Simulate behavior analysis
        print("\n--- Behavior Analysis Simulation ---")
        behavior_data = BehaviorData(
            pet_id=pet_data.pet_id,
            activity_level="moderate",
            behavior_patterns="normal",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        result = self.protocol_manager.send_message(
            "BehavioralAnalysisAgent",
            "PetOwnerAgent",
            "AnalyzeBehavior",
            behavior_data.dict()
        )
        print(f"Result: {result['result']}")
        
        # Simulate health alert
        print("\n--- Health Alert Simulation ---")
        alert_data = AlertData(
            pet_id=pet_data.pet_id,
            alert_type="health",
            message="Heart rate slightly elevated",
            severity="medium",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        result = self.protocol_manager.send_message(
            "HealthMonitoringAgent",
            "PetOwnerAgent",
            "SendHealthAlert",
            alert_data.dict()
        )
        print(f"Result: {result['result']}")
        
        # Simulate appointment scheduling
        print("\n--- Appointment Scheduling Simulation ---")
        appointment_request = AppointmentRequest(
            pet_id=pet_data.pet_id,
            vet_id="VET001",
            appointment_type="routine_checkup",
            date="2023-06-15",
            time="10:00",
            notes="Annual checkup"
        )
        
        result = self.protocol_manager.send_message(
            "PetOwnerAgent",
            "AppointmentSchedulingAgent",
            "ScheduleAppointment",
            appointment_request.dict()
        )
        print(f"Result: {result['result']}")
        
        # Simulate reminder generation
        reminder_data = ReminderData(
            pet_id=pet_data.pet_id,
            appointment_id="APT001",
            reminder_type="appointment",
            message="Reminder: Checkup appointment tomorrow at 10:00",
            reminder_date="2023-06-14",
            reminder_time="09:00"
        )
        
        result = self.protocol_manager.send_message(
            "AppointmentSchedulingAgent",
            "PetOwnerAgent",
            "SendVetReminder",
            reminder_data.dict()
        )
        print(f"Result: {result['result']}")
        
        print("\n=== Simulation Completed ===")
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'agents': self.protocol_manager.list_agents(),
            'protocols': self.protocol_manager.list_protocols(),
            'services': self.service_manager.list_services()
        }