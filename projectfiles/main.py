# Author: Beverly L Murray
# Student ID: #001328583
# C950 WGUPS

# MAIN FILE


import datetime
import csv

from hashtable import ChainingHashTable
from truck import Truck
from package import Package

# O(n) space complexity overall
# O(n^2) time complexity overall


# LOAD CSV

# space-time for loading csv data is O(n) because it depends on the amount of data, it goes through n times
# and uses n amount of data


# ADDRESS data from csv file

# declare list of addresses to fill with data from csv
addressList = list()
# load addresses into list


def load_address_data(filename):
    with open(filename) as addressRawData:
        address_data = csv.reader(addressRawData, delimiter=',')
        for address in address_data:
            addressList.append(address)


# load the address csv file
load_address_data('address_file.csv')


# DISTANCE data from csv file

# declare list of distances to fill with csv data
distanceList = list()
# load distance data into list


def load_distance_data(filename):
    with open(filename) as distanceRawData:
        distance_data = csv.reader(distanceRawData, delimiter=',')
        # for all the data in the file, add it to the distance list
        for (distance) in distance_data:
            distanceList.append(distance)


# load the  distance csv file
load_distance_data('distance_file.csv')


# PACKAGE data from csv file


# Task E and F
# packageHashTable is calling the hash table class from hashtable.py
# this hash table will store the package items as objects, using key-value pairs

packageHashTable = ChainingHashTable()

# declare list of packages
packageList = list()


# load package data
def load_package_data(filename):
    with open(filename) as packageRawData:
        package_data = csv.reader(packageRawData, delimiter=',')
        # for every package in the file, create package components
        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zipcode = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_notes = package[7]
            p_status = "At The Hub"  # they all start at the hub
            p_depart_time = None
            p_delivery_time = None
            package_data = Package(p_id, p_address, p_city, p_state, p_zipcode, p_deadline, p_weight, p_notes,
                                   p_status, p_depart_time, p_delivery_time)
            # insert package data into hash table
            packageHashTable.insert(p_id, package_data)
            # add package to the package list
            packageList.append(package)


# load the package csv file
load_package_data('package_file_with_notes.csv')


# O(n) space-time complexity for getAddressIDFromPackage

# get address ID from the package ID
# using arrays and their columns, package column 1 has the address,
# the address from the package is used to find a matching address in the address array column 2,
# column 0 holds the address id
# this will be used for getting the distance between two addresses in the distance file
def get_address_id_from_package(package_id):
    package_address = None
    # enumerate is a built-in function that adds a counter to an iterable and returns it
    # the enumerated object can then be used for a loop
    for index, package in enumerate(packageList):
        if package_id == index + 1:  # packageID starts at 1, index starts at 0, hence -> index + 1
            package_address = package[1]  # column 1 in packageList is the address
    for address in addressList:
        if package_address in address[2]:  # column 2 in addressList is address
            return int(address[0])  # column 0 in addressList is the address ID

# gets distance from the distance list that corresponds to the addressID that is obtained with getAddressIDFromPackage
# the distance is the same either way
# the excell sheet is set up to only work with the if first address id number is larger than the second address id
# there is an if/else statement to get the distance, this wouldn't be needed if the Excel sheet was filed out fully,
# but that would take longer than coding this
# O(1) because an if/else is either true or false which makes this a constant


def get_distance(address_one, address_two):
    if address_one > address_two:
        return float(distanceList[address_one][address_two])
    else:
        return float(distanceList[address_two][address_one])


# NEAREST NEIGHBOR ALGORITHM

# this will find the distance between one location and compare it to all other locations
# and will select the one closest to the starting location
# the algorithm is used on the truck
# the packages are already assigned to the truck
# the packages are in a random order
# after the algorith, the packages will be sorted

# When coding this section, I started with the algorith of sorting the packages into order, then I went through
# and added in the mileage tracker, then I could use the mileage to figure out the time, because I know the truck
# moves at a constant 18 miles per hour, I could take the distance in miles and divide it by 18 to get the hours and
# that will update the time which allows me to label what time a package is delivered

# time complexity is O(n^2) because of loops, in the worst case it goes through the code n * n times
# space complexity is O(n) because it only has to hold a set amount of data, n is the number of packages in this example

