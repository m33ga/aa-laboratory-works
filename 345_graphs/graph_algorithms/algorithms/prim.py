import heapq


def prim(graph):
    visited = set()
    mst = []
    start = next(iter(graph))
    visited.add(start)
    heap = [(weight, start, neighbor) for neighbor, weight in graph[start]]
    heapq.heapify(heap)

    while heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            for neighbor, w in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (w, v, neighbor))
    return mst
