#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from typing import NoReturn

from logger import get_logger

logger = get_logger(False, 'generator')


@dataclass
class Username(object):
    first_name1: str
    last_name1: str

    first_name2: str = ''
    last_name2: str = ''
    first_name_complex: bool = field(repr=False, default=False)
    last_name_complex: bool = field(repr=False, default=False)

    def __post_init__(self: Username) -> NoReturn:
        if self.first_name1 is None or self.last_name1 is None:
            logger.critical(f'first_name1 or last_name1 is None')
            sys.exit(-1)

        self.first_name1 = self.first_name1.lower()
        self.last_name1 = self.last_name1.lower()

        regex = r'(\w+) (\w+)'
        regex_first = re.search(regex, self.first_name1)
        if regex_first:
            self.first_name1 = regex_first.group(1)
            self.first_name2 = regex_first.group(2)
            self.first_name_complex = True
        else:
            self.first_name_complex = False

        regex_last = re.search(regex, self.last_name1)
        if regex_last:
            self.last_name1 = regex_last.group(1)
            self.last_name2 = regex_last.group(2)
            self.last_name_complex = True
        else:
            self.last_name_complex = False

    def __str__(self: Username) -> NoReturn:
        return f"{self.__class__.__name__}(first_name1='{self.first_name1}', first_name2='{self.first_name2}', " \
               f"last_name1='{self.last_name1}', last_name2='{self.last_name2}')"
