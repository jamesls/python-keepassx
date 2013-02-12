import subprocess

_CLIPBOARD = None

def copy(text):
    global _CLIPBOARD
    if _CLIPBOARD is None:
        _CLIPBOARD = OSXClipBoard()
    _CLIPBOARD.copy(text)


class ClipBoard(object):
    def copy(self, text):
        pass

    def paste(self):
        pass


class OSXClipBoard(ClipBoard):
    def copy(self, text):
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text)
        if process.returncode != 0:
            raise Exception("Couldn't copy text to clipboard.")

    def paste(self):
        pass
