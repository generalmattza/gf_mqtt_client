from typing import Optional


class ResponseException(Exception):
    """
    Base for all response‑related errors. Carries:
      - response_code: numeric status (e.g. 404, 500)
      - path: the URI or topic requested
      - detail: any payload or error message returned
      - source: who sent it (e.g. 'broker', 'handler')
      - target: the intended recipient or device tag
    """
    default_code: Optional[int] = None

    def __init__(
        self,
        detail: Optional[str] = None,
        *,
        path: Optional[str] = None,
        source: Optional[str] = None,
        target: Optional[str] = None,
        response_code: Optional[int] = None,
        request_id: Optional[str] = None,
        method: Optional[str] = None

    ):
        # pick the explicit response_code or fall back to subclass default
        self.response_code = response_code if response_code is not None else self.default_code
        self.path = path
        self.detail = detail
        self.source = source
        self.target = target
        self.request_id = request_id
        self.method = method

        parts = [f"code={self.response_code}"]
        if path:
            parts.append(f"path={path!r}")
        if source:
            parts.append(f"source={source!r}")
        if target:
            parts.append(f"target={target!r}")
        if request_id:
            parts.append(f"request_id={request_id!r}")
        if method:
            parts.append(f"method={method!r}")

        super().__init__(f"{detail!r} {self.__class__.__name__}: " + ", ".join(parts))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"response_code={self.response_code!r}, "
            f"path={self.path!r}, "
            f"detail={self.detail!r}, "
            f"source={self.source!r}, "
            f"target={self.target!r}, "
            f"request_id={self.request_id!r}, "
            f"method={self.method!r}"
            f")"
        )


class BadRequestResponse(ResponseException):
    """400 Bad Request"""
    default_code = 400


class UnauthorizedResponse(ResponseException):
    """401 Unauthorized"""
    default_code = 401


class NotFoundResponse(ResponseException):
    """404 Not Found"""
    default_code = 404


class MethodNotAllowedResponse(ResponseException):
    """405 Method Not Allowed"""
    default_code = 405


class InternalServerErrorResponse(ResponseException):
    """500 Internal Server Error"""
    default_code = 500


class GatewayTimeoutResponse(ResponseException):
    """504 Gateway Timeout"""
    default_code = 504
