#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse  # https://docs.python.org/3/library/argparse.html
import re
import sys
from dataclasses import dataclass, field
from pathlib import PurePath, Path
from typing import List, NoReturn, Tuple

from logger import get_logger
from username import Username


def create_arg_parser() -> argparse:
    """
    Metodo para establecer los argumentos que necesita la clase

    :return:
    """
    example = """python3 %(prog)s -f juan -l "sanchez perez" -o output/ -v"""

    my_parser = argparse.ArgumentParser(description='%(prog)s is a script to generate a list with possible username \
    using a first name and last name. It is compatible with compound first name and last name', usage=f'{example}')

    required_named: argparse._ArgumentGroup = my_parser.add_argument_group('required named arguments')
    required_named.add_argument('-f', '--first', help='First name only, can be simple or compound.')
    required_named.add_argument('-l', '--last', help='Last name only, can be simple or compound.')

    my_parser.add_argument('-o', '--output', help='File where the generated users will be stored.',
                           default='output.lst')
    my_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose flag (boolean).', default=False)
    # my_parser.set_defaults(output=config['DEFAULTS']['OUTPUT'])

    response: argparse = my_parser.parse_args()
    if response.first is None or response.last is None:
        logger.critical('first and last arguments are necessary.')
        my_parser.print_help()
        sys.exit(-1)

    return response


@dataclass
class Generator():
    user: Username

    usernames: List = field(default_factory=list)
    separators: Tuple = field(default_factory=tuple)

    def __post_init__(self):
        self.separators = ('.', '')  # Tipos de separadores usados
        self.first_last_complete()
        self.first_abrv_last_complete()
        self.first_complete()
        self.last_complete()
        self.last_first_complete()

    # josemaria.martinezsanchez
    def first_last_complete(self) -> NoReturn:
        for separator in self.separators:
            self.usernames.append(f'{self.user.first_name1}{separator}{self.user.last_name1}')
            for separator2 in self.separators:
                self.usernames.append(
                    f'{self.user.first_name1}{separator}{self.user.first_name2}{separator2}{self.user.last_name1}')
                self.usernames.append(
                    f'{self.user.first_name1}{separator}{self.user.last_name1}{separator2}{self.user.last_name2}')
                for separator3 in self.separators:
                    self.usernames.append(
                        f'{self.user.first_name1}{separator}{self.user.first_name2}{separator2}{self.user.last_name1}{separator3}{self.user.last_name2}')

    # j.martinez
    def first_abrv_last_complete(self):
        for separator in self.separators:
            self.usernames.append(f'{self.user.first_name1[0]}{separator}{self.user.last_name1}')
            for separator2 in self.separators:
                self.usernames.append(
                    f'{self.user.first_name1[0]}{separator}{self.user.first_name2}{separator2}{self.user.last_name1}')
                self.usernames.append(
                    f'{self.user.first_name1[0]}{separator}{self.user.last_name1}{separator2}{self.user.last_name2}')
                if self.user.first_name_complex:
                    self.usernames.append(
                        f'{self.user.first_name1[0]}{separator}{self.user.first_name2[0]}{separator2}{self.user.last_name1}')
                for separator3 in self.separators:
                    self.usernames.append(
                        f'{self.user.first_name1[0]}{separator}{self.user.first_name2}{separator2}{self.user.last_name1}{separator3}{self.user.last_name2}')
                    if self.user.first_name_complex:
                        self.usernames.append(
                            f'{self.user.first_name1[0]}{separator}{self.user.first_name2[0]}{separator2}{self.user.last_name1}{separator3}{self.user.last_name2}')

    # josemaria
    def first_complete(self):
        self.usernames.append(f'{self.user.first_name1}')
        for separator in self.separators:
            self.usernames.append(f'{self.user.first_name1}{separator}{self.user.first_name2}')

    # martinezsanchez
    def last_complete(self):
        self.usernames.append(f'{self.user.last_name1}')
        for separator in self.separators:
            self.usernames.append(f'{self.user.last_name1}{separator}{self.user.last_name2}')

    # martinezsanchez.josemaria
    def last_first_complete(self):
        for separator in self.separators:
            self.usernames.append(f'{self.user.last_name1}{separator}{self.user.first_name1}')
            for separator2 in self.separators:
                self.usernames.append(
                    f'{self.user.last_name1}{separator}{self.user.last_name2}{separator2}{self.user.first_name1}')
                for separator3 in self.separators:
                    self.usernames.append(
                        f'{self.user.last_name1}{separator}{self.user.last_name2}{separator2}{self.user.first_name1}{separator3}{self.user.first_name2}')

    def write(self, output: PurePath):
        if len(self.usernames):
            usename: str
            aux: List = list()
            for usename in list(set(self.usernames)):
                # ELiminamos los .. que aparecen por ser nombres simples
                usename = usename.replace('..', '.')
                # Si termina en . por tener apellido simple se elimina
                if re.search(r'\.$', usename):
                    aux.append(f'{usename[0:-1]}')
                    logger.debug(f'{usename[0:-1]}')
                else:
                    aux.append(f'{usename}')
                    logger.debug(f'{usename}')
            # Eliminamos los duplicados se los usuarios
            content = '\n'.join(list(set(aux)))
            logger.debug(str(output))
            # if os.access(str(output), os.R_OK):
            Path(output).write_text(content, encoding='utf-8')
            logger.info(f'File {str(output)} generated.')
            # else:
            #    logger.critical(f'Permission denied: {str(output)}')
        else:
            logger.error(f'The username list is empty')


def main():
    args: argparse = create_arg_parser()

    global logger
    logger = get_logger(args.verbose, 'generator')

    # user: Username = Username('Juan Antonio', 'Flores Caba')
    user: Username = Username(args.first, args.last)
    logger.info(user)
    generator: Generator = Generator(user)
    generator.write(PurePath(args.output))


if __name__ == '__main__':
    main()
