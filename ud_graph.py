# Course: 
# Author: 
# Assignment: 
# Description:


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list:
            return
        self.adj_list[v] = []
        return
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph. U is the edge, V is the vertex
        """
        if u == v:
            return

        if u in self.adj_list:
            if v in self.adj_list:
            # Vertex exists
                #If the vertex edge exists return
                if u in self.adj_list[v]:
                    return
                #If edge does not exist, add
                else:
                    self.adj_list[v].append(u)
                #Making sure the edge exists for the other vertex
                if v in self.adj_list[u]:
                    return
                else:
                    #Adding the vertex (now edge) to the new vertex
                    self.add_edge(v,u)
            else:
                self.add_vertex(v)
                self.add_edge(u,v)
        else:
            # Vertex does not exist so add
            self.add_vertex(u)
            self.add_edge(u, v)


        return
        

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph. U is the egde, V is the vertex
        """
        if v in self.adj_list and u in self.adj_list[v]:
            #Making sure to delete edge from both vertices
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)
        else:
            return
        

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            self.adj_list.pop(v,None)
            for i in self.adj_list:
                if v in self.adj_list[i]:
                    self.adj_list[i].remove(v)
        return

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        list = []
        for i in self.adj_list:
            list.append(i)
        return list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        list = []
        for i in self.adj_list:
            for j in range(0,len(self.adj_list[i])):
                if [i,self.adj_list[i][j]] not in list:
                    if [self.adj_list[i][j],i] not in list:
                        list.append([i,self.adj_list[i][j]])
        return list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if path == []:
            return True
        elif len(path) == 1 and path[0] in self.get_vertices():
            return True

        compare = self.get_edges()
        boolean = False
        for i in range(1,len(path)):
            if [path[i-1],path[i]] in compare or [path[i],path[i-1]] in compare:
                boolean = True
            else:
                boolean = False
                return boolean
        return boolean

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        list = []
        stack = []
        stack.append(v_start)
        if v_start not in self.adj_list:
            return list
        while len(stack) > 0:
            pop = stack.pop()
            if pop not in list:
                list.append(pop)
                if v_end is not None:
                    if pop == v_end:
                        break
                path = sorted(self.adj_list[pop],reverse=True)
                for i in path:
                    if i not in list:
                        stack.append(i)
        return list


       

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        list = []
        queue = []
        queue.append(v_start)
        if v_start not in self.adj_list:
            return list
        while len(queue) > 0:
            pop = queue.pop(0)
            if pop not in list:
                list.append(pop)
                if v_end is not None:
                    if pop == v_end:
                        break
                path = sorted(self.adj_list[pop])
                for i in path:
                    if i not in list:
                        queue.append(i)
        return list

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        visited = []
        traversed = []
        count = 0
        for i in self.adj_list:
            if i not in visited and i not in traversed:
                traversed = self.dfs(i)
                for j in traversed:
                    visited.append(j)
                count += 1
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        j = 0
        current = dict()

        for i in self.adj_list:
            current[i] = j
            j += 1

        #We are going to go with every node until we find a cylce
        for i in self.adj_list:
            #We are keeping track of which node we are trying to return to
            parent = [-1] * len(self.adj_list)

            #Creating an array of non visited nodes
            visited = [False] * len(self.adj_list)

            #Currently we visited our node i
            visited[current[i]] = True

            #BFS method cuz first value and we out
            queue = []
            queue.append(i)

            while queue != []:
                #Starting node
                u = queue.pop(0)

                #Looking at edges
                for v in self.adj_list[u]:

                    #If the current edge hasn't been visited enter if statement
                    if not visited[current[v]]:
                        #Add to our visited
                        visited[current[v]] = True
                        queue.append(v)
                        #Second tracker of visit
                        parent[current[v]] = u
                    #If parent did equal v, it would mean we were going back but
                    #with the same route we already traversed
                    elif parent[current[u]] != v:
                        return True

        return False
       

   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
