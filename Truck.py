
class Truck:
    total_distance_traveled = 0
    TRUCK_SPEED = 18
    MAX_PACKAGES = 16
    address_dict = {}
    distance_matrix = []

    def __init__(self, number):
        self.number = number
        self.packages_list = []
        self.current_time = '08:00'
        self.travel_distance = None

    # This algorithm takes the truck's current time, adds the time it took to deliver the package and returns the
    # truck's new time
    def change_time(self, minutes_passed):
        string = str(self.current_time).split(':')
        current_time_hours = int(string[0])
        current_time_mins = int(string[1])

        hours = minutes_passed // 60
        minutes = minutes_passed % 60
        total_hours = current_time_hours + hours
        if total_hours > 12:
            total_hours -= 12
        total_mins = current_time_mins + minutes
        if total_mins >59:
            total_hours += 1
            total_mins -= 60
        if total_mins == 0:
            total_mins = str(total_mins) + '0'
        elif total_mins < 10:
            total_mins = '0' + str(total_mins)
        new_time = str(total_hours) + ':' + str(total_mins)

        self.current_time = new_time
        return new_time

    # This takes the package list and assigns it to the truck's list of packages. It then assigns the time it was loaded
    # and calls the algorithm to sort and deliver the packages
    def load_truck(self, packages):
        self.packages_list = packages
        for package in self.packages_list:
            package.update_status('En Route', self.current_time)
        self.find_closest_distance(packages)

    # This algorithm finds the package in the truck's list of packages that has the shortest distance from the current
    # address. It starts at the hub, i=0, and after that package is delivered, it updates i with the id of the delivered
    # package and finds the next address closest to that one.
    # It calculates the amount of time passed with the delivery, changes the truck's time, and updates the total
    # distance traveled by both trucks. It also assigns each packaged with its delivered time and
    # the truck that delivered it. After each package is delivered, it is removed from the truck's package list.
    # If the package list of the truck is not empty after the current iteration, the function calls itself again.
    # If the package list of the truck is empty, the truck is returned to the hub.
    def find_closest_distance(self, truck_package_list, i=0):
        pack = truck_package_list[0]
        a = pack.address
        num = Truck.address_dict[a]
        minimum = float(Truck.distance_matrix[i][num])
        for package in truck_package_list:
            address = package.address
            num = Truck.address_dict[address]
            distance = float(Truck.distance_matrix[i][num])
            if float(distance) < float(minimum):
                minimum = distance
                pack = package

        miles_per_minute = Truck.TRUCK_SPEED / 60
        minutes_passed = int(minimum / miles_per_minute)
        new_time = self.change_time(minutes_passed)
        Truck.total_distance_traveled = minimum + float(Truck.total_distance_traveled)
        pack.update_status('Delivered', new_time)
        pack.delivery_truck = self.number
        self.packages_list.remove(pack)
        if len(self.packages_list) != 0:
            address2 = pack.address
            new_index = int(Truck.address_dict[address2])
            packages = self.packages_list
            return self.find_closest_distance(packages, new_index)
        else:
            current_address = pack.address
            index = int(Truck.address_dict[current_address])
            distance_to_hub = float(Truck.distance_matrix[index][0])
            miles_per_minute = Truck.TRUCK_SPEED / 60
            minutes_passed = int(distance_to_hub / miles_per_minute)
            self.change_time(minutes_passed)
            Truck.total_distance_traveled = distance_to_hub + float(Truck.total_distance_traveled)





