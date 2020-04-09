"""
Utilities and data structures for TV series script generator
"""
from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from os import listdir
import re


ACTOR_REGEXP = r"^((young |ms. |mrs. |miss. |mr. |dr. |fat |)\w+( and \w+||)|stage director|pbs volunteer|gary collins|priest on tv|pizza guy|aunt lillian|coma guy|fireman no. \d|mr.heckles|woman no. \d|joey \w+|the director)\s*:"
STAGE_DIRECTION_REGEXP = r"^\["
SCENE_RESET_MARKERS = (
    "time lapse",
    "cut",
    "flashback scene",
    "opening credits",
    "ending credits",
    "commercial break",
    "closing credits",
)


# @dataclass  # mypy does not allow any abstract class to be a dataclass
class Action(ABC):
    """ Abstract action in script """
    @abstractmethod
    def __init__(self, text: str):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


@dataclass
class StageDirection(Action):
    """
    Action with some stage directions

    Fields:
        direction: string -- Direction text
    """
    def __init__(self, text: str):
        super(StageDirection, self).__init__(text)
        self.direction = text[1:-1].strip()

    def __str__(self):
        return f"stage direction: {self.direction}"

    def __repr__(self):
        return str(self)


@dataclass
class CharacterLine(Action):
    """
    Action where character say a line

    Fields:
        actor: string -- Name of character
        line: string -- Line text
    """
    def __init__(self, text: str):
        super(CharacterLine, self).__init__(text)
        self.actor: str = re.findall(ACTOR_REGEXP, text.lower())[0][0]
        self.line: str = text[text.find(":") + 1:].strip()

    def __str__(self):
        return f"{self.actor}: {self.line}"

    def __repr__(self):
        return str(self)


@dataclass
class Scene():
    """
    Scene class

    Fields:
        description -- entering scene description
        actions -- array of scene actions
        actors -- array of characters of this scene TODO
        place -- where the action takes place TODO
    """
    def __init__(self, script: List[str], description=None):
        self.description: str = description or script[0]

        self.actors: List[str] = []
        self.place: str = ""

        self.actions: List[Action] = []

        for line in map(str.strip, script):
            if line == "":
                pass
            if re.match(ACTOR_REGEXP, line.lower()):
                self.actions.append(CharacterLine(line))
            elif re.match(STAGE_DIRECTION_REGEXP, line):
                self.actions.append(StageDirection(line))

    def __str__(self):
        res: str = ""
        res += self.description + '\n'
        for line in self.actions:
            res += str(line) + '\n'
        return res

    def __repr__(self):
        return str(self)


def load_file(filename: str) -> List[str]:
    """ Loads file into array of strings """

    with open(filename, "r") as f:
        lines = map(str.strip, f.readlines())

    lines_concat: List[str] = []
    new_line = ""

    for line in lines:
        if line == "":
            lines_concat.append(new_line)
            new_line = ""
        else:
            new_line += " " + line

    non_empty = filter(lambda x: x != "", lines_concat)
    return [" ".join(line.split()) for line in non_empty]


def stage_direction_is_a_scene_reset(line: str) -> bool:
    line = line.lower()
    for marker in SCENE_RESET_MARKERS:
        if marker in line:
            return True
    return False


def load_scenes_from_folder(dirname: str) -> List[Scene]:
    # TODO: refactor
    scenes: List[Scene] = []

    for filename in sorted(listdir(dirname)):
        SAMPLE_FILE = f"{dirname}/{filename}"

        description: str = ''
        script: List[str] = []
        for line in load_file(SAMPLE_FILE):
            if 'scene:' in line.lower():
                if description != '' and script != []:
                    scenes.append(Scene(script, description))
                description = line
                script = []
            elif re.match(ACTOR_REGEXP, line.lower()) is not None:
                script.append(line)
            elif stage_direction_is_a_scene_reset(line):
                if description != '' and script != []:
                    scenes.append(Scene(script, description))
                script = []
                description += '\n' + line
            elif re.match(STAGE_DIRECTION_REGEXP, line.lower()) is not None:
                script.append(line)
            else:
                pass

        if description != '' and script != []:
            scenes.append(Scene(script, description))

    return scenes
