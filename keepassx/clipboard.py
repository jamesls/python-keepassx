import subprocess
import platform



def copy(text):
    get_clipboard().copy(text)


def get_clipboard():
    try:
        platform_clipboard = _PLATFORMS[platform.system()]()
    except KeyError:
        raise ValueError("Unsupported clipbaord for platform %s" %
                            platform.system())
    return platform_clipboard


class ClipBoard(object):
    def copy(self, text):
        raise NotImplementedError("copy")

    def paste(self):
        raise NotImplementedError("paste")


class OSXClipBoard(ClipBoard):
    def copy(self, text):
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text)
        if process.returncode != 0:
            raise Exception("Couldn't copy text to clipboard.")


class LinuxClipboard(ClipBoard):
    def copy(self, text):
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                   stdin=subprocess.PIPE)
        process.communicate(text)
        if process.returncode != 0:
            raise Exception("Couldn't copy text to clipboard.")


_PLATFORMS = {
    'Linux': LinuxClipboard,
    'Darwin': OSXClipBoard,
}
