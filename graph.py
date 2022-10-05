class NodeNotFound(Exception):
    def __init__(self, node):
        super().__init__(f'Node {node} does not exist in the graph.')

class EdgeNotFound(Exception):
    def __init__(self, edge):
        super().__init__(f'Edge {edge} does not exist in the graph.')

class DuplicateNode(Exception):
    def __init__(self, node):
        super().__init__(f'Node {node} already exists in the graph.')

class DuplicateEdge(Exception):
    def __init__(self, edge):
        super().__init__(f'Edge {edge} already exists in the graph.')

class node:
    def __init__(self, label):
        """
        Parameter: a string indicating the label of the new node
        """
        self.label = label
        self.in_degree_val = 0
        self.out_degree_val = 0
        
    def in_degree(self):
        """
        Parameter: none
        Return value: integer representing the in-degree of 
        this node
        """
            
        return self.in_degree_val
    
    
    def update_in_degree(self, new_edge=0):
        """
        Parameter: none
        Return value: integer representing the in-degree of 
        this node
        """
        if new_edge == 1:
            self.in_degree_val += 1
        elif new_edge == -1:
            self.in_degree_val -= 1
            
        return self.in_degree_val
        
    
    def out_degree(self):
        """
        Parameter: none
        Return value: integer representing the out-degree of 
        this node
        """
        
        return self.out_degree_val
        
    
    def update_out_degree(self, new_edge=0):
        """
        Parameter: none
        Return value: integer representing the out-degree of 
        this node
        """
        if new_edge == 1:
            self.out_degree_val += 1
        elif new_edge == -1:
            self.out_degree_val -= 1
        return self.out_degree_val
    
    def __str__(self):
        """
        Parameter: none
        Return value: string label of the node
        """
        return self.label

