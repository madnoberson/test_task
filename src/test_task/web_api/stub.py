__all__ = ("Stub",)

from typing import Callable


class Stub:
    """
    This class is used to prevent fastapi from digging into
    real dependencies attributes detecting them as request data

    So instead of
    `dependency: Annotated[Dependency, Depends()]`
    Write
    `dependency: Annotated[Dependency, Depends(Stub(Dependency))]`
    """

    def __init__(self, dependency: Callable, **kwargs):
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        if isinstance(other, Stub):
            return (
                self._dependency == other._dependency
                and self._kwargs == other._kwargs
            )
        else:
            if not self._kwargs:
                return self._dependency == other
            return False

    def __hash__(self):
        if not self._kwargs:
            return hash(self._dependency)

        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)