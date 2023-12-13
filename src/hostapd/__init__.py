from ._file_manager import get_json_path, set_json_path
from ._utils import get_dummy_mode, set_dummy_mode
from . import mac_manager
from . import user_manager
from . import notifier
from . import whitelist_updater

import sys, os

def can_run():
    # Checking if we are a root user when running in not dummy mode.
    return get_dummy_mode() or (sys.platform in ["linux", "linux2"] and not os.geteuid() == 0)
