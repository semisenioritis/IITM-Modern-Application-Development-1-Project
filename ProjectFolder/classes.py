from datetime import datetime

class Venue:
    def __init__(self, name, capacity, rating, address, photo, description):
        self.name = name
        self.rating = rating
        self.address = address
        self.capacity = capacity
        self.photo = photo
        self.description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # if not isinstance(value, str):
        #     raise TypeError("Name must be a string")
        self._name = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        # if not isinstance(value, int):
        #     raise TypeError("Rating must be an integer")
        self._rating = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        # if not isinstance(value, str):
        #     raise TypeError("Address must be a string")
        self._address = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        # if not isinstance(value, int):
        #     raise TypeError("Capacity must be an integer")
        self._capacity = value

    @property
    def photo(self):
        return self._photo

    @photo.setter
    def photo(self, value):
        # if not isinstance(value, int):
        #     raise TypeError("Capacity must be an integer")
        self._photo = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # if not isinstance(value, int):
        #     raise TypeError("Capacity must be an integer")
        self._description = value

class Movie:
    def __init__(self, name, genre, rating, tags, languages, price):
        self.name = name
        self.genre = genre
        self.rating = rating
        self.tags = tags
        self.languages = languages
        self.price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # if not isinstance(value, str):
        #     raise TypeError("Name must be a string")
        self._name = value


    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        # if not isinstance(value, str):
        #     raise TypeError("Name must be a string")
        self._genre = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        # if not isinstance(value, float):
        #     raise TypeError("Rating must be a float")
        # if value > 10.0:
        #     raise ValueError("Rating must be less than or equal to 10.0")
        self._rating = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        # if not isinstance(value, float):
        #     raise TypeError("Our Rating must be a float")
        # if value > 10.0:
        #     raise ValueError("Rating must be less than or equal to 10.0")
        self._tags = value

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, value):
        # if not isinstance(value, str):
        #     raise TypeError("Languages must be a string")
        self._languages = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        # if not isinstance(value, float):
        #     raise TypeError("Price must be a float")
        self._price = value



class Screening:
    def __init__(self, venue, movie, date, time, number_of_seats_left):
        self.venue = venue
        self.movie = movie
        self.date = date
        self.time = time
        self.number_of_seats_left = number_of_seats_left

    @property
    def venue(self):
        return self._venue

    @venue.setter
    def venue(self, value):
        # if not isinstance(value, Venue):
        #     raise TypeError("Venue must be an instance of Venue")
        self._venue = value

    @property
    def movie(self):
        return self._movie

    @movie.setter
    def movie(self, value):
        # if not isinstance(value, Movie):
        #     raise TypeError("Movie must be an instance of Movie")
        self._movie = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        # if not isinstance(value, datetime):
        #     raise TypeError("Datetime must be a datetime object")
        self._date = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        # if not isinstance(value, datetime):
        #     raise TypeError("Datetime must be a datetime object")
        self._time = value


    @property
    def number_of_seats_left(self):
        return self._number_of_seats_left

    @number_of_seats_left.setter
    def number_of_seats_left(self, value):
        # if not isinstance(value, int):
        #     raise TypeError("Number of seats left must be an integer")
        self._number_of_seats_left = value

class Booking:
    def __init__(self, user_index, show_index, no_of_tickets, total_price):
        self._user_index = user_index
        self._show_index = show_index
        self._no_of_tickets = no_of_tickets
        self._total_price = total_price

    @property
    def user_index(self):
        return self._user_index

    @user_index.setter
    def user_index(self, value):
        self._user_index = value

    @property
    def show_index(self):
        return self._show_index

    @show_index.setter
    def show_index(self, value):
        self._show_index = value

    @property
    def no_of_tickets(self):
        return self._no_of_tickets

    @no_of_tickets.setter
    def no_of_tickets(self, value):
        self._no_of_tickets = value

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, value):
        self._total_price = value
