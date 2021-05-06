import json
import math
import logging


logger = logging.getLogger(__name__)


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
        self.next_id = 1
        self.components_by_id = dict()
        self.the_internet = Component("The internet", 0)
        self.components_by_id[0] = self.the_internet

    def add_components(self, component_list):
        for comp in component_list:
            self.components_by_id[self.next_id] = Component(comp["name"], self.next_id)
            self.next_id += 1

    def add_communications(self, communications_list):
        for comm in communications_list:
            source = comm["source"] if comm["source"] is not None else 0
            self.components_by_id[source].add_connection(self.components_by_id[comm["destination"]])

    def find_shortest_path_from_internet(self, destination_cid):
        """
        Finds and returns the shortest flow from the internet to destination component using Dijkstra's
        shortest-path algorithm.
        :param destination_cid: id of the destination component
        :return: list containing flow of component id's from internet to destination, None if component not reachable
        """
        dist = dict()
        prev = dict()
        queue = set()

        for comp in self.components_by_id.values():
            dist[comp] = math.inf
            prev[comp] = None
            queue.add(comp)

        dist[self.components_by_id[0]] = 0

        while len(queue) > 0:
            u = min(queue, key=lambda x: dist.get(x))
            queue.remove(u)
            for v in u.get_connections():
                if v in queue:
                    alt = dist.get(u) + 1
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u

        if dist[self.components_by_id[destination_cid]] == math.inf:
            logger.log(f"Destination component specified ({destination_cid}) is unreachable from the internet.")
            return None
        else:
            print(f"Found root from internet to destination {destination_cid} through "
                  f"{dist[self.components_by_id[destination_cid]]} components.")

        flow = list()
        node = self.components_by_id[destination_cid]
        while node.get_id() != 0:
            flow.append(node.get_id())
            node = prev[node]
        flow.reverse()
        return flow


def add_objects_request(json_input):
    analyzer = Analyzer()

    data = json.loads(json_input)
    analyzer.add_components(data["components"])
    analyzer.add_communications(data["communications"])


def get_flow(cid):
    analyzer = Analyzer()
    return analyzer.find_shortest_path_from_internet(cid)
