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
    "utc": 8,                         # UTC offset in hours (int)
    "country_code": "SG",             # 2-letter country code
    "continent": "AS",                # 2-letter continent code (AS, EU, NA, SA, AF, OC, AN)
    "airport": "Singapore Changi Airport",  # Airport name
    "latitude": 1.361173,             # Latitude coordinate (float)
    "longitude": 103.990201,          # Longitude coordinate (float)
    "elevation_ft": 193068,           # Elevation in feet (int)
    "type": "large_airport",          # Airport type
    "scheduled_service": "TRUE",      # Has scheduled commercial service ("TRUE"/"FALSE")
    "wikipedia": "https://en.wikipedia.org/wiki/Singapore_Changi_Airport",
    "website": "http://www.changiairport.com",
    "runway_length": 13200,           # Longest runway in feet (int)
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

#### `get_airport_by_city_code(city_code)`
Finds airports by their city code.

```python
airports = airport_data.get_airport_by_city_code('NYC')
# Returns all airports associated with New York City
```

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

Functions raise `ValueError` for **invalid input formats** (e.g., wrong length, invalid characters). For valid formats that simply don't match any airport, an empty list is returned instead.

```python
# Invalid format raises ValueError
try:
    airport = airport_data.get_airport_by_iata('AB')  # Too short
except ValueError as e:
    print(e)  # "Invalid IATA format. Please provide a 3-letter code, e.g., 'AAA'."

# Valid format but non-existent code returns empty list
result = airport_data.get_airport_by_iata('XYZ')
print(result)  # []
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

### Get airport statistics

```python
# Get comprehensive statistics for US airports
us_stats = airport_data.get_airport_stats_by_country('US')
print(f"Total airports: {us_stats['total']}")
print(f"Large airports: {us_stats['by_type']['large_airport']}")
print(f"Average runway length: {us_stats['average_runway_length']} ft")

# Get statistics for Asian airports
asia_stats = airport_data.get_airport_stats_by_continent('AS')
print(f"Countries with airports: {len(asia_stats['by_country'])}")
```

### Bulk operations

```python
# Fetch multiple airports at once
airports = airport_data.get_multiple_airports(['SIN', 'LHR', 'JFK', 'NRT'])
for ap in airports:
    if ap:
        print(f"{ap['iata']}: {ap['airport']}")

# Calculate distance matrix for route planning
matrix = airport_data.calculate_distance_matrix(['SIN', 'LHR', 'JFK'])
print(f"Distance from SIN to LHR: {matrix['distances']['SIN']['LHR']:.0f} km")
print(f"Distance from LHR to JFK: {matrix['distances']['LHR']['JFK']:.0f} km")
```

### Validation utilities

```python
# Validate airport codes before processing
codes = ['SIN', 'XYZ', 'LHR', 'ABCD']
for code in codes:
    is_valid = airport_data.validate_iata_code(code)
    print(f"{code}: {'Valid' if is_valid else 'Invalid'}")

# Check if airport is operational
operational = airport_data.is_airport_operational('SIN')
print(f"Singapore Changi is operational: {operational}")
```

### Find nearest airport

```python
# Find nearest airport to current location
nearest = airport_data.find_nearest_airport(1.35019, 103.994003)
print(f"Nearest airport: {nearest['airport']} ({nearest['distance']} km away)")

# Find nearest large airport with scheduled service
nearest_hub = airport_data.find_nearest_airport(1.35019, 103.994003, {
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

For Singapore Changi Airport (as returned by the library):

| Key                  | Value                                                    |
|----------------------|----------------------------------------------------------|
| `iata`               | `"SIN"`                                                  |
| `icao`               | `"WSSS"`                                                 |
| `airport`            | `"Singapore Changi Airport"`                             |
| `time`               | `"Asia/Singapore"`                                       |
| `utc`                | `8`                                                      |
| `country_code`       | `"SG"`                                                   |
| `continent`          | `"AS"`                                                   |
| `latitude`           | `1.361173`                                               |
| `longitude`          | `103.990201`                                             |
| `elevation_ft`       | `193068`                                                 |
| `type`               | `"large_airport"`                                        |
| `scheduled_service`  | `"TRUE"`                                                 |
| `runway_length`      | `13200`                                                  |
| `wikipedia`          | `"https://en.wikipedia.org/wiki/Singapore_Changi_Airport"` |
| `website`            | `"http://www.changiairport.com"`                         |
| `flightradar24_url`  | `"https://www.flightradar24.com/airport/SIN"`            |
| `radarbox_url`       | `"https://www.radarbox.com/airport/WSSS"`                |
| `flightaware_url`    | `"https://www.flightaware.com/live/airport/WSSS"`        |

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history and release notes.

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