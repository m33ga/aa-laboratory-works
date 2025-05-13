import heapq


def dijkstra(graph, start=0):
    dist = {node: float('inf') for node in graph}
    prev = {node: -1 for node in graph}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        curr_dist, u = heapq.heappop(heap)
        if curr_dist > dist[u]:
            continue
        for v, weight in graph.get(u, {}).items():
            new_dist = curr_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))
    return dist, prev
