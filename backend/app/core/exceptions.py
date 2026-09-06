class WeatherGPTError(Exception):
    """Base application error."""


class ExternalServiceError(WeatherGPTError):
    """A required external weather service could not be reached."""


class DataUnavailableError(WeatherGPTError):
    """No live or cached data is available for the request."""
