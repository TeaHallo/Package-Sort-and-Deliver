from operator import attrgetter
from Truck import Truck


class ChainingHashTable:

    def __init__(self, initial_capacity=20):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, package):
        bucket = hash(package) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append(package)

    def search(self, package_id):
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]

        for package in bucket_list:
            if package_id == hash(package):
                return package

    # The parameters of this algorithm are the hash table of packages, Truck 1 and Truck 2. The packages are inserted
    # into a list so that I can iterate through them easily. I first look to see if any packages need to be delivered
    # with other packages. I then turn this list into a set so that any duplicates are removed. Then I insert
    # all of these packages into a list together, and put any other packages into a separate list.
    # After this, I take the list of packages that need to be delivered together and see if they can be added to
    # any trucks yet based on the time they will be at the hub. If any of them are not at the hub by 8, I can't
    # deliver any of them yet and will refrain from loading them.
    # If they all can be loaded, I check to see if any of them need to be on Truck 2, and if not, I add them to Truck 1.
    # After this, I check the at hub time for all other packages, and if they can be loaded, I load them, also based
    # on if they need to be on a certain truck or not.
    # Since each truck can only hold 16 packages, I then slice the list of each truck to 16 and put the rest of
    # the packages into a list of ones that are left over.
    # Then I load each truck with its own package list
    # After all algorithms are finished, the second sorting algorithm is called for the leftover packages
    def sort_packages(self, truck1, truck2):
        packages = []
        other_packages = []
        truck1_packages = []
        truck2_packages = []
        together_packages = []
        leftover_packages = []
        ids = []

        for i in range(1, 41):
            p = self.search(i)
            packages.append(p)

        for package in packages:
            if len(package.delivered_with) > 1:
                package_list = package.delivered_with
                ids.append(package_list[0])
                ids.append(package_list[1])
                ids.append(package.package_id)

        set_ids = set(ids)
        for package in packages:
            if package.package_id in set_ids:
                together_packages.append(package)

        for package in packages:
            if package not in together_packages:
                other_packages.append(package)

        can_deliver = []
        for package in together_packages:
            if package.at_hub_time == '08:00':
                can_deliver.append(package)
        if len(can_deliver) == len(together_packages):
            for p in can_deliver:
                if p.truck_number:
                    if p.truck_number == '2':
                        truck2_packages.append(p)
                else:
                    truck1_packages.append(p)
        else:
            leftover_packages = together_packages

        other_packages.sort(key=attrgetter('delivery_deadline', 'at_hub_time'))

        for package in other_packages:
            if package.at_hub_time == '08:00':
                if package.truck_number:
                    if package.truck_number == '2':
                        truck2_packages.append(package)
                else:
                    truck1_packages.append(package)
            else:
                leftover_packages.append(package)

        if len(truck1_packages) > Truck.MAX_PACKAGES:
            temp1 = truck1_packages[0:16]
            temp2 = truck1_packages[16:]
            truck1_packages = temp1
            for t in temp2:
                truck2_packages.append(t)

        if len(truck2_packages) > Truck.MAX_PACKAGES:
            temp1 = truck2_packages[0:16]
            temp2 = truck2_packages[16:]
            truck2_packages = temp1
            for t in temp2:
                leftover_packages.append(t)

        truck1_packages.sort(key=attrgetter('delivery_deadline'))
        truck2_packages.sort(key=attrgetter('delivery_deadline'))

        truck1.load_truck(truck1_packages)
        truck2.load_truck(truck2_packages)
        self.sort_other_packages(leftover_packages, truck1, truck2)

    # This algorithm takes the leftover packages that weren't delivered with the first load as a parameter, along with
    # the two trucks that have returned to the hub.
    # It compares the current time of truck 1 with the time that each package needs to be delivered to make sure
    # the truck is back at the hub in time to load and deliver it, and if it isn't, it is loaded onto the second truck
    # Then, to prevent the packages that need to be delivered earlier from having to wait for the packages
    # that don't get to the hub until later, the packages are separated by deadline onto the trucks for delivery.
    # The trucks are then loaded with each of its corresponding lists
    def sort_other_packages(self, packages, truck1, truck2):
        truck1_packages = []
        truck2_packages = []
        together_packages = []
        other_packages = []
        ids = []

        for package in packages:
            if len(package.delivered_with) > 1:
                package_list = package.delivered_with
                ids.append(package_list[0])
                ids.append(package_list[1])
                ids.append(package.package_id)

        set_ids = set(ids)
        for package in packages:
            if package.package_id in set_ids:
                together_packages.append(package)

        for package in packages:
            if package not in together_packages:
                other_packages.append(package)

        for package in together_packages:
            if package.truck_number == '2':
                truck2_packages.append(package)
            else:
                truck1_time = str(truck1.current_time).split(':')
                truck1_hours = int(truck1_time[0])
                truck1_mins = int(truck1_time[1])
                package_deadline = str(package.delivery_deadline).split(':')
                package_deadline_hours = int(package_deadline[0])
                package_deadline_mins = int(package_deadline[1])
                if truck1_hours < package_deadline_hours:
                    truck1_packages.append(package)
                elif truck1_hours == package_deadline_hours:
                    if truck1_mins < package_deadline_mins or truck1_mins == package_deadline_mins:
                        truck1_packages.append(package)
                else:
                    truck2_packages.append(package)

        packages.sort(key=attrgetter('delivery_deadline', 'at_hub_time'))

        for package in other_packages:
            if package.truck_number == '2':
                truck2_packages.append(package)
            else:
                truck1_time = str(truck1.current_time).split(':')
                truck1_hours = int(truck1_time[0])
                truck1_mins = int(truck1_time[1])
                package_deadline = str(package.delivery_deadline).split(':')
                package_deadline_hours = int(package_deadline[0])
                package_deadline_mins = int(package_deadline[1])
                if truck1_hours < package_deadline_hours:
                    truck1_packages.append(package)
                elif truck1_hours == package_deadline_hours:
                    if truck1_mins < package_deadline_mins or truck1_mins == package_deadline_mins:
                        truck1_packages.append(package)
                else:
                    truck2_packages.append(package)

        truck1_packages.sort(key=attrgetter('delivery_deadline'))
        for package in truck1_packages:
            if package.delivery_deadline == '17:00':
                truck2_packages.append(package)
                truck1_packages.remove(package)

        truck1.load_truck(truck1_packages)
        truck2.load_truck(truck2_packages)

    # This algorithm takes a time as the parameter to see the status of each package at that time.
    # It basically compares the delivery time of the package to the input time and if the delivery time is later,
    # it then compares the en route time to the input time. If the en route time is later, then the package is displayed
    # as still being at the hub.
    def display_packages(self, time):
        # time must be in military, or comparison won't work
        time_string = str(time).split(':')
        time_hours = int(time_string[0])
        time_mins = int(time_string[1])

        delivered_packages = []
        en_route_packages = []
        at_hub_packages = []
        packages = []

        for i in range(1, 41):
            p = self.search(i)
            packages.append(p)

        for package in packages:
            if package.time_delivered:
                string = str(package.time_delivered).split(':')
                hours = int(string[0])
                minutes = int(string[1])

                if time_hours > hours:
                    package.delivery_status = 'Delivered'
                    delivered_packages.append(package)
                elif time_hours == hours:
                    if time_mins > minutes or time_mins == minutes:
                        package.delivery_status = 'Delivered'
                        delivered_packages.append(package)

        for package in packages:
            if package not in delivered_packages:
                string = str(package.en_route_time).split(':')
                hours = int(string[0])
                minutes = int(string[1])

                if time_hours > hours:
                    package.delivery_status = 'En Route'
                    en_route_packages.append(package)
                elif time_hours == hours:
                    if time_mins > minutes or time_mins == minutes:
                        package.delivery_status = 'En Route'
                        en_route_packages.append(package)

        for package in packages:
            if package not in delivered_packages and package not in en_route_packages:
                package.delivery_status = 'At Hub'
                at_hub_packages.append(package)

        print('Delivered Packages:')
        for package in delivered_packages:
            print('ID:{0}, Address: {1}, City: {2}, State: {3}, Zip Code: {4}, Weight: {5}, Deadline: {6},'
                  ' Status: Delivered, Delivery Time: {7}, Delivery Truck: {8}, At Hub Time: {9}, En Route Time: {10}'
                  .format(package.package_id,
                          package.address, package.city,
                          package.state, package.zip_code,
                          package.weight,
                          package.delivery_deadline,
                          package.time_delivered,
                          package.delivery_truck,
                          package.at_hub_time, package.en_route_time))

        print('En Route:')
        for package in en_route_packages:
            print('ID:{0}, Address: {1}, City: {2}, State: {3}, Zip Code: {4}, Weight: {5}, Deadline: {6},'
                  ' Status: En Route, En Route Time: {7}'.format(package.package_id, package.address, package.city,
                                                                 package.state, package.zip_code, package.weight,
                                                                 package.delivery_deadline, package.en_route_time))

        print('At Hub:')
        for package in at_hub_packages:
            print('ID:{0}, Address: {1}, City: {2}, State: {3}, Zip Code: {4}, Weight: {5}, Deadline: {6},'
                  ' Status: At Hub'.format(package.package_id, package.address, package.city, package.state,
                                           package.zip_code, package.weight, package.delivery_deadline))

    # This displays the total mileage traveled by both trucks after all packages are delivered and have returned
    # to the hub
    def display_total_mileage(self):
        print('Total Distance Traveled: {0}'.format(round(Truck.total_distance_traveled, 2)))
