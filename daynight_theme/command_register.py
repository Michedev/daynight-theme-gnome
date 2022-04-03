from typing import Iterator, Tuple

import numpy as np

_register_class = list()
_register_priority = list()


def register_command(priority: int = 0):
    def decorator(class_: 'Command'):
        _register_class.append((class_.__name__, class_))
        _register_priority.append(priority)
        return class_
    return decorator


def iter_commands() -> Iterator[Tuple[str, 'Command']]:
    i_sorted = np.argsort(_register_priority)
    for i in i_sorted:
        yield _register_class[i]
