

def set_cmd_background_(imgpath: str) -> str:
    return f"gsettings set org.gnome.desktop.background picture-uri file://{imgpath}"
