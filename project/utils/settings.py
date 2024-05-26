import importlib
from os import getenv

empty = object()


class LazyObject:
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.
    """

    _wrapped = None

    def __init__(self):
        self._wrapped = empty

    def _setup(self):
        """
        Must be implemented by subclasses to initialize the wrapped object.
        """
        raise NotImplementedError(
            "subclasses of LazyObject must provide a _setup() method"
        )

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup()
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            super().__setattr__(name, value)
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def __dir__(self):
        if self._wrapped is empty:
            self._setup()
        return dir(self._wrapped)


class Settings:
    def __init__(self, settings_module):
        self.settings_module = settings_module
        mod = importlib.import_module(self.settings_module)
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)


class LazySettings(LazyObject):
    def _setup(self, name=None):
        settings_module = getenv("SETTINGS_MODULE")
        if not settings_module:
            desc = ("setting %s" % name) if name else "settings"
            raise Exception(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (desc, "SETTINGS_MODULE")
            )
        self._wrapped = Settings(settings_module)

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup(name)

        return getattr(self._wrapped, name)


settings = LazySettings()
