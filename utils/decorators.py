def skip_if_swagger(default_return=None):
    """
    Decorator to safely short-circuit method if swagger_fake_view is True.
    Prevents execution of user-dependent logic during schema generation.
    """
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if getattr(self, 'swagger_fake_view', False):
                return default_return() if callable(default_return) else default_return
            return method(self, *args, **kwargs)
        return wrapper
    return decorator