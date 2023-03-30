import csv
from os import kill
import sys
import numpy as np

from util import Node, StackFrontier, QueueFrontier


# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"/Users/kristapsalmanis/Downloads/degrees/large/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"/Users/kristapsalmanis/Downloads/degrees/large/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"/Users/kristapsalmanis/Downloads/degrees/large/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")


    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        person1 = people[source]["name"]
        node = path[0]
        person2 = people[node.person]["name"]
        movie = movies[node.movie]["title"]
        print(f"1: {person1} and {person2} starred in {movie}")
        i = 1
        while (i < degrees):
            node = path[i-1]
            node2 = path[i]
            person1 = people[node.person]["name"]
            person2 = people[node2.person]["name"]
            movie = movies[node2.movie]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            i+=1

def shortest_path(source, target):
    frontier = []
    path = []
    tested = []

    neighbors = list(neighbors_for_person(source))
    neighborsLength = len(neighbors) - 1
    tested.append(source)

    neighbors_to_frontier(neighborsLength, neighbors, tested, frontier, source)

    while (len(frontier) >= 0):
        if (len(frontier) == 0):
            return
        node = frontier[0]
        if (node.person == target):
            break
        frontier.pop(0)
        neighbors = list(neighbors_for_person(node.person))
        neighborsLength = len(neighbors) - 1

        neighbors_to_frontier(neighborsLength, neighbors, tested, frontier, node)

    while (node != source):
        path.append(node)
        node = node.parent

    path.reverse()
    return path

def neighbors_to_frontier(neighborsLength, neighbors, tested, frontier, parent):
    k = 0
    while (k <= neighborsLength):
            if (neighbors[k][1] in tested):
                k+=1
            else:
                frontier.append(Node(neighbors[k][1], neighbors[k][0], parent))
                tested.append(neighbors[k][1])
                k+=1

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))

    return neighbors
    



if __name__ == "__main__":
    main()
