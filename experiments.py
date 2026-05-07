import os
import time
import statistics
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from algorithms import to_adj, bron_kerbosch, greedy, local_search


def run(fn, adj):
    t = time.time()
    C = fn(adj)
    return len(C), time.time() - t


ns = [20, 40, 60, 80]
ps = [0.1, 0.3, 0.5, 0.7, 0.9]
repeats = 5

q_greedy = {p: [] for p in ps}
q_ls = {p: [] for p in ps}
t_exact = {n: [] for n in ns}
t_ls = {n: [] for n in ns}
t_greedy = {n: [] for n in ns}

for n in ns:
    for p in ps:
        for r in range(repeats):
            seed = 1000 * n + int(100 * p) + r
            G = nx.erdos_renyi_graph(n, p, seed=seed)
            adj = to_adj(G)
            omega, te = run(bron_kerbosch, adj)
            ng, tg = run(greedy, adj)
            nl, tl = run(local_search, adj)
            t_exact[n].append(te)
            t_ls[n].append(tl)
            t_greedy[n].append(tg)
            if omega:
                q_greedy[p].append(ng / omega)
                q_ls[p].append(nl / omega)
            print(f"n={n} p={p} seed={seed} omega={omega} t={round(te, 3)} greedy={ng} ls={nl}")

print("Качество")
for p in ps:
    print(f"p={p} greedy={round(statistics.median(q_greedy[p]), 3)} ls={round(statistics.median(q_ls[p]), 3)}")

print("Время")
for n in ns:
    print(f"n={n} exact={round(statistics.median(t_exact[n]), 3)} ls={round(statistics.median(t_ls[n]), 3)} greedy={round(statistics.median(t_greedy[n]), 3)}")