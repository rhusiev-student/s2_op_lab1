"""
Lab1 closest films of a given year

https://github.com/rhusiev-student/s2_op_lab1
"""
import folium
import argparse
import haversine
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="lab1_task2")


def add_parser() -> argparse.Namespace:
    """
    Add parser for command line arguments

    Returns
    -------
    args : argparse.Namespace
        Parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("year", type=int)
    parser.add_argument("latitude", type=float)
    parser.add_argument("longitude", type=float)
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    return args


def get_films(args: argparse.Namespace) -> dict[str, list[str]]:
    """
    Get films shot in the given year from the file

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments

    Returns
    -------
    films : dict[str, list[str]]
        Dictionary with coordinates as keys and list of films as values
    """
    films = {}
    year = args.year
    path = args.path
    with open(path, "r", encoding="latin-1") as file:
        k = 0
        is_data = False
        for line in file.readlines():
            k += 1
            if k >= 200 or is_data and line.startswith("----------------------"):
                break
            if line.startswith("=============="):
                is_data = True
            elif is_data:
                tab_start = line.find("\t")
                tab_end = tab_start + 1
                for i in line[tab_start + 1 :]:
                    if i != "\t" and i != " ":
                        break
                    tab_start += 1
                year_end = line.rfind(")", 0, tab_start)
                year_start = line.rfind("(", 0, year_end)
                year = line[year_start + 1 : year_end].strip()
                while year.isdigit() is False:
                    year_end = line.rfind(")", 0, year_start)
                    year_start = line.rfind("(", 0, year_end)
                    year = line[year_start + 1 : year_end].strip()
                name = line[:year_start].replace("\t", "").strip()
                place = line[tab_end:].replace("\t", " ")
                # Remove from place if there are the last brackers and insides
                if place.rfind("(") != -1:
                    place = place[: place.rfind("(")].strip()
                location = geolocator.geocode(place, timeout=10)
                if location is None:
                    place = place[place.find(",") + 2 :]
                    location = geolocator.geocode(place, timeout=10)
                if location is not None:
                    coordinates = (location.latitude, location.longitude)
                    if year != str(args.year):
                        continue
                    if name in films:
                        films[coordinates].append(name)
                    else:
                        films[coordinates] = [name]
                else:
                    print(f"Not found {name} {year} at {place}")
    return films


def add_markers(films: dict, all_of_this_year_fg, closest_fg):
    """
    Add markers to the map

    Parameters
    ----------
    films : dict
        Dictionary with coordinates as keys and list of films as values

    all_of_this_year_fg : folium.FeatureGroup
        FeatureGroup for all films of this year

    closest_fg : folium.FeatureGroup
        FeatureGroup for closest films
    """
    closest = []
    for coordinates in films:
        for film in films[coordinates]:
            closest.append(
                (haversine.haversine(self_coordinates, coordinates), coordinates, film)
            )

    closest.sort(key=lambda x: x[0])

    print(f"{closest = }")

    used_coordinates = []
    i = 0
    while i < len(closest):
        close = closest[i]
        if close[1] in used_coordinates:
            close[1] = (close[1][0] + 0.001, close[1][1] + 0.001)
            closest[i] = close
        else:
            if i < 5:
                closest_fg.add_child(
                    folium.Marker(
                        location=close[1],
                        popup=close[2],
                        icon=folium.Icon(color="blue"),
                    )
                )
            else:
                all_of_this_year_fg.add_child(
                    folium.Marker(
                        location=close[1],
                        popup=close[2],
                        icon=folium.Icon(color="gray"),
                    )
                )
            used_coordinates.append(close[1])
            i += 1


if __name__ == "__main__":
    args = add_parser()
    films = get_films(args)

    self_coordinates = (args.latitude, args.longitude)
    map = folium.Map(location=self_coordinates, zoom_start=5)
    got_fg = folium.FeatureGroup(name="Got")
    html = """<h4> Got information: </h4>
    Coordinates: {} <br>
    Year: {} <br>
    <br>
    Gray - all films of this year <br>
    Green - closest films <br>
    """
    iframe = folium.IFrame(
        html=html.format(f"{self_coordinates[0]}, {self_coordinates[1]}", args.year),
        width=300,
        height=100,
    )
    got_fg.add_child(
        folium.Marker(
            location=self_coordinates,
            popup=folium.Popup(iframe),
            icon=folium.Icon(color="red"),
        )
    )

    all_of_this_year_fg = folium.FeatureGroup(name="All of this year")
    closest_fg = folium.FeatureGroup(name="Closest")
    add_markers(films, all_of_this_year_fg, closest_fg)

    map.add_child(got_fg)
    map.add_child(all_of_this_year_fg)
    map.add_child(closest_fg)

    map.save("map.html")

