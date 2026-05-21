from pydantic import BaseModel
from typing import List
from datetime import datetime

class AlertingAgent:
    def __init__(self):
        # Mock contact information
        self.pest_control_contacts = ['pest.control@university.edu', 'pest.control@company.com']
        self.student_contacts = ['students@university.edu']
        self.admin_contacts = ['admin@university.edu']
        
    def send_alert(self, alert_data):
        '''Send alert to all relevant parties'''
        print(f"\n--- ALERT SENT ---")
        print(f"Location: {alert_data['location']}")
        print(f"Timestamp: {alert_data['timestamp']}")
        print(f"Rat Count: {alert_data['rat_count']}")
        print(f"Severity: {alert_data['severity']}")
        print(f"Affected Areas: {alert_data['affected_areas']}")
        print("--- ALERT END ---\n")
        
        # Send to pest control
        self._send_to_pest_control(alert_data)
        
        # Send to students
        self._send_to_students(alert_data)
        
        # Send to administration
        self._send_to_administration(alert_data)
        
        return alert_data
    
    def _send_to_pest_control(self, alert_data):
        '''Send alert to pest control company'''
        print(f"Sending alert to pest control: {self.pest_control_contacts}")
        # In a real system, this would send an email or SMS
        
    def _send_to_students(self, alert_data):
        '''Send alert to students'''
        print(f"Sending alert to students: {self.student_contacts}")
        # In a real system, this would send an email or SMS
        
    def _send_to_administration(self, alert_data):
        '''Send alert to administration'''
        print(f"Sending alert to administration: {self.admin_contacts}")
        # In a real system, this would send an email or SMS