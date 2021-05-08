import logging
from analyzer import *

analyzer = Analyzer()
logger = logging.getLogger(__name__)


def add_component(name):
    return analyzer.add_component(name)


def add_communication(source_id, dest_id):
    try:
        analyzer.add_communication(source_id, dest_id)
    except ComponentNotFoundError:
        logger.exception("One of the connection request component id's was not found.")
        raise


def get_flow(cid):
    try:
        path = analyzer.find_shortest_path_from_internet(cid)
    except ComponentNotFoundError:
        logger.exception(f"Component with id {cid} not found. see details below.")
        raise
    except NoPathToComponentError:
        logger.exception(f"No path found to component {cid}. see details below.")
        raise
    else:
        return path


