"""Configure imports for tests.

The kql-validator directory uses a hyphen (per project convention),
but Python package names cannot contain hyphens. This conftest sets up
the import path so 'kql_validator' resolves correctly.
"""

import importlib
import sys
from pathlib import Path

# Register the kql-validator directory as 'kql_validator' package
_validator_dir = Path(__file__).resolve().parent.parent
_package_name = "kql_validator"

if _package_name not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        _package_name,
        _validator_dir / "__init__.py",
        submodule_search_locations=[str(_validator_dir)],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[_package_name] = mod
    spec.loader.exec_module(mod)
