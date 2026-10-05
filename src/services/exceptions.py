class ValueRequiredError(Exception):
    pass

class BadRequest(Exception):
    pass

class VerifyMismatchError(Exception):
    pass

class AgencyAlreadyExistsError(Exception):
    pass

class AgencyNotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class CACValidateError(Exception):
    pass

class InvalidAgencyCredentialsError(Exception):
    pass

class ForbiddenError(Exception):
    pass
