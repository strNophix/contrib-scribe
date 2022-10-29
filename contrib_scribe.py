#!/usr/bin/env python3
import base64
import configparser
import typing
import sys
import pathlib
from datetime import date, timedelta
import subprocess as sub
import appdirs

CharRepr = typing.List[typing.List[typing.Literal[0] | typing.Literal[1]]]

CHAR_SPACING = 1
FONT_MAP: typing.Mapping[str, CharRepr] = {
    "A": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
    ],
    "B": [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
    ],
    "C": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ],
    "D": [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
    ],
    "E": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "F": [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ],
    "G": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
    ],
    "H": [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
    ],
    "I": [
        [1],
        [1],
        [1],
        [1],
        [1],
        [1],
        [1],
    ],
    "J": [
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "K": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "L": [
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "M": [
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
    ],
    "N": [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 1, 1],
    ],
    "O": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ],
    "P": [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ],
    "Q": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
    ],
    "R": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
    ],
    "S": [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ],
    "T": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "U": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "V": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
    ],
    "W": [
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ],
    "X": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "Y": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "Z": [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1],
    ],
    " ": [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ],
}


def message_to_matrix(message: str) -> CharRepr:
    matrix: CharRepr = [[] for _ in range(7)]

    for char in message:
        crepr = FONT_MAP.get(char)
        if not crepr:
            raise ValueError(f'No repr for "{char}" found in font mapping.')
        for i in range(7):
            matrix[i].extend(crepr[i])
            matrix[i].extend([0] * CHAR_SPACING)

    return matrix


def print_char_matrix(matrix: CharRepr):
    fill = {0: " ", 1: "█"}
    for row in matrix:
        print("".join(fill[char] for char in row))

    print(f"\nWidth: {len(matrix[0])}")


def parse_config(path: str) -> typing.Mapping[str, str]:
    parser = configparser.ConfigParser()
    parser.read(path)
    return parser["contrib_scribe"]


def parse_state(path: pathlib.Path) -> date:
    if not path.exists():
        state = date.today()
        if (weekday := state.weekday()) != 6:
            state += timedelta(days=6 - weekday)
        with path.open("w") as fp:
            fp.write(str(state))
        return state

    with path.open("r") as fp:
        return date.fromisoformat(fp.read())


def main(args: typing.Sequence[str]) -> int:
    if len(args) < 1:
        print("Usage: contrib_scribe.py <config.ini>", file=sys.stderr)
        return 1

    cfg = parse_config(args[0])
    cfg_id = base64.b32encode(bytearray(args[0], "ascii")).decode("utf-8")

    data_dir = appdirs.user_data_dir("contrib-scribe")
    data_path = pathlib.Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)

    state_path = data_path / cfg_id
    start_date = parse_state(state_path)

    message = cfg["message"].upper()
    matrix = message_to_matrix(message)

    print_char_matrix(matrix)

    day_diff = (date.today() - start_date).days
    row, column = day_diff % 7, day_diff // 7
    if matrix[row][column] == 0:
        print("No commit's to do today!")
        return 0

    file_path = pathlib.Path(cfg["repo_path"]) / "test"
    commit_count = int(cfg["commit_count"])
    for i in range(commit_count):
        file_path.write_text(str(i))
        commands = [["git", "add", "."], ["git", "commit", "-m", str(i)]]
        for command in commands:
            sub.call(command, cwd=file_path.parent)

    sub.call(["git", "push"], cwd=file_path.parent)
    print("Did daily commit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
