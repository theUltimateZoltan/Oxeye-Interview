import unittest
from analyzer import Component, Analyzer, NoPathToComponentError
from applogic import AppLogic
import requests
import json


class MockUser:
    def __init__(self):
        self.host = "http://127.0.0.1"
        self.port = 8000

    def post(self, route, **kwargs):
        return requests.post(f"{self.host}:{self.port}/{route}", params=kwargs)

    def get(self, route, **kwargs):
        return requests.get(f"{self.host}:{self.port}/{route}", params=kwargs)

    def post_component(self, cname):
        return self.post("component", name=cname)

    def post_communication(self, src, dest):
        return self.post("communication", source=src, destination=dest)

    def get_flow(self, cid):
        return self.get("flow", component=cid)


user = MockUser()


class TestAnalyzer(unittest.TestCase):
    def test_componentBehavior(self):
        c = Component("test", 12)
        d = Component("test2", 42)
        c.add_connection(d)
        self.assertEqual(c.get_id(), 12)
        self.assertEqual(c.get_connections(), {d})

    def test_analyzerDataStructures(self):
        a = Analyzer()
        cids = list()
        for comp in ["test1", "test2"]:
            cids.append(a.add_component(comp))
        for comm in [{"source": 1, "destination": 2}, {"source": None, "destination": 1}]:
            a.add_communication(comm.get("source"), comm.get("destination"))
        path = a.find_shortest_path_from_internet(2)
        self.assertEqual(path[0], cids[0])
        self.assertEqual(path[1], cids[1])

    def test_unreachable(self):
        a = Analyzer()
        for comp in ["test1", "test2"]:
            a.add_component(comp)
        for comm in [{"source": None, "destination": 1}]:
            a.add_communication(comm.get("source"), comm.get("destination"))
        try:
            a.find_shortest_path_from_internet(2)
        except NoPathToComponentError:
            pass
        else:
            self.fail()

    def test_loop(self):
        a = Analyzer()
        cids = list()
        for comp in ["test1", "test2"]:
            cids.append(a.add_component(comp))
        for comm in [{"source": 1, "destination": 2},
                     {"source": 2, "destination": 1},
                     {"source": None, "destination": 1}]:
            a.add_communication(comm.get("source"), comm.get("destination"))
        path = a.find_shortest_path_from_internet(2)
        self.assertEqual(path[0], cids[0])
        self.assertEqual(path[1], cids[1])


class TestAppLogic(unittest.TestCase):
    def test_end_to_end(self):
        al = AppLogic()
        cids = list()
        for comp in ["comp1", "comp2", "comp3"]:
            cids.append(al.add_component(comp))
        for conn in [(None, cids[0]), (cids[0], cids[1]), (cids[1], cids[2])]:
            al.add_communication(conn[0], conn[1])
        path = al.get_flow(cids[2])
        self.assertEqual(path[0], cids[0])
        self.assertEqual(path[1], cids[1])
        self.assertEqual(path[2], cids[2])


class TestServer(unittest.TestCase):

    def test_post_component(self):
        cids = list()
        order_size = 10
        for comp in [f"comp{i}" for i in range(order_size)]:
            response = user.post_component(comp)
            response_obj = json.loads(response.content)
            self.assertEqual(200, response.status_code)
            self.assertEqual("success", response_obj["result"])
            cids.append(response_obj["componentId"])
        self.assertEqual(order_size, len(set(cids)))

    def test_post_communication(self):
        cids = list()
        for comp in ["comp1", "comp2"]:
            response = user.post_component(comp)
            response_obj = json.loads(response.content)
            cids.append(response_obj["componentId"])
        for conn in [(cids[0], cids[1]), (None, cids[0])]:
            response = user.post_communication(conn[0], conn[1])
            self.assertEqual(response.status_code, 200)
            response_obj = json.loads(response.content)
            self.assertEqual("success", response_obj["result"])

    def test_end_to_end(self):
        cids = list()
        # post components
        for comp in ["comp1", "comp2"]:
            response = user.post_component(comp)
            response_obj = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_obj["result"], "success", "Error in component post")
            cids.append(response_obj["componentId"])
        # post communications
        for conn in [(cids[0], cids[1]), (None, cids[0])]:
            response = user.post_communication(conn[0], conn[1])
            self.assertEqual(response.status_code, 200)
            response_obj = json.loads(response.content)
            self.assertEqual(response_obj["result"], "success", "Error in communications post")
        # get flow
        response = user.get_flow(cids[1])
        self.assertEqual(response.status_code, 200)
        response_obj = json.loads(response.content)
        self.assertEqual(response_obj["internetFacing"], True)
        self.assertEqual(response_obj["flow"], [cids[0], cids[1]])


class ServerNegativeTesting(unittest.TestCase):
    def test_invalid_arguments(self):
        for route in ["component", "communication"]:
            response = user.post(route, invalid_arg="value")
            self.assertEqual(400, response.status_code)
        response = user.get("flow", invalid_arg="value")
        self.assertEqual(400, response.status_code)

    def test_invalid_component(self):
        pass


if __name__ == '__main__':
    unittest.main()
