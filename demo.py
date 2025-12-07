import sys
import os

# Ensure we can import the module from the current directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from airports import airport_data

def run_demo():
    print("--- Airport Data Python Library Demo ---\n")

    # 1. Basic Search
    print("1. Basic Search")
    airport = airport_data.get_airport_by_iata('SIN')
    if airport:
        print(f"IATA SIN: {airport[0]['airport']}")
    
    airport = airport_data.get_airport_by_icao('WSSS')
    if airport:
        print(f"ICAO WSSS: {airport[0]['country_code']}")

    airports = airport_data.search_by_name('Singapore')
    print(f"Search 'Singapore': Found {len(airports)} airports")
    print("")

    # 2. Geographic Search
    print("2. Geographic Search")
    # Singapore coordinates: 1.35019, 103.994003
    nearby = airport_data.find_nearby_airports(1.35019, 103.994003, 50)
    print(f"Airports within 50km of SIN: {len(nearby)}")
    
    nearest = airport_data.find_nearest_airport(1.35019, 103.994003)
    if nearest:
        print(f"Nearest to SIN: {nearest['airport']} ({nearest['distance']} km)")
    
    nearest_hub = airport_data.find_nearest_airport(1.35019, 103.994003, {
        'type': 'large_airport',
        'has_scheduled_service': True
    })
    if nearest_hub:
        print(f"Nearest large hub to SIN: {nearest_hub['airport']} ({nearest_hub['distance']} km)")
    
    dist = airport_data.calculate_distance('SIN', 'LHR')
    print(f"Distance SIN-LHR: {round(dist)} km")
    print("")

    # 3. Filtering
    print("3. Filtering")
    # Find large airports in Great Britain with scheduled service
    gb_airports = airport_data.find_airports({
        'country_code': 'GB',
        'type': 'large_airport',
        'has_scheduled_service': True
    })
    print(f"Large airports in GB with service: {len(gb_airports)}")
    
    # Test the boolean fix: find airports WITHOUT scheduled service (should be many)
    no_service = airport_data.find_airports({
        'country_code': 'SG',
        'has_scheduled_service': False
    })
    print(f"Airports in SG without service: {len(no_service)}")
    print("")

    # 4. Statistics
    print("4. Statistics")
    us_stats = airport_data.get_airport_stats_by_country('US')
    print(f"US Airports: {us_stats['total']}")
    print(f"US Large Airports: {us_stats['by_type'].get('large_airport', 0)}")
    
    as_stats = airport_data.get_airport_stats_by_continent('AS')
    print(f"Asia Airports: {as_stats['total']}")
    print(f"Asia Countries: {len(as_stats['by_country'])}")
    
    largest_as = airport_data.get_largest_airports_by_continent('AS', 5, 'runway')
    print("Top 5 Asia airports by runway:")
    for a in largest_as:
        print(f"  - {a['airport']}: {a['runway_length']} ft")
    print("")

    # 5. Bulk Operations
    print("5. Bulk Operations")
    multiple = airport_data.get_multiple_airports(['SIN', 'LHR', 'JFK', 'XXX'])
    found = [a['iata'] for a in multiple if a]
    print(f"Fetched: {found}")
    
    matrix = airport_data.calculate_distance_matrix(['SIN', 'LHR', 'JFK'])
    print(f"Distance SIN->JFK: {matrix['distances']['SIN']['JFK']} km")
    print("")

    # 6. Validation & Utilities
    print("6. Validation & Utilities")
    print(f"Validate IATA 'SIN': {airport_data.validate_iata_code('SIN')}")
    print(f"Validate IATA 'XYZ': {airport_data.validate_iata_code('XYZ')}") # Might be valid or invalid depending on data
    print(f"Validate ICAO 'WSSS': {airport_data.validate_icao_code('WSSS')}")
    print(f"Operational 'SIN': {airport_data.is_airport_operational('SIN')}")
    
    count = airport_data.get_airport_count({'country_code': 'US', 'type': 'large_airport'})
    print(f"Count US Large Airports: {count}")
    
    links = airport_data.get_airport_links('SIN')
    if links:
        print(f"SIN Wikipedia: {links.get('wikipedia')}")

if __name__ == "__main__":
    try:
        run_demo()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTest FAILED with error: {e}")
        import traceback
        traceback.print_exc()
