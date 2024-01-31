#
# This file contains the code for helper functions
#
import json
from dataclasses import dataclass, field
from utils.protocols import NavalObject
from utils.fleet import Fleet
import glob
from uuid import uuid4
import os
import json
import logging


@dataclass
class Ocean:
    """
    This class takes the argument of a path if the path does not exist, it will create the path.

    Args:
        work_dir (str): The path to the directory where the data will be stored.
                        defaults to ./work_dir/session_id
        session_id (uuid4): The session id of the current session. defaults to a new session id.
    """
    work_dir: str = field(default=None)
    session_id: uuid4 = field(default=None)
    session_path: str = field(default=None, init=False)

    def __post_init__(self):
        self._set_work_dir()    
        if self.session_id is None or self.session_id == '':
            self._set_session()
        self._set_session_path()

    def _set_work_dir(self):
        """
        This method will set the workdir to ./work_dir and create the directory if it does not exist.
        """
        if self.work_dir is None or self.work_dir == '':
            self.work_dir = os.path.join(os.getcwd(), 'work_dir')
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
        logging.info(f'Work dir: {self.work_dir}')
        
    def _set_session(self):
        """
        This method will set the session id to a new session id.
        """
        self.session_id = uuid4()
        logging.info(f'Session id: {self.session_id}')
    
    def _set_session_path(self):
        """
        This method will set the session path to provided <working_dir>/session_id and create the directory if it does not exist.
        """
        self.session_path = os.path.join(self.work_dir, str(self.session_id))
        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)
        logging.info(f'Session path: {self.session_path}')


@dataclass
class NavalOperations:
    ocean: Ocean = None

    def __post_init__(self):
        if self.ocean is None:
            self.ocean = Ocean()

    @staticmethod
    def _create_new_fleet() -> Fleet:
        fleet = Fleet(boats=[], mission='')
        with open(fleet_path, 'w') as fleet_config_file:
            fleet_config_file.write(fleet.render_json())
            fleet_config_file.close()
        logging.info(f'Fleet config created at {fleet_path}')
        return fleet

    def load_fleet(self) -> Fleet:
        """
        Loads a fleet config from ocean.session_path/fleet.json if none is found a new one will be created

        Returns:
            Fleet: The fleet config
        """
        fleet_path = os.path.join(self.ocean.session_path, 'fleet.json')
        if not os.path.exists(fleet_path):
            fleet = self._create_new_fleet(fleet_path=fleet_path)
        else:
            with open(fleet_path, 'r') as fleet_config_file:
                fleet = Fleet.load_from_json_string(json_string=fleet_config_file.read())
        return fleet

    def _check_naval_object_type(self, naval_object_path: str) -> NavalObject:
        """
        Checks if the filename of the navel object is the same like the parent directory name
            ie if xxx/xxx.json it will check if xxx is the same as the parent directory name

        Args:
            navel_object_path:

        Returns:

        """
        naval_object_name = os.path.basename(naval_object_path)
        naval_object_parent_dir = os.path.basename(os.path.dirname(naval_object_path))
        if naval_object_name == naval_object_parent_dir:
            return self._load_fleet(naval_object_path)
        else:
            return self._load_boat(naval_object_path)






    def _load_naval_objects(self, naval_id: str) -> NavalObject:
        """
        Looks up the naval object based on the naval_id in the current working directory

        Args:
            naval_id:

        Returns:
            NavalObject: The naval object either Fleet or Boat

        Raises:
            FileNotFoundError: If no naval object is found with the provided naval_id
            FileNotFoundError: If multiple naval objects are found with the provided naval_id
        """
        naval_object_candidates = glob.glob(f'{self.ocean.session_path}/**/{naval_id}.json', recursive=True)
        if len(naval_object_candidates) == 0:
            raise FileNotFoundError(f'No naval object found with id {naval_id}')
        elif len(naval_object_candidates) > 1:
            raise FileNotFoundError(f'Multiple naval objects found with id {naval_id}, please provide a unique naval_id')
        else:
            return self._check_naval_object_type(navel_object_path = naval_object_candidates[0])

    def load_naval_objects(self, naval_id: str = None) -> NavalObject:
        """
        This method is an abstraction method to load naval objects like fleet and boat based on the naval_id.

        Returns:
            NavalObject: The naval object either Fleet or Boat
        """
        if naval_id is None:
            naval_object = self._create_new_fleet()
        else:
            naval_object = self._load_naval_objects(naval_id)
        return naval_object