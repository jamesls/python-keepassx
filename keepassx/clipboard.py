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
    COPY_PROCESS = []

    def copy(self, text):
        process = subprocess.Popen(self.COPY_PROCESS, stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        if process.returncode != 0:
            raise Exception("Couldn't copy text to clipboard.")

    def paste(self):
        raise NotImplementedError("paste")


class OSXClipBoard(ClipBoard):
    COPY_PROCESS = ['pbcopy']


class LinuxClipboard(ClipBoard):
    COPY_PROCESS = ['xclip', '-selection', 'clipboard']


_PLATFORMS = {
    'Linux': LinuxClipboard,
    'Darwin': OSXClipBoard,
}
