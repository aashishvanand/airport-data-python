import gzip
import json
import os
import math
import re
from typing import List, Dict, Any, Optional, Union
from collections import defaultdict

# Load the gzipped JSON data from the data directory
data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'airports.gz')
with gzip.open(data_file_path, 'rt', encoding='utf-8') as f:
    airports = json.load(f)

# Build O(1) lookup indexes at load time for fast code-based lookups
_iata_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
_icao_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
_country_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
_continent_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
_city_code_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
_timezone_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

# Name index maps lowercase name -> list of airports (handles duplicate names)
airport_name_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

for _airport in airports:
    _iata = _airport.get("iata", "")
    if _iata:
        _iata_index[_iata].append(_airport)

    _icao = _airport.get("icao", "")
    if _icao:
        _icao_index[_icao].append(_airport)

    _cc = _airport.get("country_code", "")
    if _cc:
        _country_index[_cc].append(_airport)

    _cont = _airport.get("continent", "")
    if _cont:
        _continent_index[_cont].append(_airport)

    _city = _airport.get("city_code", "")
    if _city:
        _city_code_index[_city].append(_airport)

    _tz = _airport.get("time", "")
    if _tz:
        _timezone_index[_tz].append(_airport)

    _name = _airport.get("airport", "").lower()
    if _name:
        airport_name_index[_name].append(_airport)



# Compile regex patterns once at module level for better performance
IATA_PATTERN = re.compile(r'^[A-Z]{3}$')
ICAO_PATTERN = re.compile(r'^[A-Z0-9]{4}$')
CITY_CODE_PATTERN = re.compile(r'^[A-Z0-9]+$')
COUNTRY_CODE_PATTERN = re.compile(r'^[A-Z]{2}$')
CONTINENT_CODE_PATTERN = re.compile(r'^[A-Z]{2}$')

# Module-level Haversine helper to avoid redefining in multiple functions
_EARTH_RADIUS_KM = 6371

def _to_rad(value: float) -> float:
    """Convert degrees to radians."""
    return math.radians(value)

def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points using the Haversine formula."""
    d_lat = _to_rad(lat2 - lat1)
    d_lon = _to_rad(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(_to_rad(lat1)) * math.cos(_to_rad(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return _EARTH_RADIUS_KM * c

def _validate_input(data: str, pattern: re.Pattern, error_message: str) -> str:
    """
    Validates a string against a compiled pattern and returns normalized data.
    
    Args:
        data: The data to validate
        pattern: The compiled regex pattern to test against
        error_message: The error message to raise if validation fails
    
    Returns:
        Normalized (uppercase) data
    
    Raises:
        ValueError: If the data does not match the pattern
    """
    if not isinstance(data, str):
        raise ValueError("Input must be a string")
    
    # Normalize to uppercase for consistent validation and lookup
    normalized_data = data.upper()
    
    if not pattern.match(normalized_data):
        raise ValueError(error_message)
    
    return normalized_data

def _get_airport_by_code(code: str) -> Optional[Dict[str, Any]]:
    """
    Helper function to get an airport by either IATA or ICAO code.
    Uses pre-built indexes for O(1) lookup instead of linear scan.
    
    Args:
        code: A 3-letter IATA or 4-character ICAO code
    
    Returns:
        The first matching airport object, or None
    """
    if not isinstance(code, str):
        return None
    
    code = code.upper()
    
    # Check IATA code format (3 uppercase letters) - O(1) index lookup
    if len(code) == 3 and code.isalpha():
        results = _iata_index.get(code)
        return results[0] if results else None
    
    # Check ICAO code format (4 uppercase letters/numbers) - O(1) index lookup
    if len(code) == 4 and code.isalnum():
        results = _icao_index.get(code)
        return results[0] if results else None
    
    return None

def get_airport_by_iata(iata_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 3-letter IATA code.
    
    Args:
        iata_code: The IATA code of the airport to find (e.g., 'AAA' or 'aaa')
    
    Returns:
        A list of matching airport objects. Returns an empty list if no data is found.
    
    Raises:
        ValueError: If the IATA code format is invalid
    """
    normalized_code = _validate_input(
        iata_code, 
        IATA_PATTERN, 
        "Invalid IATA format. Please provide a 3-letter code, e.g., 'AAA'."
    )
    return list(_iata_index.get(normalized_code, []))

