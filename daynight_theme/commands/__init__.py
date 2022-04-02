from .bitday_background import BitDayBackground
from .gnome_themes import GnomeThemeSetter, GnomeShellThemeSetter
from .pycharm_daynight import PycharmThemeSetter, exists_pycharm
from .notification import SendNotification


"""
How to add new Command:
    
1. Add new subclass of Command and implement abstract methods
2. Update init_registry(config) into file command_register.py
3. Optionally update daynight_theme_config.main() to add values into saved config
"""