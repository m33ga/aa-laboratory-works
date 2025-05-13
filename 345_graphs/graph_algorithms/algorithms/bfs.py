from collections import deque


def bfs(graph, num_nodes, start=0):  # index based
    visited = [False] * num_nodes
    queue = deque([start])
    visited[start] = True

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return [i for i, v in enumerate(visited) if v]
