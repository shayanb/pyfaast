class PyfastError(Exception):
    pass


class RequestError(PyfastError):
    pass


class InitializationError(PyfastError):
    pass


class RecsError(PyfastError):
    pass


class RecsTimeout(RecsError):
    pass
