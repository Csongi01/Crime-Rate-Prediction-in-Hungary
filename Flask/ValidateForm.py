class CrimeFormValidator:
    def __init__(self, year, city_code, crime):
        self.year = year
        self.city_code = city_code
        self.crime = crime
        self.errors = {}

    def validate_year(self):
        if not self.year:
            self.errors['year'] = "Please enter a year!"

    def validate_city(self):
        if not self.city_code:
            self.errors['city'] = "Please enter a city!"

    def validate_crime(self):
        if not self.crime:
            self.errors['crime'] = "Please select a crime type!"

    def validate(self):
        # Run all the validations
        self.validate_year()
        self.validate_city()
        self.validate_crime()
        return self.errors
