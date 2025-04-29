def kruskal(graph):
    parent = {}
    rank = {}

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    def union(u, v):
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        if rank[ru] > rank[rv]:
            parent[rv] = ru
        else:
            parent[ru] = rv
            if rank[ru] == rank[rv]:
                rank[rv] += 1
        return True

    edges = []
    for u in graph:
        for v, w in graph[u]:
            if u < v:
                edges.append((w, u, v))

    for node in graph:
        parent[node] = node
        rank[node] = 0

    mst = []
    for weight, u, v in sorted(edges):
        if union(u, v):
            mst.append((u, v, weight))
    return mst
