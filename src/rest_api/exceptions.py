from werkzeug.exceptions import HTTPException

class ErrorResponse(HTTPException):
    def __init__(self, code, message):
        super().__init__()
        self.code = code
        self.message = message
