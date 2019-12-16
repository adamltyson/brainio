__version__ = "0.0.9"
__author__ = "Adam Tyson, Charly Rousseau"
__license__ = "GPL-3.0"
__name__ = "brainio"

import luddite
from packaging import version

most_recent_version = luddite.get_version_pypi(__name__)

if version.parse(__version__) < version.parse(most_recent_version):
    print(f"This version of {__name__} ({__version__}) is not the most recent "
          f"version. Please update to v{most_recent_version} by running: "
          f"'pip install {__name__} --upgrade'")
