import heapq


def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        curr_dist, u = heapq.heappop(heap)
        if curr_dist > dist[u]:
            continue
        for v, weight in graph[u]:
            new_dist = curr_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    return dist
