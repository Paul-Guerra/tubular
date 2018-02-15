'''A collection of worker child processes for the manin proess to manage'''

class Workers(object):
    def __init__(self):
        object(self)
        self.__pool = []
    
    