from typing import Iterator


def file_reader(file_name: str) -> Iterator[str]:
    """Yield entries from files"""
    for row in open(file_name, "r"):
        clean_row = row.strip("\n")
        yield clean_row
