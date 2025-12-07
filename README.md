# airports-py

A comprehensive Python library providing easy retrieval of airport data based on IATA, ICAO, city codes, country codes, and continents. Ideal for developers building applications related to aviation, travel, and geography in Python.

## Features

- 🌍 **Comprehensive airport database** with worldwide coverage
- 🔍 **Search by IATA codes, ICAO codes, country, continent, and more**
- 📍 **Geographic proximity search** with customizable radius
- 🔗 **External links** to Wikipedia, airport websites, and flight tracking services
- 📏 **Distance calculation** between airports
- 🏷️ **Filter by airport type** (large_airport, medium_airport, small_airport, heliport, seaplane_base)
- 🕒 **Timezone-based airport lookup**
- 💡 **Autocomplete suggestions** for search interfaces
- 🎯 **Advanced multi-criteria filtering**
- **Built-in error handling** for invalid input formats
- **Efficiently packaged** with gzipped data

## Installation

You can install `airports-py` using pip:

```bash
pip install airports-py
```

## Airport Data Structure

Each airport object contains the following fields:

```python
{
    "iata": "SIN",                    # 3-letter IATA code
    "icao": "WSSS",                   # 4-letter ICAO code
    "time": "Asia/Singapore",         # Timezone identifier
    "country_code": "SG",             # 2-letter country code
    "continent": "AS",                # 2-letter continent code (AS, EU, NA, SA, AF, OC, AN)
    "airport": "Singapore Changi Airport",  # Airport name
    "latitude": "1.35019",            # Latitude coordinate
    "longitude": "103.994003",        # Longitude coordinate
    "elevation": "22",                # Elevation in feet
    "type": "large_airport",          # Airport type
    "scheduled_service": "yes",       # Has scheduled commercial service
    "wikipedia": "https://en.wikipedia.org/wiki/Singapore_Changi_Airport",
    "website": "https://www.changiairport.com",
    "runway_length": "13200",         # Longest runway in feet
    "flightradar24_url": "https://www.flightradar24.com/airport/SIN",
    "radarbox_url": "https://www.radarbox.com/airport/WSSS",
    "flightaware_url": "https://www.flightaware.com/live/airport/WSSS"
}
```

## Basic Usage

```python
from airports import airport_data

# Get airport by IATA code
airport_by_iata = airport_data.get_airport_by_iata("SIN")
print(airport_by_iata[0]["airport"])  # "Singapore Changi Airport"

# Get airport by ICAO code
airport_by_icao = airport_data.get_airport_by_icao("WSSS")
print(airport_by_icao[0]["country_code"])  # "SG"

# Search airports by name
airports = airport_data.search_by_name("Singapore")
print(len(airports))  # Multiple airports matching "Singapore"

# Find nearby airports (within 50km of coordinates)
nearby = airport_data.find_nearby_airports(1.35019, 103.994003, 50)
print(nearby)  # Airports near Singapore Changi
```

## API Reference

### Core Search Functions

#### `get_airport_by_iata(iata_code)`
Finds airports by their 3-letter IATA code.

```python
airports = airport_data.get_airport_by_iata('LHR')
# Returns list of airports with IATA code 'LHR'
```

#### `get_airport_by_icao(icao_code)`
Finds airports by their 4-character ICAO code.

```python
airports = airport_data.get_airport_by_icao('EGLL')
# Returns list of airports with ICAO code 'EGLL'
```

#### `search_by_name(query)`
Searches for airports by name (case-insensitive, minimum 2 characters).

```python
airports = airport_data.search_by_name('Heathrow')
# Returns airports with 'Heathrow' in their name
```

### Geographic Functions

#### `find_nearby_airports(lat, lon, radius_km=100)`
Finds airports within a specified radius of given coordinates.

```python
nearby = airport_data.find_nearby_airports(51.5074, -0.1278, 100)
# Returns airports within 100km of London coordinates
```

#### `calculate_distance(code1, code2)`
Calculates the great-circle distance between two airports using IATA or ICAO codes.

```python
distance = airport_data.calculate_distance('LHR', 'JFK')
# Returns distance in kilometers (approximately 5540)
```

### Filtering Functions

