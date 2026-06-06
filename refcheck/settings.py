import sys

from refcheck.cli import get_command_line_arguments


class Settings:
    def __init__(self) -> None:
        # Only parse arguments if not running under pytest
        if "pytest" in sys.modules:
            # Default values used during testing; no type annotations needed here
            self._paths = []
            self._verbose = False
            self._check_remote = False
            self._no_color = False
            self._allow_absolute = False
            self._quiet = False
            self._exclude = []
        else:
            args = get_command_line_arguments()

            # Assign values without redeclaring types to avoid MyPy redefinition errors
            self._paths = args.paths
            self._verbose = args.verbose
            self._check_remote = args.check_remote
            self._no_color = args.no_color
            self._allow_absolute = args.allow_absolute
            self._quiet = args.quiet
            self._exclude = args.exclude

    def __str__(self) -> str:
        return f"Settings(paths={self.paths}, verbose={self.verbose}, check_remote={self.check_remote}, no_color={self.no_color}, allow_absolute={self.allow_absolute}, exclude={self.exclude})"

    def is_valid(self) -> bool:
        try:
            assert self.paths
        except AssertionError:
            return False
        else:
            return True

    @property
    def paths(self) -> list[str]:
        return self._paths

    @property
    def verbose(self) -> bool:
        return self._verbose

    @property
    def check_remote(self) -> bool:
        return self._check_remote

    @property
    def no_color(self) -> bool:
        return self._no_color

    @property
    def allow_absolute(self) -> bool:
        return self._allow_absolute

    @property
    def quiet(self) -> bool:
        """Return True when the ``--quiet`` flag is set.

        The flag suppresses all non‑summary output.  It does **not** affect the
        exit code or the final summary printed by ``ReferenceChecker``.
        """
        return getattr(self, "_quiet", False)

    @property
    def exclude(self) -> list[str]:
        return self._exclude


settings = Settings()
