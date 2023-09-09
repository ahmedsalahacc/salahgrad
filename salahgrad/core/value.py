"""Implements the value class and its operations"""
import networkx as nx

import numpy as np

import matplotlib.pyplot as plt


class Value:
    """Value class"""

    def __init__(self, data, _children=[], _op=""):
        self.data = data
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data})"

    def __add__(self, other):
        return Value(self.data + other.data, (self, other), _op="+")

    def __sub__(self, other):
        return Value(self.data - other.data, (self, other), _op="-")

    def __mul__(self, other):
        return Value(self.data * other.data, (self, other), _op="*")

    def __truediv__(self, other):
        return Value(self.data / other.data, (self, other), _op="/")

    def __pow__(self, other):
        assert isinstance(
            other, (int, float, np.int64, np.float64, Value)
        ), "Power must be a number"
        if isinstance(other, Value):
            return Value(self.data**other.data, (self, other), _op="**")
        return Value(self.data**other, (self, other), _op="**")

    def visualise(self) -> None:
        """Visualise the value graph"""
        nodes = set()
        edges = set()

        def get_nodes_and_edges(value):
            if value not in nodes:
                nodes.add(value)
                if not isinstance(value, Value):
                    return
                for child in value._prev:
                    edges.add((child, value))
                    get_nodes_and_edges(child)

        get_nodes_and_edges(self)

        G = nx.DiGraph()

        # add nodes
        for node in nodes:
            # add nodes with square shape
            G.add_node(node, shape="box")

        # add edges
        for edge in edges:
            op = edge[1]._op
            G.add_node(op, shape="circle")
            G.add_edge(edge[0], op)
            G.add_edge(op, edge[1])

        # visualise the graph
        # use spring_layout
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_cmap=plt.cm.Blues)
        plt.show()


if __name__ == "__main__":
    a = Value(1)
    b = Value(2)
    c = a + b**2
    (c / (c**0.5)).visualise()
