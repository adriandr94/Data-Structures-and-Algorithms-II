# Adrian Reyes
# Student ID: 010555271
# WGU (Computer Science)
# Data Structures and Algorithms II
# 04/28/26

# Making a function that sorts the zipcode from highest frequency to lowest
# updating highest/max
from loadCSV import load_HashTable, load_distance_data, load_address
from loadCSV import WGUPS
from Truck import Truck
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

# Load CSV files using these three loading functions. They are found in loadCSV.py:

# This load_HashTable() function load in CSV files that have package data such as:
# package ID, Address, City, State, Zip, Weight, Deadline, and Notes:
load_HashTable("CSV files/WGUPS Package File.csv")
# The load_distance_data() function loads CSV files that are formatted into a adjancy matrix-like chart of distance float values:
distance_data = load_distance_data('CSV files\WGUPS Distance Table.csv')
# the load_address() function loads CSV files that have just the string addresses
address_data = load_address('CSV files\Addresses.csv')

# Instantiation all 3 trucks.
truck1 = Truck(truckID=1, driver=1, mileage=0)
truck2 = Truck(truckID=2, driver=2, mileage=0)
truck3 = Truck(truckID=3, driver=None, mileage=0)

# The address string will be the key entered. This is done to find the index position of each package.


def address_maping(addresses):
    addressIndexMap = {}
    for index, address in enumerate(addresses):
        addressIndexMap[address] = index
    return addressIndexMap

# function for finding distance between 2 indexes
# Making row as max and column as min makes it so that the values 'NaN' are never used.


def get_distance(index1, index2, ListOfLists):
    row = max(index1, index2)
    column = min(index1, index2)
    distance = ListOfLists[row][column]
    return distance


# instantiating address dictionary with string address as key and index as value:
address_dictionary = address_maping(address_data)


# updating status of packages not arriving to hub until 9:05. Easily done using the Hash Table:
for pkg in [6, 25, 28, 32]:
    WGUPS[pkg].Status = 'DELAYED'

# Note all trucks have to be manually loaded by entering just the package ID numbers as shown below:
# Truck 1 loaded
truck1.load([1, 4, 8, 13, 14, 15, 16, 19, 20,
            21, 29, 30, 31, 34, 37, 40], "08:00")

# Again, we can update the status for packages that arrived after truck 1 finished.
for pkg in [6, 25, 28, 32]:
    WGUPS[pkg].Status = 'Arrived at Hub at 9:05 AM'

truck2.load([3, 6, 12, 17, 18, 25, 26, 28, 32, 36, 38, 27, 35, 39], "09:15")

# Driver 1 from truck1 changes to truck3
truck3.driver = 1

# Address changed for package ID 9. Easily changed using the Hash Table:
WGUPS[9].Address = '410 S State St'
WGUPS[9].ZipCode = '84111'

truck3.load([2, 5, 7, 9, 10, 11, 22, 23, 24, 33], "10:25")
combined_truck_mileage = 0

# Process and flow of program: CSV files are loaded using functions in loadCSV.py and instantiated in main.py
# hash table is also loaded from main.py and new package objects made with Package.py defining its class and values are stored in the hash table
# functions in main.py are used to extract and organize data from 3 CSV files for later algorithm use
# truck class objects are instantiated in main.py with a load function defined in Truck.py
# a separate dictionary is used to map string addresses as keys and index positions as value
# trucks are manually loaded utilizing the .load() function and get/look up function from the hash table
# the truck's capacity list is iterate through to match the hash table's package's addresses with the separate dictionary to match an index
# each index found is then appended to a list for the delivery algorithm to use to find the minimum distance float value.
# the main delivery algorithm uses nearest-neighbor idea to delivery packages by finding the minimum value from each location that is undelivered.
# after delivery, the algorithm updates each respective package's delivery time and status.
# another algorithm is made to handle the statuses of each package based on a specific time a user inputs.


