from dijkstar import Graph, find_path, NoPathError
from functools import lru_cache


class Component:
    """
    Represents a component within a network. Modeled after a directed graph.
    """
    def __init__(self, name, cid):
        self._connections = set()
        self._name = name
        self._cid = cid

    def add_connection(self, component):
        assert type(component) is Component
        self._connections.add(component)

    def get_connections(self):
        return self._connections.copy()

    def get_id(self):
        return self._cid


class Analyzer:
    def __init__(self):
        self._next_id = 1
        self._components_by_id = dict()
        self._the_internet = Component("The internet", 0)
        self._components_by_id[0] = self._the_internet

    def add_component(self, component_name):
        cid = self._next_id
        self._next_id += 1
        self._components_by_id[cid] = Component(component_name, cid)
        return cid

    def add_communication(self, source_id, dest_id):
        source_id = source_id if source_id is not None else 0
        if source_id not in self._components_by_id or dest_id not in self._components_by_id:
            raise ComponentNotFoundError
        destination = self._components_by_id.get(dest_id)
        source = self._components_by_id.get(source_id)
        source.add_connection(destination)

    @lru_cache
    def find_shortest_path_from_internet(self, dest_cid):
        if dest_cid not in self._components_by_id.keys():
            raise ComponentNotFoundError
        model = Graph()
        for vertex in self._components_by_id.keys():
            for neighbor in self._components_by_id.get(vertex).get_connections():
                model.add_edge(vertex, neighbor.get_id(), 1)
        try:
            path = find_path(model, 0, dest_cid).nodes[1:]
        except NoPathError:
            raise NoPathToComponentError
        return path


class ComponentNotFoundError(Exception):
    pass


class NoPathToComponentError(Exception):
    pass


class MissingArgumentsError(Exception):
    pass
