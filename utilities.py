"""
  This utilities file includes util methods that we may need in our app
"""

from typing import Tuple, IO, Iterator, List, Dict


def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    """ A generator to read files, skipping comments and combining lines ending in '\'
            Return the portion of each line without comments.
            Based on a solution by Jeff Maassen.
    """
    try:
        fp: IO = open(path, 'r', encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't open '{path}'")
    else:
        with fp:
            cnt: int = 0
            for line in fp:
                cnt += 1
                line = line.rstrip('\n')
                lst: List = line.split(sep)
                if len(lst) != fields:
                    raise ValueError(
                        f"'{path}' has {len(lst)} fields on line {cnt} but expected {fields} ")
                if header == True:
                    header = False
                    line = next(fp).rstrip("\n")
                yield line.split(sep)
