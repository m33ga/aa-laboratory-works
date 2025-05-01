def kruskal(graph):
    edges = []
    node_to_idx = {}
    idx = 0
    for u in graph:
        if u not in node_to_idx:
            node_to_idx[u] = idx
            idx += 1
        for v, w in graph[u].items():
            if v not in node_to_idx:
                node_to_idx[v] = idx
                idx += 1
            if u < v:
                edges.append((w, u, v))
    edges.sort()

    parent = list(range(idx))
    rank = [0] * idx

    def find(u_idx):
        while parent[u_idx] != u_idx:
            parent[u_idx] = parent[parent[u_idx]]
            u_idx = parent[u_idx]
        return u_idx

    def union(u_idx, v_idx):
        ru, rv = find(u_idx), find(v_idx)
        if ru == rv:
            return False
        if rank[ru] > rank[rv]:
            parent[rv] = ru
        else:
            parent[ru] = rv
            if rank[ru] == rank[rv]:
                rank[rv] += 1
        return True

    mst_edges = []
    total_weight = 0
    for w, u, v in edges:
        u_idx = node_to_idx[u]
        v_idx = node_to_idx[v]
        if union(u_idx, v_idx):
            mst_edges.append((u, v, w))
            total_weight += w

    return mst_edges, total_weight