class Graph:
    def __init__(self, directed=False):
        """
        Parameter: a boolean indicating whether the new instance 
        of Graph will be directed (True) or undirected (False)
        Post condition: new instance of an empty graph is 
        created
        """
        self.directed = directed
        self.num_vertices_val = 0
        self.num_edges_val = 0
        self.is_weighted_val = False
        self.graph = {}
        self.node_label_map = {}

    def set_graph(self, graph):
        self.graph = graph
        
    def num_vertices(self):
        """
        Parameters: none
        Return value: integer corresponding to the total number
        of vertices in the graph
        """
        
        return self.num_vertices_val
    
    def num_edges(self):
        """
        Parameters: none
        Return value: integer corresponding to the total number
        of edges in the graph
        """
        
        return self.num_edges_val
    
    def is_directed(self):
        """
        Parameters: none
        Return value: boolean - True if this instance of the 
        Graph class is a directed graph, False otherwise
        """
        
        return self.directed
    
    def is_weighted(self):
        """
        Parameters: none
        Return value: boolean - True if any edge in the Graph
        has a weight other than 1, False otherwise
        """
        
        return self.is_weighted_val

    def __check_node_exists(self, label):
        if label not in self.graph.keys():
            raise NodeNotFound(label)

    def __check_node_duplicate(self, label):
        if label in self.graph.keys():
            raise DuplicateNode(label)

    def add_node(self, label):
        """
        Parameter: a string indicating the label of a new node
        in the Graph
        Return value: none
        Assumptions: labels of nodes in the Graph must be unique
        """
        self.__check_node_duplicate(label)
        new_node = node(label)
        self.node_label_map[label] = new_node
        self.graph[label] = set()
        
        self.num_vertices_val += 1
        
        return new_node
    
    def remove_node(self, label):
        """
        Parameter: a string indicating the label of an existing
        node in the Graph
        Return value: none
        Post conditions: the node with the given label, as well 
        as any edges to/from that node, are removed from the 
        graph
        """
        self.__check_node_exists(label)
        node = self.node_label_map[label]
        adjacent_vertices = self.graph[label]
        
        for vertex in adjacent_vertices:
            self.graph[vertex].remove(label)
            vertex_node = self.node_label_map[vertex]
            ## TO do: In degree
            self.num_edges_val -= 1
        
        del self.graph[label]
        del self.node_label_map[label]
        self.num_vertices_val -= 1
        
    def __edge_exists(self, n1, n2):
        try:
            edges_n1 = self.graph[n1]
            if n2 in edges_n1:
                return True
            else:
                raise EdgeNotFound((n1, n2))
        except KeyError:
            raise NodeNotFound(n1)

    def __check_duplicate_edge(self, n1, n2):
        try:
            edges_n1 = self.graph[n1]
            if n2 in edges_n1:
                raise DuplicateEdge((n1, n2))
        except KeyError:
            raise NodeNotFound(n1)
    
    def add_edge(self, n1, n2, weight = 1):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes connected by the new edge. If this is a directed 
            Graph, then the edge will be FROM n1 TO n2.
            a numeric value (int/float) for a weight of the edge
        Return value: none
        Assumptions: the combination of (n1, n2, weight) must 
        be unique in the Graph
        Post conditions: one new edge is added to the Graph
        """
        self.__check_duplicate_edge(n1, n2)
        self.graph[n1].add(n2)
        node_n1 = self.node_label_map[n1]
        node_n2 = self.node_label_map[n2]
        node_n1.update_out_degree(1)
        node_n2.update_in_degree(1)
        
        if not self.directed:
            self.graph[n2].add(n1)
            node_n2.update_out_degree(1)
            node_n1.update_in_degree(1)
            
        self.num_edges_val += 1
        
    
    def remove_edge(self, n1, n2, weight = 1):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes connected by the edge. If this is a directed 
            Graph, then the edge will be FROM n1 TO n2.
            a numeric value (int/float) for a weight of the edge
        Return value: none
        Post conditions: the edge with the given nodes and weight
        is removed from the graph
        """
        self.__edge_exists(n1, n2)
        self.graph[n1].remove(n2)
        node_n1 = self.node_label_map[n1]
        node_n2 = self.node_label_map[n2]
        node_n1.update_out_degree(-1)
        node_n2.update_in_degree(-1)
        
        if not self.directed:
            self.graph[n2].remove(n1)
            node_n2.update_out_degree(-1)
            node_n1.update_in_degree(-1)
            
        self.num_edges_val -= 1
    
    def BFS(self, source):
        """
        Parameter: a string indicating the label of an existing 
        node in the Graph
        Return value: a list of node objects, which is the 
        Breadth First Search starting at source
        """
        
        visited_dict = {}
        result_list = []
        def do_bfs(source):
            result_list = []
            queue = [source]

            while queue:
                print(queue)
                current_node = queue.pop(0)
                visited_dict[current_node] = True
                result_list.append(current_node)
                for neighbor in self.graph[current_node]:
                    if not visited_dict.get(neighbor, False) and neighbor not in queue:
                        queue.append(neighbor)
            
            return result_list
        
        result_list = do_bfs(source)
        # for node in self.graph.keys():
        #     if not visited_dict.get(node, False):
        #         result_list += do_bfs(node)

        return result_list
        
    def DFS(self, source):
        """
        Parameter: a string indicating the label of an existing 
        node in the Graph
        Return value: a list of node objects, which is the 
        Depth First Search starting at source
        """
        visited_dict = {}
        result_list = []
        for node in self.graph.keys():
            visited_dict[node] = False
        
        def do_dfs(current_node):
            if visited_dict[current_node]:
                return
            visited_dict[current_node] = True
            for neighbour_node in self.graph[current_node]:
                do_dfs(neighbour_node)
            result_list.append(current_node)
        
        do_dfs(source)
        for node in visited_dict.keys():
            if not visited_dict[node]:
                do_dfs(node)
        
        return result_list
    
    def has_edge(self, n1, n2):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes connected by the new edge. If this is a directed 
            Graph, then the edge will be FROM n1 TO n2.
        Return value: a boolean - True if there is an edge in the 
            Graph from n1 to n2, False otherwise
        """
        self.__check_node_exists(n1)
        self.__check_node_exists(n2)
        if n2 in self.graph.get(n1):
            return True
        else:
            return False
    
    def get_path(self, n1, n2):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes you wish to find a path between. The path will be
            FROM n1 TO n2.
        Return value: a list L of node objects such that L[0] has 
            label n1, L[-1] has label n2, and for 1 <= i <= len(L) - 1,
            the Graph has an edge from L[i-1] to L[i]
        """
        self.__check_node_exists(n1)
        self.__check_node_exists(n2)
        visited_dict = {}
        result_list = []
        for node in self.graph.keys():
            visited_dict[node] = False
        
        def do_bfs(current_node, result_list):
            if visited_dict[current_node]:
                return result_list
            if current_node == n2:
                result_list.append(current_node)
                return result_list
            visited_dict[current_node] = True
            result_list.append(current_node)
            for neighbour_node in self.graph[current_node]:
                result_list = do_bfs(neighbour_node, result_list)
                if n2 in result_list:
                    break
                    
            return result_list
        
        result_list = do_bfs(n1, result_list)
        
        return result_list
        pass

    
    def get_adjacent_nodes(self, label):
        """
        Parameter: a string indicating the label of an existing 
        node in the Graph
        Return value: a list of node objects containing all nodes
        adjacent to the node with the given label
        """
        self.__check_node_exists(label)
        return list(self.graph[label])
    
    def random_return(self):
        return self.graph