import random

class Functions:
    
    @staticmethod
    def prob(p):
        return True if (random.randrange(0, 1000))/10.0 <= p else False