from django.http import JsonResponse
from rest_framework.response import Response

class CustomResponse:

    @classmethod
    def success(
        cls,
        data=None,
        message: str = "Success",
        status_code: int = 200,
        extra_fields: dict | None = None,
    ) -> JsonResponse:
        if data:
            return cls._build_response(data, message, status_code, extra_fields)
        return cls._build_response(
            data=data,
            message=message,
            status_code=status_code,
            extra_fields=extra_fields,
        )

    @classmethod
    def successfully_created(
        cls,
        data=None,
        message: str = "Successfully created",
        status_code: int = 201,
        extra_fields: dict | None = None,
    ) -> JsonResponse:
        return cls._build_response(data, message, status_code, extra_fields)

    @classmethod
    def basic_response(
        cls,
        data=None,
        message: str = "Sucessfully retrive",
        status_code: int = 200,
        extra_fields: dict | None = None,
    ) -> JsonResponse:
        return cls._build_response(data, message, status_code, extra_fields)

    @classmethod
    def error(
        cls,
        message: str = "Something wrong",
        status_code: int = 400,
        extra_fields: dict | None = None,
    ) -> JsonResponse:
        # Normalize any provided errors into: { "errors": { "message": [ ... ] } }
        normalized_extra = dict(extra_fields or {})
        messages = []

        raw_errors = normalized_extra.get("errors")
        if raw_errors is not None:
            if isinstance(raw_errors, dict):
                for val in raw_errors.values():
                    if isinstance(val, (list, tuple)):
                        messages.extend([str(v) for v in val])
                    else:
                        messages.append(str(val))
            elif isinstance(raw_errors, (list, tuple)):
                messages.extend([str(v) for v in raw_errors])
            else:
                messages.append(str(raw_errors))

        if not messages:
            messages = [str(message)]

        seen = set()
        deduped = []
        for m in messages:
            if m not in seen:
                seen.add(m)
                deduped.append(m)

        normalized_extra["errors"] = {"message": deduped}
        return cls._build_response(None, message, status_code, normalized_extra)

    @staticmethod
    def _build_response(
        data,
        message: str,
        status_code: int,
        extra_fields: dict | None = None,
    ) -> JsonResponse:
        response_data = {"results": data, "message": message}
        if extra_fields:
            response_data.update(extra_fields)
        return Response(data=response_data, status=status_code)