def nearest_neightbor_algorithm(truck):
    packages_in_order = []  # this is going to hold the packages in order after going through the algorithm
    packages_in_random = []  # this will be immediately filled with packages to put through the algorithm
    truck.mileage = 0.0  # keeping track of mileage
    time = truck.depart_time  # keeping track of time
    for package in truck.packages:  # for each package in the truck
        packages_in_random.append(package.package_id)  # add packages to the random list
    nearest_distance = float(100.0)  # set a large value to compare packages distances to
    first_package = None  # we need a variable to hold the closest package
    for package in packages_in_random:  # for each package in the random list
        distance = get_distance(0, get_address_id_from_package(package))  # use the get distance function
        if distance < nearest_distance:  # if the distance is closer
            nearest_distance = distance  # the distance is recorded to use and compare
            first_package = package  # the package that is closer is assigned here
    truck.mileage += nearest_distance  # the distance of the nearest package is added to the truck mileage
    time += datetime.timedelta(hours=nearest_distance / 18)  # the time is progressed based off 18mph
    package_update = packageHashTable.lookup(first_package)  # we find the package info from the hash table
    package_update.depart_time = truck.depart_time  # the package is given the departure hub time
    # the package deliver time is updated:
    package_update.delivery_time = (truck.depart_time + datetime.timedelta(hours=(truck.mileage / 18)))
    packages_in_order.append(first_package)  # the first package to be delivered is added to the in-order list
    packages_in_random.remove(first_package)  # the first package is taken off the random list

    while len(packages_in_random) > 0:  # while there are still packages not ordered
        nearest_distance = float(100.0)  # set a large number to a variable to compare and find the closest distance
        nearest_package = None  # this will hold the nearest package, can be assigned with None initially
        for package in packages_in_random:  # for each package on the random list
            # get the distance between packages by using getAddressIdFromPackage from the most recent package put in
            # the in-order list, which can be obtained with a (-1), and the getAddressIDFromPackage on the package
            # in the random list
            distance = get_distance(get_address_id_from_package(packages_in_order[-1]),
                                    get_address_id_from_package(package))
            if distance < nearest_distance:  # if the distance is found to be closer
                nearest_distance = distance  # this is now the nearest distance
                nearest_package = package  # the package is not the nearest package
        packages_in_order.append(nearest_package)  # add the package to the in-order list
        packages_in_random.remove(nearest_package)  # remove the package from the random list
        truck.mileage += nearest_distance  # the distance is added to the truck mileage
        # the time is found because we know the miles and speed is 18 mph:
        time += datetime.timedelta(hours=nearest_distance / 18)
        package_update = packageHashTable.lookup(nearest_package)  # look up the package in the hash table
        package_update.depart_time = truck.depart_time  # update the packages departure time (the same as truck's)
        # package delivery time is updated:
        package_update.delivery_time = (truck.depart_time + datetime.timedelta(hours=(truck.mileage / 18)))
    return packages_in_order  # we now have a list that gives us an efficient delivery route


# TRUCKS from the truck class

# truck(id, location, packages, mileage, depart_time)
# all trucks start at location 0 which is the hub
# O(1) space-time complexity

# truck 1
# this truck can leave at start of day, 8am
truck1 = Truck(1, 0, set(), 0.0, datetime.timedelta(hours=8))

# truck 2
# this truck contains a package that will not update in WGUPS system until 10:20am, so
# it will depart at 10:20am
truck2 = Truck(2, 0, set(), 0.0, datetime.timedelta(hours=10, minutes=20))

# truck 3
# this truck contains packages that are delayed on a flight, expected arrival is 9:05am, so
# it will depart at 9:45am because the driver of truck1 will be done at 9:32am
truck3 = Truck(3, 0, set(), 0.0, datetime.timedelta(hours=9, minutes=45))

# can add more trucks here


# manually load packages, limit of 16, paying attention to special notes and delivery deadlines
# I color coded the original Excel doc to aid in assigning packages to trucks

# get a list of package IDs on the truck
# for each package in the truck's list, add it to the truck
# use nearest neighbor algorith to find optimal delivery route

# O(1) space-time complexity because it is a constant, there is no "n" to go through

truck1PackageList = [1, 7, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
for packageID in truck1PackageList:
    truck1.add(packageHashTable.lookup(packageID))
truck1Route = nearest_neightbor_algorithm(truck1)

truck2PackageList = [3, 9, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
for packageID in truck2PackageList:
    truck2.add(packageHashTable.lookup(packageID))
truck2Route = nearest_neightbor_algorithm(truck2)

truck3PackageList = [2, 4, 5, 6, 8, 10, 11, 12, 17, 25, 28, 32, 33]
for packageID in truck3PackageList:
    truck3.add(packageHashTable.lookup(packageID))
truck3Route = nearest_neightbor_algorithm(truck3)

# if more trucks are added, they need to also be loaded and run through the algorithm here


# TEST PRINTS
# print(truck1.mileage)
# print(truck2.mileage)
# print(truck3.mileage)
# print(truck1.mileage + truck2.mileage + truck3.mileage)

# print("Truck 1 packages and delivery times:")
# truck1Packages = []
# for packages in truck1PackageList:
#    truck1Packages.append(packages)
# for packages in truck1Packages:
#    print(packageHashTable.lookup(packages))

# USER INTERFACE

def main():
    print("*~ WGUPS ~*")
    print("Total Mileage: " + str(truck1.mileage + truck2.mileage + truck3.mileage))
    print("Truck 1 (Driver A) Depart Time: " + str(truck1.depart_time)
          + "     Miles: " + str(round(truck1.mileage, 1)))
    print("Truck 2 (Driver B) Depart Time: " + str(truck2.depart_time)
          + "    Miles: " + str(round(truck2.mileage, 1)))
    print("Truck 3 (Driver A) Depart Time: " + str(truck3.depart_time)
          + "     Miles: " + str(round(truck3.mileage, 1)))
    print("\nMenu:")
    print("1. Get All Package Status")
    print("2. Get Single Package Status")
    user_input1 = input("Type '1' or '2' to start ")
    if user_input1 == "1":
        user_input2 = input("\nEnter Time: HH:MM:SS ")
        (h, m, s) = user_input2.split(":")
        convert_time_delta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        print("\nPackage ID, Address, City, State, Zipcode, Deadline, Weight, Status, In Transit Time, "
              "Delivery Time, Notes")
        for package_id in range(1, 41):
            package = packageHashTable.lookup(package_id)
            package.update_status(convert_time_delta)
            print(package)
    elif user_input1 == "2":
        user_input3 = input("\nEnter Package ID: ")
        user_input4 = input("\nEnter Time: HH:MM:SS ")
        (h, m, s) = user_input4.split(":")
        convert_time_delta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        package = packageHashTable.lookup(int(user_input3))
        package.update_status(convert_time_delta)
        print("\nPackage ID, Address, City, State, Zipcode, Deadline, Weight, Status, In Transit Time, "
              "Delivery Time, Notes")
        print(str(package))


main()
