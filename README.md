# MaxCut (Annealing)

> Solve MaxCut graph partitioning via quantum/simulated annealing. Same problem as qaoa-maxcut but uses annealing instead of gate-based QAOA. Compare results across paradigms: gate-based (QAOA) vs annealing on the same graph. QUBO formulation: Q_{ij} = -w for cut edges.

## At a glance

| | |
|---|---|
| Slug | `annealing-maxcut` |
| Qubits | 3 |
| Industries | foundational |
| Techniques | annealing |
| Difficulty | intermediate |
| Computation model | annealing |
| Access | `open` |
| License | Apache-2.0 |

## Circuit

_Coming soon — runnable implementation pending._

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
