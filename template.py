"""MaxCut via annealing — same 4-node ring graph as the live
qaoa-maxcut template, solved through the QUBO/annealing lane instead
of gate-based QAOA (dimod simulated annealing runs server-side; this
template only emits the QUBO).

QUBO: maximise cut(x) = sum over edges (i,j) of x_i + x_j - 2*x_i*x_j.
Annealing minimises energy, so we emit Q = -cut:
    Q[i][i] -= 1 per incident edge, Q[i][j] += 2 per edge.
Best energy == -(cut size), so for the default 4-cycle the optimum
is energy -4 (cut of all 4 edges: alternating partition 0101/1010).

Sandbox: no imports — pure dict construction on Python built-ins.
See vortex_common.algorithm_executor.validate_template_ast.
"""

_DEFAULT_EDGES = [[0, 1], [1, 2], [2, 3], [3, 0]]


class AlgorithmTemplate:

    def build(self, input_data, ctx):
        backend = ctx.get("backend", "auto") if isinstance(ctx, dict) else "auto"
        edges = _normalize_edges(input_data.get("edges", _DEFAULT_EDGES))
        return {
            "type": "annealing",
            "backend_id": backend if backend != "auto" else "vortex-annealing-sim",
            "provider": "vortex",
            "annealing_config": {
                "problem_type": "qubo",
                "qubo": _maxcut_to_qubo(edges),
                "num_reads": input_data.get("num_reads", 1000),
            },
        }

    def interpret(self, raw_result, input_data):
        result = raw_result if isinstance(raw_result, dict) else {}
        edges = _normalize_edges(input_data.get("edges", _DEFAULT_EDGES))
        num_nodes = _num_nodes(edges)
        sample = result.get("best_sample", {})

        # Decode the partition: node -> side 0 or side 1
        partition = {}
        for node in range(num_nodes):
            partition[str(node)] = 1 if sample.get(str(node), 0) == 1 else 0

        # Count edges actually cut by this assignment (honest re-check —
        # derived from the sample itself, not from the reported energy)
        cut_edges = []
        for i, j in edges:
            if partition[str(i)] != partition[str(j)]:
                cut_edges.append([i, j])
        cut_size = len(cut_edges)

        side_0 = sorted(int(n) for n, s in partition.items() if s == 0)
        side_1 = sorted(int(n) for n, s in partition.items() if s == 1)

        return {
            "partition": partition,
            "side_0": side_0,
            "side_1": side_1,
            "cut_edges": cut_edges,
            "cut_size": cut_size,
            # Honest comparison: total edge count is a trivial upper bound
            # on the max cut; reaching it is only possible for bipartite
            # graphs (the default 4-cycle is bipartite, so best = 4).
            "num_edges": len(edges),
            "cut_fraction": cut_size / len(edges) if edges else 0.0,
            "note": (
                "cut_size is recomputed from the best sample; num_edges is "
                "an upper bound on the max cut (achievable only if the "
                "graph is bipartite)."
            ),
            "best_energy": result.get("best_energy"),
            "total_reads": result.get("total_reads", 0),
        }


def _normalize_edges(edges):
    """Coerce edges to a deduplicated list of [min, max] int pairs."""
    seen = set()
    clean = []
    for pair in edges:
        i = int(pair[0])
        j = int(pair[1])
        if i == j or i < 0 or j < 0:
            continue
        key = (min(i, j), max(i, j))
        if key in seen:
            continue
        seen.add(key)
        clean.append([key[0], key[1]])
    return clean


def _num_nodes(edges):
    highest = -1
    for i, j in edges:
        highest = max(highest, i, j)
    return highest + 1


def _maxcut_to_qubo(edges):
    """MaxCut QUBO with '(i,j)' string keys (i <= j).

    Minimising this QUBO maximises the cut: energy == -(cut size).
    """
    qubo = {}
    for i, j in edges:
        ki = f"({i},{i})"
        kj = f"({j},{j})"
        kij = f"({i},{j})"
        qubo[ki] = qubo.get(ki, 0.0) - 1.0
        qubo[kj] = qubo.get(kj, 0.0) - 1.0
        qubo[kij] = qubo.get(kij, 0.0) + 2.0
    return qubo
