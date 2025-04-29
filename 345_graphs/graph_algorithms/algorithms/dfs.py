def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor, _ in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
