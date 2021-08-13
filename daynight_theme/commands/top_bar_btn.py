from daynight_theme.commands.command import Command
import os


class TopBarBtn(Command):

    @staticmethod
    def can_add_to_registry(config) -> bool:
        return config['unite_button']

    @property
    def day_value(self) -> str:
        key = 'unite_daybutton'
        return self.config[key] if key in self.config else 'united-dark'

    @property
    def night_value(self) -> str:
        key = 'unite_nightbutton'
        return self.config[key] if key in self.config else 'united-light'

    def action(self, value: str):
        value = f"""  "'{value}'"  """.strip()
        os.system(f'dconf write /org/gnome/shell/extensions/unite/window-buttons-theme {value}')
