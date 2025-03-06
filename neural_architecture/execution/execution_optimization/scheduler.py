import networkx as nx
import logging

class PhiScheduler:
    def __init__(self):
        """Initialize execution graph for optimized scheduling."""
        self.execution_graph = nx.DiGraph()

    def optimize(self, input_data):
        """Optimize execution order using Φ(a) scheduling."""
        self._build_execution_graph(input_data)
        optimized_path = list(nx.topological_sort(self.execution_graph))
        logging.info(f"Optimized Execution Path: {optimized_path}")
        return optimized_path

    def _build_execution_graph(self, input_data):
        """Construct execution dependency graph dynamically."""
        self.execution_graph.clear()
        self.execution_graph.add_node("start")
        
        for key in input_data.keys():
            self.execution_graph.add_node(key)
            self.execution_graph.add_edge("start", key)

        self.execution_graph.add_edge(key, "end")
