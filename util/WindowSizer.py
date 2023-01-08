from screeninfo import get_monitors
from util.SettingsReader import SettingsReader

class WindowSizer:
    """A class responsible for getting the window size

    Attributes
    ----------
    writingAreaSizes : dict
        Dictionary hold settings related to writing area sizes

    Methods
    -------
    getWritingAreaSize(title, content)
        Get writing area size according to current display resolution
    """
    def __init__(self):
        self.writingAreaSizes = SettingsReader().getWritingAreaSizeSettings()

    def getWritingAreaSize(self) -> list:
        """Get writing area size according to current display resolution

        Returns
        -------
        list
            List contains the width and margin of the writing area
        """
        for m in get_monitors():
            if m.is_primary:
                height = m.height
                width = m.width

        return self.writingAreaSizes[str(width)][str(height)]
