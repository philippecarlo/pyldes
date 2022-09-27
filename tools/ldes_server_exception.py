
class LdesServerError(Exception):
    pass

class LdesPresistenceError(LdesServerError):
    pass

class LdesNotFoundError(LdesServerError):
    pass