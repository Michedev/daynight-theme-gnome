

def get_cmd_background(imgpath: str) -> str:
    return f"gsettings set org.gnome.desktop.background picture-uri file://{imgpath}"
