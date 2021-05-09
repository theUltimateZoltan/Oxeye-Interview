import logging
from analyzer import Analyzer, ComponentNotFoundError, NoPathToComponentError


class AppLogic:
    def __init__(self):
        self.analyzer = Analyzer()
        self.logger = logging.getLogger(__name__)

    def add_component(self, name):
        return self.analyzer.add_component(name)

    def add_communication(self, source_id, dest_id):
        try:
            self.analyzer.add_communication(source_id, dest_id)
        except ComponentNotFoundError:
            self.logger.exception("One of the connection request component id's was not found.")
            raise

    def get_flow(self, cid):
        try:
            path = self.analyzer.find_shortest_path_from_internet(cid)
        except ComponentNotFoundError:
            self.logger.exception(f"Component with id {cid} not found. see details below.")
            raise
        except NoPathToComponentError:
            self.logger.exception(f"No path found to component {cid}. see details below.")
            raise
        else:
            return path


