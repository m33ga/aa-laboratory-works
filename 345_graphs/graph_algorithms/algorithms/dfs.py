def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            neighbors = [neighbor for neighbor, _ in graph.get(node, [])]
            stack.extend(reversed(neighbors))
    return visited
