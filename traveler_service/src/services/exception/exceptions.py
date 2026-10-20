class ValueRequiredError(Exception):
    pass

class BadRequest(Exception):
    pass

class VerifyMismatchError(Exception):
    pass

class TravelerAlreadyExistsError(Exception):
    pass

class TravelerNotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class CACValidateError(Exception):
    pass

class InvalidTravelerCredentialsError(Exception):
    pass

class ForbiddenError(Exception):
    pass
