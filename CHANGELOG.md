# Changelog

All notable changes to this project will be documented in this file.

## [3.1.0] - 2026-03-11

### Added
- Comprehensive test coverage for all statistical, bulk, validation, and utility functions (30 new test cases)
- Tests for `get_airport_stats_by_country`, `get_airport_stats_by_continent`, `get_largest_airports_by_continent`
- Tests for `get_multiple_airports`, `calculate_distance_matrix`, `find_nearest_airport`
- Tests for `validate_iata_code`, `validate_icao_code`, `get_airport_count`, `is_airport_operational`

### Fixed
- README data structure now accurately reflects actual field names and types (`elevation_ft`, `utc`, float coordinates, int runway_length, string `"TRUE"`/`"FALSE"` for scheduled_service)
- README error handling section corrected: valid-but-nonexistent codes return empty list, only invalid formats raise `ValueError`
- README changelog section now points to this CHANGELOG.md

### Documentation
- Added `get_airport_by_city_code` to API reference (was implemented but undocumented)
- Added examples for statistics, bulk operations, validation utilities, and nearest airport search
- Aligned README examples with JS library documentation for consistency

## [3.0.0] - 2024-12-01

### Added
- Multiple O(1) lookup indexes for IATA, ICAO, country, continent, city code, and timezone
- Centralized Haversine distance calculations at module level
- Name index for faster `search_by_name` performance

### Changed
- Major performance improvements through pre-built indexes (O(1) vs O(n) lookups)
- Refactored all lookup functions to use index-based retrieval
- Updated GitHub Actions workflow with explicit permissions and pinned dependencies

### Breaking Changes
- Internal data structure changes may affect code that directly accesses module internals

## [2.1.0] - 2024-11-01

### Added
- `get_airport_stats_by_country(country_code)` - Comprehensive country-level airport statistics
- `get_airport_stats_by_continent(continent_code)` - Continent-level statistics with country breakdown
- `get_largest_airports_by_continent(continent_code, limit, sort_by)` - Top airports by runway length or elevation
- `get_multiple_airports(codes)` - Bulk fetch by IATA/ICAO codes
- `calculate_distance_matrix(codes)` - Distance matrix between all pairs of airports
- `find_nearest_airport(lat, lon, filters)` - Find single nearest airport with optional filtering
- `validate_iata_code(code)` / `validate_icao_code(code)` - Code validation utilities
- `is_airport_operational(code)` - Check scheduled service status
- `get_airport_count(filters)` - Efficient filtered counting
- `get_airports_by_timezone(timezone)` - Find airports by timezone
- `get_airport_links(code)` - Get external links (Wikipedia, website, flight tracking)
- `find_airports(filters)` - Advanced multi-criteria filtering
- `get_autocomplete_suggestions(query)` - Autocomplete functionality for search interfaces
- `search_by_name(query)` - Search airports by name
- `find_nearby_airports(lat, lon, radius_km)` - Geographic proximity search
- `calculate_distance(code1, code2)` - Distance calculation between airports
- Enhanced `get_airports_by_type(type)` with convenience search for "airport" type

### Fixed
- `find_airports` now correctly handles boolean filters stored as strings ("TRUE"/"FALSE")

### Improved
- Better error handling and validation with specific error messages
- Improved type filtering with partial matching
- Enhanced geographic calculations using great-circle distance
- Case-insensitive search across all lookup functions

## [2.0.0] - 2024-10-01

### Changed
- Bumped version to 2.0.0 with enhanced package metadata
- Improved CI/CD pipeline
- Enhanced package functionality

## [1.0.0] - 2024-09-01

### Added
- Initial release
- Basic airport lookup by IATA code
- Airport lookup by ICAO code
- Airport lookup by city code
- Airport lookup by country code
- Airport lookup by continent
- Gzipped data for efficient distribution
- Error handling for invalid inputs
