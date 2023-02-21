# Lab1 closest films of a given year
It is a simple program that takes a year and coordinates as input and returns the closest to that position films that were shot in that year.

# How to run
1. Clone the repository
2. Run the following command in the terminal:
```
python3 main.py <year> <latitude> <longitude> <path_to_file>
```
3. The program will create a map with the closest films to the given coordinates that were shot in the given year.

# Example
```
python3 main.py 2016 35.7128 -78.0060 ./locations.list
```
The program will create a map with the closest films to North Carolina that were shot in 2016.

# Requirements
- folium
- geopy
- argparse
- haversine

# License
GPL-3.0 License
