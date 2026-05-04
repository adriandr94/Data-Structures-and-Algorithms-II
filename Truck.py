from HashTable import HashTable
# Truck class is defined and used to instantiate objects that will transport the "Package" objects
from loadCSV import WGUPS
from datetime import datetime

current_time = datetime.strptime


class Truck:
    def __init__(self, truckID, driver, mileage):
        self.truckID = truckID
        self.driver = driver
        self.mileage = mileage
        self.capacity = []

# load function that gives the option for loading the truck after instantiating a truck object.
    def load(self, pkgIDs, enterTime):
        self.base_time = datetime.strptime(enterTime, "%H:%M")
        for pkgID in pkgIDs:
            self.capacity.append(WGUPS[pkgID])
            WGUPS[pkgID].LoadTime = self.base_time.strftime("%I:%M %p")
            WGUPS[pkgID].Status = "In Transit"

    def __str__(self):
        ppackages = [pkg.ID for pkg in self.capacity]
        return (f"Truck Number: {self.truckID}, Driver: {self.driver}, Package IDs Remaining: {ppackages}, Mileage: {self.mileage}")
