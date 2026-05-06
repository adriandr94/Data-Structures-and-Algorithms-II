
class Package:

    def __init__(self, ID, Address, City, State, ZipCode, Deadline, Weight, Notes, Status, LoadTime, DeliveryTime, TruckID, DriverID):
        self.ID = ID
        self.Address = Address
        self.City = City
        self.State = State
        self.ZipCode = ZipCode
        self.Deadline = Deadline
        self.Weight = Weight
        self.Notes = Notes
        self.Status = Status
        self.LoadTime = LoadTime
        self.DeliveryTime = DeliveryTime
        self.TruckID = TruckID
        self.DriverID = DriverID

    def __str__(self):
        return (f"Package ID: {self.ID}, Status: {self.Status}, Loaded: {self.LoadTime}, Delivered: {self.DeliveryTime}, \n Address: {self.Address}, City: {self.City}, State: {self.State}, Zip: {self.ZipCode}, \nDeadline: {self.Deadline}, Weight(kg): {self.Weight}, Notes: {self.Notes}")
