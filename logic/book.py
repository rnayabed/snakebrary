from datetime import datetime


class BookRatings:
    def __init__(self, isbn, ratings):
        self.ISBN = isbn
        self.ratings = ratings

    def get_average_rating(self):
        if len(self.ratings) == 0:
            return 0.0

        s = 0.0
        for each_rating in self.ratings.values():
            s += each_rating

        return round(s / len(self.ratings), 1)

    def get_rating_by_username(self, username):
        if username in self.ratings:
            return self.ratings[username]
        return None

    def set_rating_by_username(self, username, rating):
        self.ratings[username] = rating

    def delete_rating_by_username(self, username):
        del self.ratings[username]

    def get_ratings_by_proportion(self, rating):
        return (self.get_total_ratings_for_particular_rating(rating) / len(self.ratings)) * 100

    def get_total_ratings_for_particular_rating(self, rating):
        c = 0
        for each_rating in self.ratings.values():
            if each_rating == rating:
                c += 1

        return c


class BookHolder:
    def __init__(self, username, issued_on=None, returned_on=None):
        self.username = username
        self.returned_on = returned_on

        if issued_on is None:
            issued_on = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.issued_on = issued_on

    def get_raw_list(self):
        return [self.username, self.issued_on, self.returned_on]

    @staticmethod
    def from_list(raw_list):
        return BookHolder(raw_list[0], raw_list[1], raw_list[2])


class Book:
    def __init__(self, isbn, name, author, holders, genres, price, about, is_unavailable=False, photo=None,
                 date_time_added=None):
        self.ISBN = isbn
        self.name = name
        self.author = author
        self.holders = holders
        self.genres = genres
        self.price = price
        self.about = about
        self.is_unavailable = is_unavailable
        self.photo = photo

        if date_time_added is None:
            date_time_added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.date_time_added = date_time_added

    def is_eligible_to_rate(self, username):
        for each_holder in self.holders:
            if each_holder[0] == username and each_holder[2] is not None:
                return True

        return False

    def get_stylish_genres(self):
        genres_length = len(self.genres)
        g = ''
        for i in range(genres_length):
            g += self.genres[i].capitalize()
            if i < (genres_length - 1):
                g += ', '
        return g

    def return_now(self):
        self.holders[-1][2] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def get_current_holder(self):
        if len(self.holders) > 0:
            last_holder = self.holders[-1]
            if last_holder[2] is None:
                return last_holder[0]

        return None
