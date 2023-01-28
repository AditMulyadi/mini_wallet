import json

from rest_framework import status
from rest_framework.response import Response

from typing import Dict, Any, Optional


class SuccessResponse(Response):
    """
    Subclassed `Response` from rest_framework to simplify constructing error messages
    """

    def __init__(self, data: Dict, status: status = status.HTTP_200_OK) -> None:
        super().__init__(status=status)

        self.data = {
            "data": data,
            "status": "success"
        }


class ErrorResponse(Response):
    """
    Subclassed `Response` from rest_framework to simplify constructing error messages
    """

    def __init__(self, form: Optional[Any] = None,
                 status: status = status.HTTP_404_NOT_FOUND, **kwargs: Any) -> None:
        super().__init__(status=status)

        data = {}

        if kwargs.get("error"):
            data["error"] = kwargs.get("error")

        elif form and form.errors.items():
            for field, errors in json.loads(form.errors.as_json()).items():
                if field == "__all__":
                    field = "error"

                data[field] = errors[0]['message']
        else:
            data["error"] = "Your request cannot be completed"

        self.data = {
            "data": data,
            "status": "fail"
        }
