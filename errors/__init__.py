class StartDateFormatException(Exception):
    def __str__(self):
        return "Wrong start date format.\n"
class EndDateFormatException(Exception):
    def __str__(self):
        return "Wrong end date format.\n"   
class LocationNotFoundException(Exception):
    def __str__(self):
        return "Location not found.\n"
