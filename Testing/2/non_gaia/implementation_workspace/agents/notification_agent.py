from pydantic import BaseModel
from typing import List
from datetime import datetime

class NotificationAgent:
    def __init__(self):
        # Mock student room information
        self.rooms = {
            'room_101': {'students': ['student1@university.edu', 'student2@university.edu']},
            'room_102': {'students': ['student3@university.edu', 'student4@university.edu']},
            'room_103': {'students': ['student5@university.edu', 'student6@university.edu']},
        }
        
    def send_notification(self, notification_data):
        '''Send notification to students about room conditions'''
        print(f"\n--- NOTIFICATION SENT ---")
        print(f"Room ID: {notification_data['room_id']}")
        print(f"Location: {notification_data['location']}")
        print(f"Timestamp: {notification_data['timestamp']}")
        print(f"Status: {notification_data['status']}")
        print(f"Message: {notification_data['message']}")
        print("--- NOTIFICATION END ---\n")
        
        # Send to students in the room
        self._send_to_students(notification_data)
        
        return notification_data
    
    def _send_to_students(self, notification_data):
        '''Send notification to students in a specific room'''
        if notification_data['room_id'] in self.rooms:
            students = self.rooms[notification_data['room_id']]['students']
            print(f"Sending notification to students in {notification_data['room_id']}: {students}")
            # In a real system, this would send an email or SMS
        else:
            print(f"No students registered for room {notification_data['room_id']}")
            
    def update_room_status(self, room_id: str, status: str, message: str):
        '''Update room status and send notification'''
        # Determine if we need to send a notification based on status change
        notification_data = {
            'room_id': room_id,
            'location': f"Building A, {room_id}",
            'timestamp': datetime.now(),
            'status': status,
            'message': message
        }
        
        print(f"Updating room {room_id} status to {status}")
        return self.send_notification(notification_data)