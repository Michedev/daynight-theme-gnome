import os


def set_shell_theme_cmd(theme):
    cmd = f'gsettings set org.gnome.shell.extensions.user-theme name "{theme}"'
    os.system(cmd)

def set_theme_cmd(theme: str):
    cmd = f'gsettings set org.gnome.desktop.interface gtk-theme "{theme}"'
    os.system(cmd)