def get_airport_by_icao(icao_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 4-character ICAO code.
    
    Args:
        icao_code: The ICAO code of the airport to find (e.g., 'NTGA' or 'ntga')
    
    Returns:
        A list of matching airport objects. Returns an empty list if no data is found.
    
    Raises:
        ValueError: If the ICAO code format is invalid
    """
    normalized_code = _validate_input(
        icao_code, 
        ICAO_PATTERN, 
        "Invalid ICAO format. Please provide a 4-character code, e.g., 'NTGA'."
    )
    return list(_icao_index.get(normalized_code, []))

def get_airport_by_city_code(city_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their city code.
    
    Args:
        city_code: The city code to search for. Alphanumeric (e.g., 'NYC' or 'nyc').
    
    Returns:
        A list of matching airport objects. Returns an empty list if no data is found.
    
    Raises:
        ValueError: If the city code format is invalid
    """
    normalized_code = _validate_input(
        city_code, 
        CITY_CODE_PATTERN, 
        "Invalid City Code format. Please provide an alphanumeric code, e.g., 'NYC'."
    )
    return list(_city_code_index.get(normalized_code, []))

def get_airport_by_country_code(country_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 2-letter country code.
    
    Args:
        country_code: The country code to search for (e.g., 'US' or 'us')
    
    Returns:
        A list of matching airport objects. Returns an empty list if no data is found.
    
    Raises:
        ValueError: If the country code format is invalid
    """
    normalized_code = _validate_input(
        country_code, 
        COUNTRY_CODE_PATTERN, 
        "Invalid Country Code format. Please provide a 2-letter code, e.g., 'US'."
    )
    return list(_country_index.get(normalized_code, []))

def get_airport_by_continent(continent_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 2-letter continent code.
    
    Args:
        continent_code: The continent code to search for (e.g., 'AS' for Asia)
    
    Returns:
        A list of matching airport objects. Returns an empty list if no data is found.
    
    Raises:
        ValueError: If the continent code format is invalid
    """
    normalized_code = _validate_input(
        continent_code, 
        CONTINENT_CODE_PATTERN, 
        "Invalid Continent Code format. Please provide a 2-letter code, e.g., 'AS'."
    )
    return list(_continent_index.get(normalized_code, []))

def search_by_name(query: str, max_results: int = 100) -> List[Dict[str, Any]]:
    """
    Searches for airports by their name. Case-insensitive with early termination for performance.
    
    Args:
        query: The name or partial name to search for (e.g., "Heathrow")
        max_results: Maximum number of results to return (default 100)
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If search query is less than 2 characters
    """
    if not isinstance(query, str) or len(query) < 2:
        raise ValueError("Search query must be at least 2 characters long.")
    
    lower_case_query = query.lower()
    results = []
    seen_ids = set()  # Track by id() for O(1) dedup instead of O(n) list containment
    
    # First, check for exact match in name index (O(1) lookup)
    exact_matches = airport_name_index.get(lower_case_query, [])
    for airport in exact_matches:
        if id(airport) not in seen_ids:
            results.append(airport)
            seen_ids.add(id(airport))
            if len(results) >= max_results:
                return results
    
    # Then check for partial matches in name index
    for name, airport_list in airport_name_index.items():
        if lower_case_query in name:
            for airport in airport_list:
                if id(airport) not in seen_ids:
                    results.append(airport)
                    seen_ids.add(id(airport))
                    if len(results) >= max_results:
                        return results
    
    return results

def find_nearby_airports(lat: float, lon: float, radius_km: float = 100) -> List[Dict[str, Any]]:
    """
    Finds airports within a specified radius (in kilometers) of a given latitude and longitude.
    
    Args:
        lat: The latitude of the center point
        lon: The longitude of the center point
        radius_km: The search radius in kilometers (defaults to 100)
    
    Returns:
        A list of airports within the radius
    """
    results = []
    for airport in airports:
        airport_lat = airport.get("latitude")
        airport_lon = airport.get("longitude")
        if not airport_lat or not airport_lon:
            continue
        
        try:
            distance = _haversine_distance(lat, lon, float(airport_lat), float(airport_lon))
            if distance <= radius_km:
                results.append(airport)
        except (ValueError, TypeError):
            continue
    
    return results

def get_airports_by_type(airport_type: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their type (e.g., 'large_airport', 'medium_airport', 'small_airport', 'heliport', 'seaplane_base').
    
    Args:
        airport_type: The type of airport to filter by
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If the type is not a non-empty string
    """
    if not isinstance(airport_type, str) or len(airport_type) == 0:
        raise ValueError("Invalid type provided.")
    
    lower_case_type = airport_type.lower()
    results = []
    
    for airport in airports:
        if not airport.get("type"):
            continue
        
        airport_type_lower = airport["type"].lower()
        
        # Exact match first
        if airport_type_lower == lower_case_type:
            results.append(airport)
        # Allow partial matching for convenience (e.g., 'airport' matches 'large_airport')
        elif lower_case_type == 'airport' and 'airport' in airport_type_lower:
            results.append(airport)
    
    return results

def calculate_distance(code1: str, code2: str) -> Optional[float]:
    """
    Calculates the great-circle distance between two airports using their IATA or ICAO codes.
    
    Args:
        code1: The IATA or ICAO code of the first airport
        code2: The IATA or ICAO code of the second airport
    
    Returns:
        The distance in kilometers, or None if an airport is not found
    """
    airport1 = _get_airport_by_code(code1)
    airport2 = _get_airport_by_code(code2)
    
    if not airport1 or not airport2:
        return None
    
    try:
        return _haversine_distance(
            float(airport1["latitude"]), float(airport1["longitude"]),
            float(airport2["latitude"]), float(airport2["longitude"])
        )
    except (ValueError, TypeError, KeyError):
        return None

def get_autocomplete_suggestions(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Provides a list of airports for autocomplete suggestions based on a query.
    It searches by airport name, city, and IATA code with early termination.
    
    Args:
        query: The partial query string from the user
        limit: Maximum number of results to return (defaults to 10)
    
    Returns:
        A list of matching airports (limited to specified number)
    """
    if not isinstance(query, str) or len(query) < 2:
        return []
    
    lower_case_query = query.lower()
    results = []
    
    for airport in airports:
        if (lower_case_query in airport.get("airport", "").lower() or
            lower_case_query in airport.get("iata", "").lower()):
            results.append(airport)
            
            # Early termination when limit is reached for better performance
            if len(results) >= limit:
                break
    
    return results

def find_airports(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Finds airports that match multiple criteria.
    
    Args:
        filters: A dictionary of filters to apply
    
    Returns:
        A list of matching airports
    """
    results = []
    
    for airport in airports:
        match = True
        for key, filter_value in filters.items():
            if key == 'has_scheduled_service':
                # Check if the airport's scheduled_service matches the filter
                scheduled_service = airport.get('scheduled_service')
                
                # Convert string "yes"/"no" to boolean if needed
                if isinstance(scheduled_service, str):
                    actual_value = scheduled_service.upper() == 'TRUE'
                else:
                    actual_value = bool(scheduled_service)
                
                if actual_value != filter_value:
                    match = False
                    break
            
            elif key == 'min_runway_ft':
                try:
                    runway_length = int(airport.get('runway_length', 0))
                    if runway_length < filter_value:
                        match = False
                        break
                except (ValueError, TypeError):
                    match = False
                    break
            
            else:
                # For other filters, do exact match
                if airport.get(key) != filter_value:
                    match = False
                    break
        
        if match:
            results.append(airport)
    
    return results

def get_airports_by_timezone(timezone: str) -> List[Dict[str, Any]]:
    """
    Finds all airports within a specific timezone.
    
    Args:
        timezone: The timezone identifier (e.g., 'Europe/London')
    
    Returns:
        A list of matching airports
    
    Raises:
        ValueError: If timezone is empty
    """
    if not timezone:
        raise ValueError("Timezone cannot be empty.")
    
    return list(_timezone_index.get(timezone, []))

def get_airport_links(code: str) -> Optional[Dict[str, Optional[str]]]:
    """
    Gets a map of external links for a given airport.
    
    Args:
        code: The IATA or ICAO code of the airport
    
    Returns:
        A dictionary of links, or None if airport not found
    """
    airport = _get_airport_by_code(code)
    if not airport:
        return None
    
    return {
        'website': airport.get('website'),
        'wikipedia': airport.get('wikipedia'),
        'flightradar24': airport.get('flightradar24_url'),
        'radarbox': airport.get('radarbox_url'),
        'flightaware': airport.get('flightaware_url'),
    }

def get_airport_stats_by_country(country_code: str) -> Dict[str, Any]:
    """
    Gets comprehensive statistics about airports in a specific country.
    
    Args:
        country_code: 2-letter country code
    
    Returns:
        Dictionary containing statistics
    """
    airports_list = get_airport_by_country_code(country_code)
    
    stats = {
        'total': len(airports_list),
        'by_type': {
            'large_airport': 0,
            'medium_airport': 0,
            'small_airport': 0,
            'heliport': 0,
            'seaplane_base': 0,
            'closed': 0,
            'balloonport': 0
        },
        'with_scheduled_service': 0,
        'average_runway_length': 0,
        'average_elevation': 0,
        'timezones': set()
    }
    
    total_runway_length = 0
    runway_count = 0
    total_elevation = 0
    elevation_count = 0
    
    for airport in airports_list:
        # Type stats
        atype = airport.get('type')
        if atype in stats['by_type']:
            stats['by_type'][atype] += 1
            
        # Scheduled service
        scheduled = airport.get('scheduled_service')
        if scheduled == 'TRUE' or scheduled is True:
            stats['with_scheduled_service'] += 1
            
        # Runway length
        try:
            rl = airport.get('runway_length')
            if rl:
                total_runway_length += float(rl)
                runway_count += 1
        except (ValueError, TypeError):
            pass
            
        # Elevation
        try:
            el = airport.get('elevation_ft')
            if el is not None:
                total_elevation += float(el)
                elevation_count += 1
        except (ValueError, TypeError):
            pass
            
        # Timezone
        tz = airport.get('time')
        if tz:
            stats['timezones'].add(tz)
            
    if runway_count > 0:
        stats['average_runway_length'] = total_runway_length / runway_count
        
    if elevation_count > 0:
        stats['average_elevation'] = total_elevation / elevation_count
        
    stats['timezones'] = list(stats['timezones'])
    return stats

def get_airport_stats_by_continent(continent_code: str) -> Dict[str, Any]:
    """
    Gets comprehensive statistics about airports on a specific continent.
    
    Args:
        continent_code: 2-letter continent code
    
    Returns:
        Dictionary containing statistics
    """
    airports_list = get_airport_by_continent(continent_code)
    
    stats = {
        'total': len(airports_list),
        'by_country': {},
        'by_type': {
            'large_airport': 0,
            'medium_airport': 0,
            'small_airport': 0,
            'heliport': 0,
            'seaplane_base': 0,
            'closed': 0,
            'balloonport': 0
        },
        'with_scheduled_service': 0,
        'average_runway_length': 0,
        'average_elevation': 0,
        'timezones': set()
    }
    
    total_runway_length = 0
    runway_count = 0
    total_elevation = 0
    elevation_count = 0
    
    for airport in airports_list:
        # Country stats
        cc = airport.get('country_code')
        if cc:
            stats['by_country'][cc] = stats['by_country'].get(cc, 0) + 1
            
        # Type stats
        atype = airport.get('type')
        if atype in stats['by_type']:
            stats['by_type'][atype] += 1
            
        # Scheduled service
        scheduled = airport.get('scheduled_service')
        if scheduled == 'TRUE' or scheduled is True:
            stats['with_scheduled_service'] += 1
            
        # Runway length
        try:
            rl = airport.get('runway_length')
            if rl:
                total_runway_length += float(rl)
                runway_count += 1
        except (ValueError, TypeError):
            pass
            
        # Elevation
        try:
            el = airport.get('elevation_ft')
            if el is not None:
                total_elevation += float(el)
                elevation_count += 1
        except (ValueError, TypeError):
            pass
            
        # Timezone
        tz = airport.get('time')
        if tz:
            stats['timezones'].add(tz)
            
    if runway_count > 0:
        stats['average_runway_length'] = total_runway_length / runway_count
        
    if elevation_count > 0:
        stats['average_elevation'] = total_elevation / elevation_count
        
    stats['timezones'] = list(stats['timezones'])
    return stats

def get_largest_airports_by_continent(continent_code: str, limit: int = 10, sort_by: str = 'runway') -> List[Dict[str, Any]]:
    """
    Gets the largest airports on a continent by runway length or elevation.
    
    Args:
        continent_code: 2-letter continent code
        limit: Max number of results (default 10)
        sort_by: 'runway' or 'elevation' (default 'runway')
    
    Returns:
        List of airport objects
    """
    airports_list = get_airport_by_continent(continent_code)
    
    def get_sort_key(airport):
        try:
            if sort_by == 'elevation':
                val = airport.get('elevation_ft')
                return float(val) if val is not None else -1
            else: # runway
                val = airport.get('runway_length')
                return float(val) if val else -1
        except (ValueError, TypeError):
            return -1
            
    sorted_airports = sorted(airports_list, key=get_sort_key, reverse=True)
    return sorted_airports[:limit]

def get_multiple_airports(codes: List[str]) -> List[Optional[Dict[str, Any]]]:
    """
    Fetches multiple airports by their IATA or ICAO codes.
    
    Args:
        codes: List of IATA or ICAO codes
    
    Returns:
        List of airport objects (None for codes not found)
    """
    return [_get_airport_by_code(code) for code in codes]

def calculate_distance_matrix(codes: List[str]) -> Dict[str, Any]:
    """
    Calculates distances between all pairs of airports in a list.
    Pre-resolves all airports once to avoid redundant lookups in the inner loop.
    
    Args:
        codes: List of IATA or ICAO codes
    
    Returns:
        Dictionary with airport info and distance matrix
    """
    # Pre-resolve all airports once (O(k) lookups instead of O(k^2))
    resolved = {}
    airport_objs = []
    clean_codes = []
    
    for code in codes:
        ap = _get_airport_by_code(code)
        if ap:
            resolved[code] = ap
            airport_objs.append({
                'code': code,
                'name': ap.get('airport'),
                'iata': ap.get('iata'),
                'icao': ap.get('icao')
            })
            clean_codes.append(code)
    
    # Compute distances using pre-resolved airports directly
    distances = {}
    for code1 in clean_codes:
        distances[code1] = {}
        ap1 = resolved[code1]
        try:
            lat1 = float(ap1["latitude"])
            lon1 = float(ap1["longitude"])
        except (ValueError, TypeError, KeyError):
            for code2 in clean_codes:
                distances[code1][code2] = 0 if code1 == code2 else -1
            continue
        
        for code2 in clean_codes:
            if code1 == code2:
                distances[code1][code2] = 0
            elif code2 in distances and code1 in distances[code2]:
                # Reuse already-computed symmetric distance
                distances[code1][code2] = distances[code2][code1]
            else:
                ap2 = resolved[code2]
                try:
                    dist = _haversine_distance(
                        lat1, lon1,
                        float(ap2["latitude"]), float(ap2["longitude"])
                    )
                    distances[code1][code2] = dist
                except (ValueError, TypeError, KeyError):
                    distances[code1][code2] = -1
                
    return {
        'airports': airport_objs,
        'distances': distances
    }

def find_nearest_airport(lat: float, lon: float, filters: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Finds the single nearest airport to given coordinates, optionally with filters.
    
    Args:
        lat: Latitude
        lon: Longitude
        filters: Optional dictionary of filters
    
    Returns:
        Nearest airport object with 'distance' field, or None
    """
    nearest = None
    min_dist = float('inf')
    
    # Filter candidates first if needed
    candidates = airports
    if filters:
        candidates = find_airports(filters)
        
    for airport in candidates:
        airport_lat = airport.get("latitude")
        airport_lon = airport.get("longitude")
        if not airport_lat or not airport_lon:
            continue
            
        try:
            dist = _haversine_distance(lat, lon, float(airport_lat), float(airport_lon))
            
            if dist < min_dist:
                min_dist = dist
                nearest = airport.copy()  # Return copy to avoid modifying original
                nearest['distance'] = round(dist, 2)
                
        except (ValueError, TypeError):
            continue
            
    return nearest

def validate_iata_code(code: str) -> bool:
    """
    Validates if an IATA code exists in the database.
    
    Args:
        code: 3-letter IATA code to validate
        
    Returns:
        True if the code matches the format and exists in the database, False otherwise
    """
    if not isinstance(code, str) or not IATA_PATTERN.match(code.upper()):
        return False
    return _get_airport_by_code(code) is not None

def validate_icao_code(code: str) -> bool:
    """
    Validates if an ICAO code exists in the database.
    
    Args:
        code: 4-character ICAO code to validate
        
    Returns:
        True if the code matches the format and exists in the database, False otherwise
    """
    if not isinstance(code, str) or not ICAO_PATTERN.match(code.upper()):
        return False
    return _get_airport_by_code(code) is not None

def get_airport_count(filters: Optional[Dict[str, Any]] = None) -> int:
    """
    Gets the count of airports matching the given filters.
    
    Args:
        filters: Optional dictionary of filters to apply
        
    Returns:
        Total count of matching airports
    """
    if not filters:
        return len(airports)
    return len(find_airports(filters))

def is_airport_operational(code: str) -> bool:
    """
    Checks if an airport has scheduled commercial service.
    
    Args:
        code: IATA or ICAO code of the airport
        
    Returns:
        True if the airport has scheduled service, False otherwise
    """
    ap = _get_airport_by_code(code)
    if not ap:
        return False
        
    scheduled = ap.get('scheduled_service')
    return scheduled == 'TRUE' or scheduled is True