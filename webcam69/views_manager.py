import importlib
import inspect
import pkgutil
from types import ModuleType, SimpleNamespace
from typing import List, Union

from aiohttp import web

import views


class ViewsManager:
    def __init__(
        self, app: web.Application, *, source_package: Union[SimpleNamespace, '__init__'] = views
    ):
        self._app = app
        self._allowed_http_methods = [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
            "TRACE",
            "CONNECT",
        ]
        self._source_package = source_package

    def register_routes(self) -> None:
        package_modules = self._get_package_view_modules()
        for module in package_modules:
            self._attach_module_views_to_routes(module_obj=module)

    def _get_package_view_modules(
        self, source_package: Union[SimpleNamespace, ModuleType] = None
    ) -> List[ModuleType]:
        """Recursively searches for all modules in a package"""
        module_objects = []
        source_package = (
            self._source_package if source_package is None else source_package
        )

        for module_info in pkgutil.iter_modules(source_package.__path__):
            module_obj = importlib.import_module(
                f"{source_package.__name__}.{module_info.name}"
            )

            if not module_info.ispkg:
                module_objects.append(module_obj)
            else:
                package_views = self._get_package_view_modules(
                    source_package=module_obj
                )
                module_objects.extend(package_views)

        return module_objects

    def _attach_module_views_to_routes(self, module_obj: ModuleType) -> None:
        """
        Inspect module and register object methods as routes
        for current application
        """

        for name, obj in inspect.getmembers(module_obj):
            if inspect.isclass(obj) and web.View in obj.__bases__:
                if not hasattr(obj, "endpoint"):
                    raise NotImplementedError(
                        f"View class {name} must have 'endpoint' attribute"
                    )

                view_methods = [
                    method for method in self._allowed_http_methods if hasattr(obj, method.lower())
                ]

                for method in view_methods:
                    route = web.route(method, obj.endpoint, obj)
                    self._app.router.add_routes([route])
