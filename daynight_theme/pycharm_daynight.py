from dataclasses import dataclass, field
from typing import Final

from path import Path
from daynight_theme.command import Command
import os

night_theme_xml = """\
<application> 
    <component name="LafManager" autodetect="false">
        <laf class-name="com.intellij.ide.ui.laf.darcula.DarculaLaf" />
    </component>
</application>"""

day_color_scheme_xml = """\
<application>
  <component name="EditorColorsManagerImpl">
    <global_color_scheme name="IntelliJ Light" />
  </component>
</application>"""

night_color_scheme_xml = """\
<application>
  <component name="EditorColorsManagerImpl">
    <global_color_scheme name="Darcula" />
  </component>
</application>"""

day_theme_xml = """\
<application>
  <component name="LafManager" autodetect="false">
    <laf class-name="com.intellij.ide.ui.laf.IntelliJLaf" themeId="JetBrainsLightTheme" />
  </component>
</application>"""

path_configs = Path(os.environ["HOME"]) / ".config" / "JetBrains"


def pycharm_set_theme(xml_text: str):
    for dirpath in path_configs.walkdirs('PyCharm*'):
        filepath = dirpath / "options" / "laf.xml"
        with open(filepath, 'w') as f:
            f.write(xml_text)
        print("wrote into", filepath)


def pycharm_set_color_scheme(xml_text: str):
    for dirpath in path_configs.walkdirs('PyCharm*'):
        filepath = dirpath / "options" / "colors.scheme.xml"
        with open(filepath, 'w') as f:
            f.write(xml_text)
        print("wrote into", filepath)


def exists_pycharm():
    return path_configs.exists()


@dataclass
class PycharmThemeSetter(Command):
    day_theme_xml: str = """\
<application>
  <component name="LafManager" autodetect="false">
    <laf class-name="com.intellij.ide.ui.laf.IntelliJLaf" themeId="JetBrainsLightTheme" />
  </component>
</application>"""

    night_theme_xml: str = """\
<application> 
    <component name="LafManager" autodetect="false">
        <laf class-name="com.intellij.ide.ui.laf.darcula.DarculaLaf" />
    </component>
</application>"""

    day_value: str = field(init=False, default=day_theme_xml)

    night_value: str = field(init=False, default=night_theme_xml)

    def action(self, xml_text: str):
        for dirpath in path_configs.walkdirs('PyCharm*'):
            filepath = dirpath / "options" / "laf.xml"
            with open(filepath, 'w') as f:
                f.write(xml_text)
            print("wrote into", filepath)

@dataclass
class PycharmColorSetter(Command):

    day_color_scheme_xml = """\
    <application>
      <component name="EditorColorsManagerImpl">
        <global_color_scheme name="IntelliJ Light" />
      </component>
    </application>"""

    day_value: str = field(init=False, default=day_color_scheme_xml)

    night_color_scheme_xml = """\
    <application>
      <component name="EditorColorsManagerImpl">
        <global_color_scheme name="Darcula" />
      </component>
    </application>"""

    night_value: str = field(init=False, default=night_color_scheme_xml)

    def action(self, xml_text: str):
        for dirpath in path_configs.walkdirs('PyCharm*'):
            filepath = dirpath / "options" / "colors.scheme.xml"
            with open(filepath, 'w') as f:
                f.write(xml_text)
            print("wrote into", filepath)


PYCHARM_THEME_CMD: Final[Command] = PycharmThemeSetter()
PYCHARM_COLOR_CMD: Final[Command] = PycharmColorSetter()
