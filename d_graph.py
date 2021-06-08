# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:
import heapq
class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a vertex to the weighted graph
        """
        self.v_count = self.v_count + 1

        if self.v_count == 1:
            self.adj_matrix.append([0])
            return self.v_count

        self.adj_matrix.append([0]*self.v_count)
        temp = 0

        for i in range(0,self.v_count-1):
            self.adj_matrix[i].append(temp)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a weighted edge between 2 vertices
        """
        if src == dst:
            return
        elif src > self.v_count-1:
            return
        elif dst > self.v_count-1:
            return
        elif weight < 0:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes the edge between specified vertex
        """
        if src == dst:
            return
        elif src > self.v_count-1 or src < 0:
            return
        elif dst > self.v_count-1 or dst < 0:
            return
        elif self.adj_matrix[src][dst] < 0:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns the vertices in the graph
        """
        list = []
        for i in range(0,self.v_count):
            list.append(i)
        return list

    def get_edges(self) -> []:
        """
        Returns the  edges of vertex with their weights
        """
        list = []
        for i in range(0,self.v_count):
            for j in range(0,self.v_count):
                if self.adj_matrix[i][j] > 0:
                    list.append((i,j,self.adj_matrix[i][j]))
        return list

    def is_valid_path(self, path: []) -> bool:
        """
        Returns true for valid paths and false for invalid paths
        """
        if len(path) == 0 or (len(path) == 1 and path[0] < self.v_count-1):
            return True
        for i in range(1,len(path)):
            if self.adj_matrix[path[i-1]][path[i]] == 0:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Depth First Search
        """
        list = []
        stack = []
        stack.append(v_start)

        #means the vertex is not in our matrix
        if v_start > self.v_count-1:
            return list

        while len(stack) > 0:
            pop = stack.pop()
            if pop not in list:
                list.append(pop)

                #Ending with the loop
                if v_end is not None:
                    if pop == v_end:
                        break

                path = self.adj_matrix[pop]
                actual_path = []
                for i in range(0,self.v_count):
                    if path[i] != 0:
                        actual_path.append(i)
                for i in range(len(actual_path)-1,-1,-1):
                    if actual_path[i] not in list:
                        stack.append(actual_path[i])
        return list

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        list = []
        queue = []
        queue.append(v_start)

        # means the vertex is not in our matrix
        if v_start > self.v_count - 1:
            return list

        while len(queue) > 0:
            pop = queue.pop(0)
            if pop not in list:
                list.append(pop)

                # Ending with the loop
                if v_end is not None:
                    if pop == v_end:
                        break

                path = self.adj_matrix[pop]
                actual_path = []
                for i in range(0, self.v_count):
                    if path[i] != 0:
                        actual_path.append(i)
                for i in range(0,len(actual_path)):
                    if actual_path[i] not in list:
                        queue.append(actual_path[i])
        return list

    def has_cycle(self):
        """
        Detects a cycle in the graph
        """
        def isCyclicUtil(node, visited, recStack,matrix):
            visited[node] = True
            # recStack[node] = node

            inner = []
            for i in range(0,len(matrix)):
                if matrix[node][i] != 0:
                    inner.append(i)

            for neighbor in range(0,len(inner)):
                if visited[inner[neighbor]] == False:
                    if isCyclicUtil(inner[neighbor], visited, recStack,matrix) == True:
                        return True
                elif recStack == inner[neighbor]:
                    return True

        for node in range(0,self.v_count):
            visited = [False] * (self.v_count)
            recStack = node

            if visited[node] == False:
                if isCyclicUtil(node, visited, recStack,self.adj_matrix) == True:
                    return True
        return False

    def dijkstra(self, src: int) -> []:
        """
        Returns the shortest path from Src node to all other nodes
        """
        visited = [False] * self.v_count
        distances = [float('inf')] * self.v_count
        distances[src] = 0

        heap = []
        heap.append([0,src])
        while len(heap) > 0:
            pop = heapq.heappop(heap)
            node = pop[1]
            row = self.adj_matrix[node]

            for i in range(0, self.v_count):
                if row[i] != 0:
                    # Making sure we take the shortest path
                    if visited[i]:
                        compare = row[i] + distances[node]
                        distances[i] = min(distances[i], compare)
                    else:
                        distances[i] = row[i] + distances[node]
                        heapq.heappush(heap, [distances[i], i])
            visited[node] = True

        return distances








if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
