# Author: Beverly L Murray
# Student ID: #001328583
# C950 WGUPS

# truck class

# O(1) space-time complexity

class Truck:
    def __init__(self, truck_id, location, packages, mileage, depart_time):
        self.truck_id = truck_id
        self.location = location
        self.packages = packages
        self.mileage = mileage
        self.depart_time = depart_time
        self.time = depart_time

    def add(self, package_id):
        self.packages.add(package_id)

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.truck_id, self.location, self.packages, self.mileage, self.depart_time)
