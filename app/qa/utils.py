from typing import Union


def validate_marks(mark: Union[str, int]) -> bool:
    if isinstance(mark, int) and 0<=mark<=100:
        return True
    elif (isinstance(mark, str) and mark.isdigit()) or isinstance(mark, float):
        if 0<=int(mark)<=100:
            return True

    return False