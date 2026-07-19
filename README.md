# MaxCut (Annealing)

> Solve MaxCut graph partitioning via quantum/simulated annealing. Same problem as qaoa-maxcut but uses annealing instead of gate-based QAOA. Compare results across paradigms: gate-based (QAOA) vs annealing on the same graph. QUBO formulation: Q_{ij} = -w for cut edges.

## At a glance

| | |
|---|---|
| Slug | `annealing-maxcut` |
| Qubits | 4 |
| Industries | foundational |
| Techniques | annealing |
| Difficulty | intermediate |
| Computation model | annealing |
| Access | `open` |
| License | Apache-2.0 |

## How it works

No circuit — this is an annealing algorithm. `template.py` emits a QUBO with
energy = −(cut size): for each edge (i,j), `Q[i][i] -= 1`, `Q[j][j] -= 1`,
`Q[i][j] += 2`. Simulated annealing (dimod, server-side on
`vortex-annealing-sim`) minimises the energy, i.e. maximises the cut.

**Default instance**: the same 4-node ring as the live `qaoa-maxcut` template
(edges `[[0,1],[1,2],[2,3],[3,0]]`) so results can be compared across
paradigms. The ring is bipartite, so the optimum cuts all 4 edges
(best energy −4, partition `0101`/`1010`).

**Inputs** (all optional — `{}` runs the demo):

- `edges`: list of `[i, j]` pairs (custom graph)
- `num_reads`: annealing samples (default 1000)

**Output**: `partition`, `side_0`/`side_1`, `cut_edges`, `cut_size`,
`num_edges` (a trivial upper bound on the max cut — reachable only for
bipartite graphs), `cut_fraction`, `best_energy`, `total_reads`. The cut is
recomputed from the best sample, not inferred from the reported energy.

## How to run

### Python SDK

```python
from openqc import OpenQC

qc = OpenQC(api_key="oqc_...")           # see openqc.io → Settings → API Keys
result = qc.algorithm.run("annealing-maxcut", input_data={})
print(result)
```

`input_data` is required (use `{}` if the algorithm takes no parameters).
`run()` polls until the job completes; pass `wait=False` to return the job id immediately.

### HTTP API

```bash
curl -X POST https://openqc.io/v1/jobs/algorithms/annealing-maxcut/run \
  -H "Authorization: Bearer $OPENQC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input_data": {}, "backend": "auto"}'
```

Returns a job id; poll `GET /v1/jobs/{job_id}` until `status=completed`.

### CLI

A dedicated `openqc algorithm run ...` command is on the roadmap (Phase 9). Until then, use the SDK or HTTP examples above.

## References

- https://doi.org/10.1126/science.1057726

---
Maintained by the OpenQC team. See [CONTRIBUTING.md](https://github.com/openqc-io/algorithms-index/blob/main/CONTRIBUTING.md) for how to propose changes.