def delivery(truck):
    current_location = 0
    total_mileage = 0
    current_time = truck.base_time
    undelivered = []
    for pkg in truck.capacity:
        undelivered.append(address_dictionary[pkg.Address])
    while len(undelivered) > 0:
        float_points = []
        for index in undelivered:
            float_points.append(get_distance(
                current_location, index, distance_data))

    # finding min distance of list using min method:
        min_distance = min(float_points)
        matching_index = float_points.index(min_distance)

        travel_time = (min_distance/18.0)*60.00
        travel_delta = timedelta(minutes=travel_time)
        current_time += travel_delta
    # Update total mileage and current location
        total_mileage += min_distance
        current_location = undelivered[matching_index]

    # Pop the package at that specific position
        undelivered.pop(matching_index)

    # We can pop the actual truck packages from the capacity list,
    # making them physically "delivered" as well since their indexes match
    # the indexes of float_points list (distance locations)
        truck.capacity[matching_index].DeliveryTime = current_time.strftime(
            "%I:%M %p")
        truck.capacity[matching_index].Status = "Delivered"
        truck.capacity.pop(matching_index)

    # now to update current location back to 0 and add that mileage into total_mileage
    back_to_hub = get_distance(current_location, 0, distance_data)
    min_distance = back_to_hub
    total_mileage += min_distance
    truck.mileage = total_mileage


delivery(truck1)
delivery(truck2)
delivery(truck3)

# to check if all orders with deadlines made it in time:
# for i, value in WGUPS.items():
#     if value.Deadline != "EOD":
#         print(value)

# function to check status of all packages at any given time:


def print_status_time(userTime):

    inputTime = datetime.strptime(userTime, "%I:%M %p")
    # needed to create another list and change return values to appending to status_list just to
    # print into the GUI using scrolltext widget.
    status_list = []
    for index, value in WGUPS.items():
        # program crashes when parsing packages without a load/delivery time:

        if not value.LoadTime or not value.DeliveryTime:
            status_list.append(
                f"Package: {index}, Status: Pending {inputTime.strftime("%I:%M %p")}")
            continue
        pkgLoaded = datetime.strptime(value.LoadTime, "%I:%M %p")
        pkgDelivered = datetime.strptime(value.DeliveryTime, "%I:%M %p")
        if inputTime < pkgLoaded:
            status_list.append(
                f"Package: {index}, Truck ID: In Preparation, Driver ID: In Preparation, Address: {value.Address}, {value.City}, {value.State}, {value.ZipCode}, Deadline: {value.Deadline}, Status: At Hub -- {inputTime.strftime("%I:%M %p")} -- \n" + "----------------------------------------------------------------------------------------------------------------")
        elif inputTime < pkgDelivered:
            status_list.append(
                f"Package: {index}, Truck ID: {value.TruckID}, Driver ID: {value.DriverID}, Address: {value.Address}, {value.City}, {value.State}, {value.ZipCode}, Deadline: {value.Deadline}, Status: In Transit -- {value.LoadTime} --\n" + "----------------------------------------------------------------------------------------------------------------")
        else:
            status_list.append(
                f"Package: {index}, Truck ID: {value.TruckID}, Driver ID: {value.DriverID}, Address: {value.Address}, {value.City}, {value.State}, {value.ZipCode}, Deadline: {value.Deadline}, Status: Delivered at -- {value.DeliveryTime} --\n" + "----------------------------------------------------------------------------------------------------------------")
    return "\n".join(status_list)


# -------------User Interface-----------------------------------------------------
window = Tk()
window.geometry("500x600")
window.title("WGUPS Tracking Application")


notebook = ttk.Notebook(window)

tab1 = Frame(notebook, background="#3F404B")
tab2 = Frame(notebook, background="#3F404B")
tab3 = Frame(notebook, background="#3F404B")

style = ttk.Style()
# 'default' or 'clam' allow for better color customization
style.theme_use('default')

# Configure the background and text color of the Tab bar area
style.configure("TNotebook", background="#3F404B", borderwidth=0)

# Configure the appearance of the Tabs themselves
style.configure("TNotebook.Tab",
                background="#4169A5",
                foreground="#FFFFFF",
                lightcolor="#3F404B",
                borderwidth=1)

# Configure what the tab looks like when it is selected
style.map("TNotebook.Tab",
          background=[("selected", "#3F404B")],
          foreground=[("selected", "#FFFFFF")])

notebook.add(tab1, text="Tracking")
notebook.add(tab2, text="EOD Log")
notebook.add(tab3, text="Status Check")
notebook.pack(expand=True, fill='both')
icon = PhotoImage(file='images\icons8-fast-delivery-32.png')
window.iconphoto(True, icon)
window.config(background="#3F404B")
# Tab 1 window code below:
label = Label(tab1, text="WGUPS Tracking", font=(
    'Arial', 32, 'bold'), fg="#8DADDD", background="#3F404B")
label.grid(row=0, column=0, columnspan=3)

