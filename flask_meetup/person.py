from numpy import np

class Person(object):
    def __init__(self,dictionary):
        self.cuisine = np.array(dictionary["data"]).reshape(16,)
        self.price = dictionary["price"]
        self.location = np.array(dictionary["location"]).reshape(2,)