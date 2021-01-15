import csv
import os

class CarBase:
    """
        base class for all transport vehicles
    """

    # params for class
    required = []

    def __init__(self, brand, photo_file_name, carrying):
        # self.car_type = str(car_type)
        self.brand = self.validate_input(brand)
        self.photo_file_name = self.validate_photo_filename(photo_file_name)
        self.carrying = float(self.validate_input(carrying))
    
    def validate_input(self, value):
        if value == '':
            raise ValueError
        return value

    def validate_photo_filename(self, photo_filename):
        for ext in ('.jpg', '.jpeg', '.png', '.gif'):
            if photo_filename.endswith(ext) and len(photo_filename) > len(ext):
                return photo_filename
        raise ValueError

    def get_photo_file_ext(self):
        _, ext = os.path.splitext(self.photo_file_name)
        return ext

    @classmethod
    def create_from_dict(cls, data):
        """
            create an instance of the class from dict with parametres
        """
        parametres = [data[param] for param in cls.required]
        return cls(*parametres)

class Car(CarBase):

    car_type = "car"
    required = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(
            brand=brand, 
            photo_file_name=photo_file_name,
            carrying=carrying)
        self.passenger_seats_count = int(self.validate_input(passenger_seats_count))
        

class Truck(CarBase):

    car_type = "truck"
    required = ['brand', 'photo_file_name', 'carrying', 'body_whl']

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(
            brand=brand, 
            photo_file_name=photo_file_name,
            carrying=carrying)

        self.body_length, self.body_width, self.body_height = self.parse_whl(body_whl)

    def parse_whl(self, body_whl):
        try:
            length, width, heigth = (float(num) for num in body_whl.split('x', 2))
        except:
            length, width, heigth = 0.0, 0.0, 0.0
        return length, width, heigth

    def get_body_volume(self) -> float:
        return float(self.body_length) * float(self.body_width) * float(self.body_height)

class SpecMachine(CarBase):

    car_type = "spec_machine"
    required = ['brand', 'photo_file_name', 'carrying', 'extra']

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(
            brand=brand, 
            photo_file_name=photo_file_name,
            carrying=carrying)
        self.extra = self.validate_input(extra)

def get_car_list(csv_filename):
    
    car_types = {'car': Car, 'spec_machine': SpecMachine, 'truck': Truck}
    cars = []
    csv.register_dialect('cars', delimiter=';')

    try:
        with open(csv_filename, 'r') as csv_fd:
            reader = csv.DictReader(csv_fd, dialect='cars')
            # next(reader)
            for row in reader:
                try:
                    car_class = car_types[row['car_type']]
                    cars.append(car_class.create_from_dict(row))
                except Exception:
                    pass
    except IOError:
        pass

    return cars