output_label = StringVar()


def click():
    output_txt = ""
    usrPkgID = int(entry.get())
    output_label.set(WGUPS[usrPkgID])


packagetxt = Label(tab1, text='Package ID: ', font=('bold'),
                   background="#3F404B", fg="#FFFFFF").grid(row=1, column=0)

track_btn = Button(tab1, text='Track Package', command=click)
track_btn.config(font=('Arial'), fg="#FFFFFF",
                 background="#4169A5", activebackground="#4169A5")
track_btn.grid(row=1, column=2)

entry = Entry(tab1)
entry.config(font=('Arial'), background="#757575", fg="#FFFFFF")
entry.grid(row=1, column=1)

label2 = Label(tab1, textvariable=output_label,
               background="#757575", fg="#FFFFFF", width=60, height=3)
label2.grid(row=2, column=0, columnspan=3)


# Tab 2 window code below:
label3 = Label(tab2, text="End of Day Log", font=(
    'Arial', 20, 'bold'), fg="#8DADDD", background="#3F404B")
label3.grid(row=0, column=0)

output_label2 = StringVar()


def LoadLog():

    output_txt3 = ""
    truck1_details = str(truck1)
    truck2_details = str(truck2)
    truck3_details = str(truck3)

    truck1_mileage = float(truck1.mileage)
    truck2_mileage = float(truck2.mileage)
    truck3_mileage = float(truck3.mileage)
    total_mileage = float(truck1.mileage + truck2.mileage + truck3.mileage)
    output_label2.set(
        f'{truck1} \n {truck2} \n {truck3} \n Total Truck Mileage Combined: {total_mileage: .2f}')
# Truck 1 total mileage:{truck1_mileage} \n Truck 2 total mileage:{truck2_mileage} \n Truck 3 total mileage:{truck3_mileage} \n
    output_txt2 = ""
    for index, value in WGUPS.items():
        output_txt2 += str(value) + "\n" + \
            "-------------------------------------------------------------------------------------------------------------" + "\n"
    label4.config(state='normal')
    label4.delete('1.0', 'end')
    label4.insert('1.0', output_txt2)
    label4.config(state='disabled', background="#757575", fg="#FFFFFF")


LoadLog_btn = Button(tab2, text='Load Log', command=LoadLog)
LoadLog_btn.config(font=('Arial'), fg="#FFFFFF",
                   background="#4169A5", activebackground="#4169A5")
LoadLog_btn.grid(row=1, column=0)

label4 = scrolledtext.ScrolledText(
    tab2, width=65, height=20, font=('Arial', 10), background="#757575", fg="#FFFFFF")
label4.grid(row=3, column=0)
label4.config(state='disabled')

label5 = Label(tab2, textvariable=output_label2,
               width=60, height=5, font=('Arial', 10), background="#757575", fg="#FFFFFF")
label5.grid(row=2, column=0)

# tab 3 code below:

label6 = Label(tab3, text="Package Status", font=(
    'Arial', 20, 'bold'), fg="#8DADDD", background="#3F404B")
label6.grid(row=0, column=0, columnspan=4, pady=10)

time_txt = Label(tab3, text='Enter Time: HH:MM AM/PM ',
                 font=('bold'),
                 background="#3F404B", fg="#FFFFFF").grid(row=1, column=0, sticky="e")

entry2 = Entry(tab3)
entry2.config(font=('Arial'), width=10, background="#757575", fg="#FFFFFF")
entry2.grid(row=1, column=1)

output_label3 = StringVar()


def click2():
    try:
        usr_entry = print_status_time(str(entry2.get()))
        label7.config(state='normal')
        label7.delete('1.0', 'end')
        label7.insert('1.0', usr_entry)
        label7.config(state='disabled')
    except ValueError:
        label7.config(state='normal')
        label7.insert(
            'end', "Error: Use 'HH:MM AM/PM' format. \n Be sure there is a space between the time and AM/PM \n")
        label7.config(state='disabled')


status_btn = Button(tab3, text='Status Check', command=click2)
status_btn.config(font=('Arial'), fg="#FFFFFF",
                  background="#4169A5", activebackground="#4169A5")
status_btn.grid(row=1, column=3)

label7 = scrolledtext.ScrolledText(
    tab3, width=67, height=30, font=('Arial', 10), background="#757575", fg="#FFFFFF")
label7.grid(row=3, column=0, columnspan=4)
label7.config(state='disabled')

window.mainloop()
