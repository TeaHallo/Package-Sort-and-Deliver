# Sommer Starr 001059225

from Package import Package
from ChainingHashTable import ChainingHashTable
import csv
from Truck import Truck

if __name__ == '__main__':
    truck1 = Truck(1)
    truck2 = Truck(2)
    package_table = ChainingHashTable()

    # Open package file. For each row, the items are read into variables and a package object is created.
    # The package object is then inserted into the created hash table
    with open('updated packages list.txt') as package_file:
        readCSV = csv.reader(package_file, delimiter=',')
        for row in readCSV:
            package_id = row[0]
            address = row[1]
            city = row[2]
            zip_code = row[3]
            weight = row[4]
            delivered_with = row[5]
            truck = row[6]
            at_hub_time = row[7]
            deadline = row[8]

            package = Package(package_id, address, city, zip_code, weight, delivered_with, truck, at_hub_time, deadline)
            package_table.insert(package)

    # Open address file. Each address is then inserted into the dictionary as a key, with an integer as its value
    # The dictionary is then inserted into the Truck class for use
    address_dict = {}
    with open('addresses.txt') as address_file:
        addresses = address_file.read().split("\n")
        for i in range(27):
            address_dict[addresses[i]] = i

    Truck.address_dict = address_dict

    # Opens the distance file. Creates a 2d array of the distances. The distance between two addresses can then be
    # found by first looking up each of the address's ids using the address dictionary, and then using the ids in the
    # distance_matrix to find the distance between them, ex: distance_matrix[0][5] equals the distance between address
    # at id 0 and id 5 which equals 3.5 miles. The 2d array is then inserted into the Truck class for use
    distance_matrix = [[] * 27] * 27
    with open('distances.txt') as distance_file:
        distances = distance_file.read().split('\n')
        # distance[0] is equal to the first row
        for i in range(27):
            distance = (distances[i]).split(',')
            distance_matrix[i] = distance

    Truck.distance_matrix = distance_matrix

    # Calls the primary algorithm for sorting the packages between trucks and calling the algorithm that will sort the
    # packages by distance and deliver them
    package_table.sort_packages(truck1, truck2)

    # User interface
    string = None
    while string != 'E':
        print('Enter D to display packages, T to display total distance or E to exit:')
        string = input()
        if string == 'D':
            print("Please enter military time with format '00:00' :")
            time = input()
            package_table.display_packages(time)
            print('\n')
        elif string == 'T':
            package_table.display_total_mileage()
            print('\n')
        elif string != 'E':
            print('Invalid input. Please try again')
            print('\n')














