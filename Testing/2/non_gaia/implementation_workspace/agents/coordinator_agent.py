from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import statistics

class CoordinatorAgent:
    def __init__(self):
        # Store sensor data
        self.sensor_data_history = []
        self.areas = {}
        
    def receive_data(self, data):
        '''Receive data from sensor agents and store it'''
        self.sensor_data_history.append(data)
        
        # Update area information
        if data.location not in self.areas:
            self.areas[data.location] = []
        
        self.areas[data.location].append(data)
        
        print(f"Coordinator received data from {data.sensor_id} at {data.location}: {data.rat_count} rats")
        
        return data
    
    def analyze_patterns(self) -> Dict:
        '''Analyze sensor data to identify rat activity patterns'''
        if not self.sensor_data_history:
            return {}
        
        # Calculate statistics for each area
        area_stats = {}
        
        for location, data_points in self.areas.items():
            rat_counts = [d.rat_count for d in data_points]
            
            area_stats[location] = {
                'total_events': len(data_points),
                'total_rats': sum(rat_counts),
                'avg_rats': statistics.mean(rat_counts) if rat_counts else 0,
                'max_rats': max(rat_counts) if rat_counts else 0,
                'min_rats': min(rat_counts) if rat_counts else 0,
            }
        
        return area_stats
    
    def identify_hotspots(self, threshold: int = 5) -> List[str]:
        '''Identify areas with high rat activity'''
        stats = self.analyze_patterns()
        hotspots = []
        
        for location, stats_data in stats.items():
            if stats_data['avg_rats'] >= threshold or stats_data['max_rats'] >= threshold:
                hotspots.append(location)
                
        return hotspots
    
    def generate_alert(self, location: str, rat_count: int):
        '''Generate an alert based on rat activity'''
        # Determine severity based on rat count
        if rat_count >= 10:
            severity = 'high'
        elif rat_count >= 5:
            severity = 'medium'
        else:
            severity = 'low'
            
        # Get affected areas (in this case, just the location)
        affected_areas = [location]
        
        alert = {
            'location': location,
            'timestamp': datetime.now(),
            'rat_count': rat_count,
            'severity': severity,
            'affected_areas': affected_areas
        }
        
        print(f"Generated alert for {location}: {rat_count} rats detected (severity: {severity})")
        return alert