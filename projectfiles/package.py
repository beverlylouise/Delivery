# Author: Beverly L Murray
# Student ID: #001328583
# C950 WGUPS

# package class

# O(1) space-time complexity

class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, notes, status,
                 depart_time, delivery_time):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.depart_time = depart_time
        self.delivery_time = delivery_time

    # change status of package
    def update_status(self, time):
        if time > self.delivery_time:
            self.status = "Delivered"
        elif time < self.depart_time:
            self.status = "At The Hub"
        else:
            self.status = "In Transit"

    # delivery time of package
    def update_delivery_time(self, new_delivery_time):
        self.delivery_time = new_delivery_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state,
                                                               self.zipcode, self.deadline, self.weight, self.status,
                                                               self.depart_time, self.delivery_time, self.notes)
