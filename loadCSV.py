import pandas as pd
from HashTable import HashTable
from Package import Package

# instantiate Hash Table:
WGUPS = HashTable()

# creating pacackage objects and assigning them to the hash table from CSV file:


def load_HashTable(filepath):

    df = pd.read_csv(filepath, header=4)
    df = df.fillna('None')
    df['Status'] = 'At hub'
    df['Loaded'] = ''
    df['Delivered'] = ''
    df['Truck ID'] = ''
    df['Driver ID'] = ''
    for index, row in df.iterrows():
        pkgID = row['PackageID']

        newPackage = Package(
            ID=pkgID,
            Address=row['Address'],
            City=row['City'],
            State=row['State'],
            ZipCode=row['Zip'],
            Deadline=row['Delivery Deadline'],
            Weight=row['Weight KILO'],
            Notes=row['Notes'],
            Status=row['Status'],
            LoadTime=row['Loaded'],
            DeliveryTime=row['Delivered'],
            TruckID=row['Truck ID'],
            DriverID=row['Driver ID']
        )
        WGUPS[pkgID] = newPackage

    print(f'file path: {filepath} has been loaded successfully!')

# this function loads 27x27 matrix of float points between addresses


def load_distance_data(filepath):
    df = pd.read_csv(filepath, header=None)
    return df.to_numpy()

# this function loads CSV string address. Needed for future dictionary use for the string address index.


def load_address(filepath):
    df = pd.read_csv(filepath, header=None)

    return df.to_numpy().flatten()

# Function for finding the highest frequency of zip codes:


def zip_freq(filepath):

    df = pd.read_csv(filepath, header=4)
    df = df.fillna('None')
    group = df.groupby('Zip')
    print(group['Zip'].count().sort_values(ascending=False))
