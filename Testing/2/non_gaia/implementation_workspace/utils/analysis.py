from typing import List, Dict
from datetime import datetime
import statistics


def analyze_sensor_data(data_history: List[Dict]) -> Dict:
    '''Analyze sensor data to identify patterns and trends'''
    if not data_history:
        return {}
    
    # Group data by location
    location_data = {}
    for data_point in data_history:
        location = data_point['location']
        if location not in location_data:
            location_data[location] = []
        location_data[location].append(data_point)
    
    # Calculate statistics for each location
    analysis_results = {}
    for location, data_points in location_data.items():
        rat_counts = [d['rat_count'] for d in data_points]
        
        analysis_results[location] = {
            'total_events': len(data_points),
            'total_rats': sum(rat_counts),
            'avg_rats': statistics.mean(rat_counts) if rat_counts else 0,
            'max_rats': max(rat_counts) if rat_counts else 0,
            'min_rats': min(rat_counts) if rat_counts else 0,
            'timestamps': [d['timestamp'] for d in data_points]
        }
    
    return analysis_results


def identify_hotspots(analysis_results: Dict, threshold: int = 5) -> List[str]:
    '''Identify areas with high rat activity'''
    hotspots = []
    
    for location, stats in analysis_results.items():
        if stats['avg_rats'] >= threshold or stats['max_rats'] >= threshold:
            hotspots.append(location)
            
    return hotspots


def determine_severity(rat_count: int) -> str:
    '''Determine alert severity based on rat count'''
    if rat_count >= 10:
        return 'high'
    elif rat_count >= 5:
        return 'medium'
    else:
        return 'low'