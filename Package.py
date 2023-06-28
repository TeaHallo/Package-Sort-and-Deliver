class Package:
    def __init__(self, package_id, address, city, zip_code, weight, delivered_with, truck=None,
                 at_hub_time=None, deadline=None, delivery_status='At Hub', time_delivered=None, delivery_truck=None,
                 en_route_time=None, state='UT'):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.delivered_with = delivered_with.split(' ')
        self.truck_number = truck
        self.delivery_truck = delivery_truck
        self.at_hub_time = at_hub_time
        self.delivery_deadline = deadline
        self.delivery_status = delivery_status
        self.time_delivered = time_delivered
        self.en_route_time = en_route_time

    # Prints all package object variables for ease in checking for accuracy
    def __str__(self):
        return ('ID: {0}, Address: {1}, City: {2}, Zip Code: {3}, State: {4}, Weight: {5}, Delivered With: {6},'
                ' Truck: {7}, At Hub By: {8}, Deadline: {9}, Delivery Status: {10}, '
                'En Route Time: {11}, Time Delivered: {12}, Delivery Truck: {13}').format(self.package_id, self.address,
                                                                                          self.city,
                                                                                          self.zip_code, self.state,
                                                                                          self.weight,
                                                                                          self.delivered_with,
                                                                                          self.truck_number,
                                                                                          self.at_hub_time,
                                                                                          self.delivery_deadline,
                                                                                          self.delivery_status,
                                                                                          self.en_route_time,
                                                                                          self.time_delivered,
                                                                                          self.delivery_truck)

    # Ensures the hash is on the package's id and not any other variable, so it it always put into the same bucket
    def __hash__(self):
        return int(self.package_id)

    # Checks whether the package is either being delivered or being added to a truck
    # and assigns what time it is happening
    def update_status(self, status, time):
        if status == 'Delivered':
            self.time_delivered = time
        elif status == 'En Route':
            self.en_route_time = time
