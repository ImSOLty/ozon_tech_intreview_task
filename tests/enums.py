import enum


class Filetype(enum.Enum):
    DIR = 'dir'
    FILE = 'file'

    def __str__(self):
        return self.value
