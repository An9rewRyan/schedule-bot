class BaseBookingException(Exception):
    """
    Basic class for booking exceptions
    """

class BookingRequestException(BaseBookingException):
    """
    Throw when error appears while booking request
    """



class TooSmallBookingDurationException(BaseBookingException):
    """
    Throw an exception when Booking request has less than 3 timeslots (1.30h)
    """


class NotEnoughSlotsException(BaseBookingException):
    """
    Throw an exception when available slots amount are less than requested
    """


class RequestedSlotsBusyException(BaseBookingException):
    """
    Throw an exception when one or many requested slots are already occupied
    """


class BookingSaveFailedException(BaseBookingException):
    """
    Throw an exception when saving booking to database failed
    """


class BookingNotFoundException(BaseBookingException):
    """
    Throw an exception when requested booking not found
    """
