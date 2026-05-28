class FootballPredictorError(Exception):
    pass


class APIError(FootballPredictorError):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class DataValidationError(FootballPredictorError):
    pass


class ModelNotFoundError(FootballPredictorError):
    pass


class InsufficientDataError(FootballPredictorError):
    pass


class FeatureEngineeringError(FootballPredictorError):
    pass