#  This file is part of 'analyzer', the tool used to process the information
#  collected for Andrea Esposito's Thesis.
#  Copyright (C) 2020  Andrea Esposito
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import logging
import functools
from typing import Tuple, Any, Callable, TypeVar

T = TypeVar('T')


def timed(message: str = 'Completed after %.3fs') -> Callable[[Callable[..., T]], Callable[..., Tuple[T, float]]]:
    def inner_function(f: Callable[..., T]) -> Callable[..., Tuple[T, float]]:
        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Tuple[T, float]:
            start_time = time.time()
            result = f(*args, **kwargs)
            end_time = time.time()
            logging.getLogger(f.__module__).info(message, end_time - start_time)
            return result, end_time - start_time

        return wrapper

    return inner_function
