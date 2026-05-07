def degeneracy_order(adj):
    deg = {v: len(adj[v]) for v in adj}
    order = []
    seen = set()
    while len(order) < len(adj):
        v = min((u for u in adj if u not in seen), key=lambda u: deg[u])
        order.append(v)
        seen.add(v)
        for u in adj[v]:
            if u not in seen:
                deg[u] -= 1
    return order


def bron_kerbosch(adj):
    best = [set()]

    def expand(R, P, X):
        if not P and not X:
            if len(R) > len(best[0]):
                best[0] = set(R)
            return
        if len(R) + len(P) <= len(best[0]):
            return
        u = max(P | X, key=lambda v: len(adj[v] & P))
        for v in list(P - adj[u]):
            expand(R | {v}, P & adj[v], X & adj[v])
            P = P - {v}
            X = X | {v}

    order = degeneracy_order(adj)
    for i, v in enumerate(order):
        later = set(order[i + 1:])
        earlier = set(order[:i])
        expand({v}, adj[v] & later, adj[v] & earlier)
    return best[0]


def greedy(adj):
    nodes = sorted(adj, key=lambda v: -len(adj[v]))
    C = set()
    for v in nodes:
        if all(v in adj[u] for u in C):
            C.add(v)
    return C


def local_search(adj):
    C = greedy(adj)
    while True:
        improved = False
        for v in list(C):
            rest = C - {v}
            if rest:
                common = set.intersection(*(adj[u] for u in rest)) - C
            else:
                common = set(adj) - C
            common = list(common)
            for i in range(len(common)):
                for j in range(i + 1, len(common)):
                    if common[j] in adj[common[i]]:
                        C = rest | {common[i], common[j]}
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
        if not improved:
            break
    return C


def to_adj(G):
    return {v: set(G.neighbors(v)) for v in G.nodes()}
