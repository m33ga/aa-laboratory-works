import heapq


def prim(graph, num_nodes, start=0):
    if num_nodes == 0:
        return [], 0

    visited = [False] * num_nodes
    mst_edges = []
    total_cost = 0

    heap = []
    visited[start] = True

    for neighbor, weight in graph.get(start, {}).items():
        if not visited[neighbor]:
            heapq.heappush(heap, (weight, start, neighbor))

    while heap and len(mst_edges) < num_nodes - 1:
        weight, u, v = heapq.heappop(heap)
        if not visited[v]:
            visited[v] = True
            mst_edges.append((u, v, weight))
            total_cost += weight

            for neighbor, w in graph.get(v, {}).items():
                if not visited[neighbor]:
                    heapq.heappush(heap, (w, v, neighbor))

    return mst_edges, total_cost
