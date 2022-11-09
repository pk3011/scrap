from sys import version_info

from pyrogram import __version__ as __pyrog_version__
from pyrogram.raw.all import layer

"""
https://github.com/UsergeTeam/Userge/blob/alpha/userge/versions.py
"""

__major__ = 2
__minor__ = 0
__micro__ = 0


def get_version() -> str:
    return f"{__major__}.{__minor__}.{__micro__}"


__pyrog_version__ = __pyrog_version__.replace("'", "").replace("{", "").replace("}", "")
layer = str(layer)
layer = layer.replace("'", "")

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
__bot_version__ = get_version()
__pyro_version__ = __pyrog_version__
__pyro_layer__ = layer
__license__ = "[GNU Affero General Public License v3.0](https://github.com/missemily22/MultiFunctionBot/blob/main/LICENSE)"
__gitrepo__ = "https://github.com/missemily22/MultiFunctionBot"
