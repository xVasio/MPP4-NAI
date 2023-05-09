import csv
import random
import math


def read_csv(file):
    """
    Wczytanie danych z pliku csv z pominięciem ostatniej kolumny, która zawiera etykiety.
    """
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        return [list(map(float, row[:-1])) for row in csvreader]


def mean_centroids(data, assignment, k):
    """
    Metoda obliczająca średnią arytmetyczną puntków dla każdego klastra.
    """
    centroids = []
    for i in range(k):
        cluster_points = [data[j] for j in range(len(data)) if assignment[j] == i]
        centroid = [sum(col) / len(cluster_points) for col in zip(*cluster_points)]
        centroids.append(centroid)
    return centroids


def euclidean_distance(p1, p2):
    """
    Metoda obliczająca odległość euklidesową między dwoma punktami.
    """
    return math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(p1, p2)]))


def assign_to_centroids(data, centroids):
    """
    Metoda przypisująca punkty do klastrów na podstawie odległości euklidesowej.
    """
    assignment = []
    for i in range(len(data)):
        distances = [euclidean_distance(data[i], centroid) for centroid in centroids]
        assignment.append(distances.index(min(distances)))
    return assignment


def sum_of_squares(data, centroids, assignment):
    """
    Metoda obliczająca sumę kwadratów odległości w klastrach.
    """
    total = 0
    for i in range(len(data)):
        total += euclidean_distance(data[i], centroids[assignment[i]]) ** 2
    return total


def k_means(data, k):
    """
    Metoda implementująca algorytm k-średnich.
    """

    assignment = [random.randint(0, k - 1) for _ in range(len(data))]
    centroids = mean_centroids(data, assignment, k)

    prev_sum = math.inf
    no_improvement_count = 0
    iteration = 1
    while no_improvement_count < 2:
        assignment = assign_to_centroids(data, centroids)
        new_centroids = mean_centroids(data, assignment, k)

        if new_centroids == centroids:
            break
        centroids = new_centroids

        current_sum = sum_of_squares(data, centroids, assignment)
        if prev_sum == current_sum:
            no_improvement_count += 1
        else:
            no_improvement_count = 0
        prev_sum = current_sum

        print(f"Iteracje {iteration}:")
        print("Grupy:")
        for i in range(k):
            cluster_points = [data[j] for j in range(len(data)) if assignment[j] == i]
            print(f"  Grupy {i + 1}: {cluster_points}")
        print(f"Suma kwadratów odległości w klastrach: {current_sum}\n")

        iteration += 1


if __name__ == '__main__':
    csv_file = "data.csv"
    k = int(input("Podaj liczbę klastrów: "))
    data = read_csv(csv_file)
    k_means(data, k)