from utils.tools import Ocean, NavalOperations
import logging





def setup_logging(log_level: int = logging.INFO):
    """
    This function will set up the logging for the project.

    Args:
        log_level (int): The logging level. defaults to logging.INFO
    """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=log_level)

def main():
    setup_logging()
    project = Ocean()   # loading a new project since no session and path is provided
    fleet = NavalOperations(ocean=project).load_fleet()


if __name__ == "__main__":
    main()