#### `get_airport_by_country_code(country_code)`
Finds all airports in a specific country.

```python
us_airports = airport_data.get_airport_by_country_code('US')
# Returns all airports in the United States
```

#### `get_airport_by_continent(continent_code)`
Finds all airports on a specific continent.

```python
asian_airports = airport_data.get_airport_by_continent('AS')
# Returns all airports in Asia
# Continent codes: AS, EU, NA, SA, AF, OC, AN
```

#### `get_airports_by_type(airport_type)`
Finds airports by their type.

```python
large_airports = airport_data.get_airports_by_type('large_airport')
# Available types: large_airport, medium_airport, small_airport, heliport, seaplane_base

# Convenience search for all airports
all_airports = airport_data.get_airports_by_type('airport')
# Returns large_airport, medium_airport, and small_airport
```

#### `get_airports_by_timezone(timezone)`
Finds all airports within a specific timezone.

```python
london_airports = airport_data.get_airports_by_timezone('Europe/London')
# Returns airports in London timezone
```

### Advanced Functions

#### `find_airports(filters)`
Finds airports matching multiple criteria.

```python
# Find large airports in Great Britain with scheduled service
airports = airport_data.find_airports({
    'country_code': 'GB',
    'type': 'large_airport',
    'has_scheduled_service': True
})

# Find airports with minimum runway length
long_runway_airports = airport_data.find_airports({
    'min_runway_ft': 10000
})
```

#### `get_autocomplete_suggestions(query, limit=10)`
Provides autocomplete suggestions for search interfaces (returns max 10 results by default).

```python
suggestions = airport_data.get_autocomplete_suggestions('Lon')
# Returns up to 10 airports matching 'Lon' in name or IATA code
```

#### `get_airport_links(code)`
Gets external links for an airport using IATA or ICAO code.

```python
links = airport_data.get_airport_links('SIN')
# Returns:
# {
#     'website': "https://www.changiairport.com",
#     'wikipedia': "https://en.wikipedia.org/wiki/Singapore_Changi_Airport",
#     'flightradar24': "https://www.flightradar24.com/airport/SIN",
#     'radarbox': "https://www.radarbox.com/airport/WSSS",
#     'flightaware': "https://www.flightaware.com/live/airport/WSSS"
# }
```
### Statistical & Analytical Functions
 
 #### `get_airport_stats_by_country(country_code)`
 Gets comprehensive statistics about airports in a specific country.
 
 ```python
 stats = airport_data.get_airport_stats_by_country('US')
 # Returns:
 # {
 #   'total': 5432,
 #   'by_type': {
 #     'large_airport': 139,
 #     'medium_airport': 467,
 #     'small_airport': 4826,
 #     ...
 #   },
 #   'with_scheduled_service': 606,
 #   'average_runway_length': 5234,
 #   'average_elevation': 1245,
 #   'timezones': ['America/New_York', 'America/Chicago', ...]
 # }
 ```
 
 #### `get_airport_stats_by_continent(continent_code)`
 Gets comprehensive statistics about airports on a specific continent.
 
 ```python
 stats = airport_data.get_airport_stats_by_continent('AS')
 # Returns statistics for Asian airports
 ```
 
 #### `get_largest_airports_by_continent(continent_code, limit=10, sort_by='runway')`
 Gets the largest airports on a continent by runway length or elevation.
 
 ```python
 # Get top 5 airports in Asia by runway length
 top_airports = airport_data.get_largest_airports_by_continent('AS', limit=5, sort_by='runway')
 
 # Get top 10 airports by elevation
 high_airports = airport_data.get_largest_airports_by_continent('SA', limit=10, sort_by='elevation')
 ```
 
 ### Bulk Operations
 
 #### `get_multiple_airports(codes)`
 Fetches multiple airports by their IATA or ICAO codes in one call.
 
 ```python
 airports = airport_data.get_multiple_airports(['SIN', 'LHR', 'JFK', 'WSSS'])
 # Returns list of airport objects (None for codes not found)
 ```
 
 #### `calculate_distance_matrix(codes)`
 Calculates distances between all pairs of airports in a list.
 
 ```python
 matrix = airport_data.calculate_distance_matrix(['SIN', 'LHR', 'JFK'])
 # Returns:
 # {
 #   'airports': [...],
 #   'distances': {
 #     'SIN': { 'SIN': 0, 'LHR': 10872, 'JFK': 15344 },
 #     ...
 #   }
 # }
 ```
 
 #### `find_nearest_airport(lat, lon, filters=None)`
 Finds the single nearest airport to given coordinates, optionally with filters.
 
 ```python
 # Find nearest airport
 nearest = airport_data.find_nearest_airport(1.35019, 103.994003)
 print(f"{nearest['airport']} is {nearest['distance']} km away")
 
 # Find nearest large airport with scheduled service
 nearest_hub = airport_data.find_nearest_airport(1.35019, 103.994003, {
     'type': 'large_airport',
     'has_scheduled_service': True
 })
 ```
 
 ### Validation & Utilities
 
 #### `validate_iata_code(code)` / `validate_icao_code(code)`
 Validates if a code exists in the database.
 
 ```python
 is_valid = airport_data.validate_iata_code('SIN')  # True
 ```
 
 #### `get_airport_count(filters)`
 Gets the count of airports matching the given filters.
 
 ```python
 count = airport_data.get_airport_count({
     'country_code': 'US', 
     'type': 'large_airport'
 })
 ```
 
 #### `is_airport_operational(code)`
 Checks if an airport has scheduled commercial service.
 
 ```python
 is_operational = airport_data.is_airport_operational('SIN')  # True
 ```

