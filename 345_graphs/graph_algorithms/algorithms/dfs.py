def dfs(graph, num_nodes, start=0):
    visited = [False] * num_nodes
    stack = [start]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in reversed(graph.get(node, [])):
                if not visited[neighbor]:
                    stack.append(neighbor)
    return [i for i, v in enumerate(visited) if v]