from datetime import datetime



class BookReviews:
    def __init__(self, ISBN, ratings, reviews):
        self.ISBN = ISBN
        self.ratings = ratings
        self.reviews = reviews

class Book:
    def __init__(self, ISBN, name, author, current_holder,
                 previous_holders, genre, price, photo=None, date_time_added=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        self.ISBN = ISBN
        self.name = name
        self.author = author
        self.current_holder = current_holder
        self.previous_holders = previous_holders
        self.genre = genre
        self.price = price
        self.photo = photo
        self.date_time_added = date_time_added


    def print_details(self):
        print(self.ISBN)
        print(self.name)
        print(self.author)
        print(self.current_holder)
        print(self.previous_holders)
        print(self.genre)
        print(self.price)
        print(self.date_time_added)


