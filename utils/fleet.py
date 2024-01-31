from utils.boat import Boat
from typing import List
import json
from uuid import uuid4
from dataclasses import dataclass, field


@dataclass
class Fleet:
    id: uuid4 = field(default_factory=uuid4)
    boats: List[Boat] = field(default_factory=list)
    mission: str = field(default=None)

    def render_json(self) -> str:
        """
        This method will dump the fleet to a json string.
        Return:
            str: The json string of the fleet.
        """
        return json.dumps({
            'fleet': [boat.render_json() for boat in self.boats],
            'mission': self.mission,
            'id': str(self.id)
        })

    @staticmethod
    def load_from_json_string(json_string: str) -> "Fleet":
        """
        This method will load the fleet from a json string.
        Args:
            json_string: The configuration of the fleet as json string

        Returns:
            Fleet: The fleet object.
        """
        return Fleet(*json_string)