## Error Handling

All functions raise appropriate exceptions for invalid input or when no data is found.

```python
try:
    airport = airport_data.get_airport_by_iata('XYZ')
except ValueError as e:
    print(e)  # "No data found for IATA code: XYZ"
```

## Examples

### Find airports near a city

```python
# Find airports within 100km of Paris
paris_airports = airport_data.find_nearby_airports(48.8566, 2.3522, 100)
print(f"Found {len(paris_airports)} airports near Paris")
```

### Get flight distance

```python
# Calculate distance between Singapore and London
distance = airport_data.calculate_distance('SIN', 'LHR')
print(f"Distance: {round(distance)} km")
```

### Build an airport search interface

```python
# Get autocomplete suggestions
suggestions = airport_data.get_autocomplete_suggestions('New York')
for airport in suggestions:
    print(f"{airport['iata']} - {airport['airport']}")
```

### Filter airports by multiple criteria

```python
# Find large airports in Asia with scheduled service
asian_hubs = airport_data.find_airports({
    'continent': 'AS',
    'type': 'large_airport',
    'has_scheduled_service': True
})
```

### Using Command-Line Interface (CLI)

You can also directly execute Python code from the CLI without entering the interactive shell. Navigate to the root of your project and run:

```bash
python3 -c "from airports import airport_data; result = airport_data.get_airport_by_iata('MAA'); print(result)"
```

Replace `'MAA'` with other codes as needed.

## Testing

To test the library locally:

1. Navigate to the root of the project:

```bash
cd path_to_airports-py
```

2. Run the tests using:

```bash
python3 -m unittest discover tests -v
```

This command will discover and run all test files inside the `tests` directory and provide a detailed output.

## Example Data Fields

For Chennai International Airport:

