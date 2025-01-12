import networkx as nx


def edge_presentation(graph):
    edges = []
    root = find_root(graph)
    for u, v in nx.dfs_edges(graph, source=root):
        if graph.has_edge(u, v):
            weight = graph[u][v].get("weight", None)
            edge_str = f"{u} -({weight})-> {v}" if weight is not None else f"{u} -> {v}"
            edges.append(edge_str)
    if len(edges) == 0:
        return "No edges"
    return ', '.join(edges)



def find_root(graph):
    for node in graph.nodes:
        if graph.in_degree(node) == 0:
            return node
    return None


def hierarchy_presentation(graph, node=None, prefix="", visited=None, is_last=True, is_root=True):
    if visited is None:
        visited = set()  # Initialize a set to track visited nodes

    if node is None:
        node = find_root(graph)
        if node is None:
            raise ValueError("The graph has no root; it may not be a valid tree.")

    # If the node has already been visited, mark it as a duplicate
    if node in visited:
        # return f"{prefix}{'`-- ' if not is_root else ''}{node} (duplicate)\n"
        return ""

    # Mark the current node as visited
    visited.add(node)

    # Build the current node's representation
    result = f"{prefix}{'   ' if is_root else ('`-- ' if is_last else '|-- ')}{node}\n"

    # Get children of the current node
    children = list(graph.successors(node))
    for i, child in enumerate(children):
        child_is_last = (i == len(children) - 1)
        # Adjust the prefix for the child nodes
        child_prefix = prefix + ("    " if is_last else "|   ")
        # Recursively process child nodes
        result += hierarchy_presentation(graph, node=child, prefix=child_prefix, visited=visited, is_last=child_is_last, is_root=False)
    
    return result
