import psycopg2


def create_tables():
    commands = (
        """ 
        CREATE TABLE taxis (
            id INTEGER PRIMARY KEY,
            passenger_name VARCHAR(100),
            destination VARCHAR(100)
        )
        """,
        """ 
        INSERT INTO taxis (id, passenger_name, destination) VALUES (1, 'John Doe', 'Airport')
        """,
        """ 
        INSERT INTO taxis (id, passenger_name, destination) VALUES (2, 'Jane Smith', 'Hotel')
        """,
        """ 
        INSERT INTO taxis (id, passenger_name, destination) VALUES (3, 'Bob Johnson', 'Restaurant')
        """
    )
       
    conn = psycopg2.connect(
        port=5432,
        host="localhost",
        database="taxi",
        user="postgres",
        password="aziz"
    )
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

create_tables()

class InvalidTaxiName(Exception):
    pass

class Taxi:
    def __init__(self, id):
        self.id = id
        self.passenger = None
        self.trips = []

    def __str__(self):
        return f"Taxi {self.id}"

    def beginTrip(self, destination):
        if self.passenger is not None:
            raise Exception("A passenger is already assigned to this taxi.")
        trip = Trip(self.passenger.getPlace(), destination)
        self.trips.append(trip)
        self.passenger = None

    def terminateTrip(self):
        if self.passenger is None:
            raise Exception("No passenger is currently assigned to this taxi.")
        self.passenger = None

class TaxiCompany:
    def __init__(self):
        self.taxis = []

    def addTaxi(self, taxi):
        if any(t.id == taxi.id for t in self.taxis):
            raise InvalidTaxiName(f"A taxi with ID {taxi.id} already exists.")
        self.taxis.append(taxi)

    def getAvailable(self):
        return [taxi for taxi in self.taxis if taxi.passenger is None]

    def getTrips(self, taxi_id):
        for taxi in self.taxis:
            if taxi.id == taxi_id:
                return taxi.trips
        raise InvalidTaxiName(f"No taxi found with ID {taxi_id}.")

class Passenger:
    def __init__(self, place):
        self.place = place

    def getPlace(self):
        return self.place

class Place:
    def __init__(self, address, district, neighborhood):
        self.address = address
        self.district = district
        self.neighborhood = neighborhood

    def __str__(self):
        return f"{self.address}, {self.district}, {self.neighborhood}"

class Trip:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start}, {self.end}"

    def getEnd(self):
        return self.end

taxiCompany = TaxiCompany()

place = Place("123 Main St", "District A", "Neighborhood B")
passenger = Passenger(place)
taxi1 = Taxi(1)

taxiCompany.addTaxi(taxi1)