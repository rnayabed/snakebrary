from datetime import datetime



class BookReviews:
    def __init__(self, ISBN, ratings, reviews):
        self.ISBN = ISBN
        self.ratings = ratings
        self.reviews = reviews
    

class BookHolder:
    def __init__(self, username, issued_on=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), returned_on=None):
        self.username = username
        self.issued_on = issued_on
        self.returned_on = returned_on
    
    def get_raw_list(self):
        return [self.username, self.issued_on, self.returned_on]
    
    @staticmethod
    def from_list(raw_list):
        return BookHolder(raw_list[0], raw_list[1], raw_list[2])

    

class Book:
    def __init__(self, ISBN, name, author, holders, genre, price, about, photo=None,
                    date_time_added=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        self.ISBN = ISBN
        self.name = name
        self.author = author
        self.holders = holders
        self.genre = genre
        self.price = price
        self.about = about
        self.photo = photo
        self.date_time_added = date_time_added

    def return_now(self):
        self.holders[-1][2] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def get_current_holder(self):
        if len(self.holders) > 0:
            last_holder = self.holders[-1]
            if last_holder[2] == None:
                return last_holder[0]
        
        return None
            
                

    def print_details(self):
        print(self.ISBN)
        print(self.name)
        print(self.author)
        print(self.genre)
        print(self.price)
        print(self.about)
        print(self.date_time_added)