| Field Name           | Data                                                     |
|----------------------|----------------------------------------------------------|
| IATA                 | MAA                                                      |
| ICAO                 | VOMM                                                     |
| Time Zone            | Asia/Kolkata                                             |
| City Code            | MAA                                                      |
| Country Code         | IN                                                       |
| Name                 | Chennai International Airport                            |
| Latitude             | 12.99                                                    |
| Longitude            | 80.1693                                                  |
| Altitude (in feet)   | 52                                                       |
| State                | Tamil Nadu                                               |
| City                 | Pallavaram                                               |
| County               | Kancheepuram                                             |
| State Code           | Tamil Nadu                                               |
| Airport Type         | large_airport                                            |
| Continent            | AS                                                       |
| State Abbreviation   | IN-TN                                                    |
| International        | TRUE                                                     |
| Wikipedia Link       | [Wikipedia](https://en.wikipedia.org/wiki/Chennai_International_Airport)|
| Official Website     | [Chennai Airport](http://chennaiairport.com)            |
| Location ID          | 12513629                                                 |
| Phone Number         | 044-2340551                                              |
| Runway Length (in meters) | 10050                                               |
| Flightradar24        | [Flightradar24](https://www.flightradar24.com/airport/MAA)|
| Radarbox             | [Radarbox](https://www.radarbox.com/airport/VOMM)       |
| Flightaware Link     | [Flightaware](https://www.flightaware.com/live/airport/VOMM)|

### Singapore Changi Airport:

| Field Name           | Data                                                     |
|----------------------|----------------------------------------------------------|
| IATA                 | SIN                                                      |
| ICAO                 | WSSS                                                     |
| Time Zone            | Asia/Singapore                                           |
| City Code            | SIN                                                      |
| Country Code         | SG                                                       |
| Name                 | Singapore Changi Airport                                 |
| Latitude             | 1.35019                                                  |
| Longitude            | 103.994                                                  |
| Altitude (in feet)   | 22                                                       |
| State                | Singapore                                                |
| City                 | Singapore                                                |
| County               | Singapore                                                |
| State Code           | South East                                               |
| Airport Type         | large_airport                                            |
| Continent            | AS                                                       |
| State Abbreviation   | SG-04                                                    |
| International        | TRUE                                                     |
| Wikipedia Link       | [Wikipedia](https://en.wikipedia.org/wiki/Singapore_Changi_Airport)|
| Official Website     | [Changi Airport](http://www.changiairport.com/)         |
| Location ID          | 12517525                                                 |
| Phone Number         | (65) 6542 1122                                           |
| Runway Length (in meters) | 13200                                               |
| Flightradar24         | [Flightradar24](https://www.flightradar24.com/airport/SIN)|
| Radarbox              | [Radarbox](https://www.radarbox.com/airport/WSSS)       |
| Flightaware           | [Flightaware](https://www.flightaware.com/live/airport/WSSS)|

## Changelog

### Version 2.1.0 (Latest)
 
 #### 🆕 New Features
 - **`get_airport_stats_by_country(country_code)`** - Comprehensive country-level airport statistics
 - **`get_airport_stats_by_continent(continent_code)`** - Continent-level statistics
 - **`get_largest_airports_by_continent`** - Find top airports by runway length or elevation
 - **`get_multiple_airports(codes)`** - Bulk fetch by IATA/ICAO codes
 - **`calculate_distance_matrix(codes)`** - Calculate distances between all pairs of airports
 - **`find_nearest_airport(lat, lon, filters)`** - Find single nearest airport with optional filtering
 - **`validate_iata_code`** / **`validate_icao_code`** - Validation utilities
 - **`is_airport_operational(code)`** - Check scheduled service status
 - **`get_airport_count(filters)`** - Efficient filtered counting
 
 #### 🔄 Improvements
 - **Fixed `find_airports`** to correctly handle boolean filters stored as strings ("TRUE"/"FALSE")
 - **`get_airports_by_timezone(timezone)`** - Find airports by timezone
 - **`get_airport_links(code)`** - Get external links for airports
 - **`find_airports(filters)`** - Advanced multi-criteria filtering
 - **`get_autocomplete_suggestions(query)`** - Autocomplete functionality
 - **Enhanced `get_airports_by_type(type)`** - Now supports convenience search for "airport" type
 - **`search_by_name(query)`** - Search airports by name
 - **`find_nearby_airports(lat, lon, radius_km)`** - Geographic proximity search
 - **`calculate_distance(code1, code2)`** - Distance calculation between airports
 - **External links support** - Wikipedia, websites, and flight tracking URLs
 - **Timezone information** - Complete timezone data for all airports
 - **Runway length data** - Airport runway information included
 - **Scheduled service indicator** - Whether airports have commercial scheduled service

#### 🔄 Improvements
- Better error handling and validation with specific error messages
- More comprehensive airport data structure
- Improved type filtering with partial matching
- Enhanced geographic calculations using great-circle distance
- Case-insensitive search improvements
- Comprehensive test coverage for all functions

#### ❌ Removed from v1.x
- Legacy simple filtering (replaced with advanced `find_airports` function)
- Basic airport objects (expanded to include more fields)

## Running the Project Locally

### Prerequisites
- Python 3.6 or higher
- Git

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/aashishvanand/airports-py.git
```

2. **Change into the cloned directory:**
```bash
cd airports-py
```

3. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
```

4. **Activate the virtual environment:**
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

5. **Install development dependencies:**
```bash
pip install --upgrade pip
pip install build twine pytest pytest-cov
```

6. **Install the package in development mode:**
```bash
pip install -e .
```

7. **Generate the compressed data file (if needed):**
```bash
# Generate airports.gz from airports.json
python scripts/generate_airports_gz.py

# Verify the data file
python scripts/generate_airports_gz.py --verify-only
```

### Testing

8. **Run all tests:**
```bash
python -m unittest discover tests -v
```

9. **Run tests with pytest (alternative):**
```bash
python -m pytest tests/ -v
```

10. **Run tests with coverage:**
```bash
python -m pytest tests/ -v --cov=airports --cov-report=term-missing
```

11. **Test basic functionality manually:**
```bash
python -c "
from airports import airport_data
print('Testing IATA lookup:')
result = airport_data.get_airport_by_iata('LHR')
print(f'Found: {result[0][\"airport\"]}')
print('✅ Basic functionality working!')
"
```

### Building and Validation

12. **Build the package:**
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python -m build
```

13. **Validate the package:**
```bash
twine check dist/*
```

14. **Test package installation:**
```bash
pip install dist/airports_py-*.whl --force-reinstall
```

### Development Scripts

The project includes utility scripts in the `scripts/` directory:

#### Generate Compressed Data File
```bash
# Generate airports.gz from airports.json
python scripts/generate_airports_gz.py

# Generate with custom compression level
python scripts/generate_airports_gz.py --compression 6

# Generate with custom source/output files
python scripts/generate_airports_gz.py --source custom_data.json --output custom_data.gz

# Verify existing compressed file
python scripts/generate_airports_gz.py --verify-only
```

### Quick Development Workflow

For ongoing development, use this workflow:

```bash
# 1. Make your changes to the code

# 2. Regenerate data file if JSON was updated
python scripts/generate_airports_gz.py

# 3. Run tests
python -m pytest tests/ -v

# 4. Build and validate
python -m build && twine check dist/*

# 5. Test installation
pip install dist/airports_py-*.whl --force-reinstall
```

### Troubleshooting

**If you get import errors:**
- Ensure you're in the virtual environment: `which python` should show the venv path
- Verify the package is installed: `pip list | grep airports`
- Check import works: `python -c "import airports.airport_data"`

**If data file is missing:**
- Generate it: `python scripts/generate_airports_gz.py`
- Verify location: `ls -la airports/data/airports.gz`
- Check file integrity: `python scripts/generate_airports_gz.py --verify-only`

**If tests fail:**
- Ensure data file exists and is valid
- Check that all dependencies are installed: `pip install pytest pytest-cov`
- Run individual tests: `python -m pytest tests/test_airport_data.py::TestAirportData::test_get_airport_by_iata -v`

**If build fails:**
- Ensure `setup.py` has correct package data configuration
- Check that `airports/data/airports.gz` exists and is included in package

### Deactivating Environment

When you're done developing:
```bash
deactivate
```

## Data Management

The airport data is stored in `airports/data/` directory:
- `airports.json` - Source data in JSON format (4.7MB)
- `airports.gz` - Compressed data used by the library (617KB, 86.9% compression)

### Updating Airport Data

1. **Update the source JSON file:**
```bash
# Edit airports/data/airports.json with new airport data
```

2. **Regenerate the compressed file:**
```bash
python scripts/generate_airports_gz.py
```

3. **Verify the update:**
```bash
python scripts/generate_airports_gz.py --verify-only
python -c "from airports import airport_data; print(f'Loaded {len(airport_data.airports)} airports')"
```

4. **Run tests to ensure compatibility:**
```bash
python -m pytest tests/ -v
```

## Data Source

This library uses a comprehensive dataset of worldwide airports with regular updates to ensure accuracy and completeness.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/aashishvanand/airports-py/issues).