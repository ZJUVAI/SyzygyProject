"""Exact checker for Taillard ta41 job-shop machine orders."""

from collections import deque
import json
from pathlib import Path

N_JOBS = 30
N_MACHINES = 20
INSTANCE = "ta41"
PARAMETERS = {"instance": INSTANCE, "jobs": N_JOBS, "machines": N_MACHINES}
_INSTANCE_PATH = Path(__file__).resolve().parent / "data/source/ta41_instance.json"


def load_instance():
    data = json.loads(_INSTANCE_PATH.read_text(encoding="utf-8"))
    if (data.get("instance"), data.get("jobs"), data.get("machines")) != (
        INSTANCE, N_JOBS, N_MACHINES
    ):
        raise RuntimeError("bad pinned instance data")
    operations = data.get("operations")
    if not isinstance(operations, list) or len(operations) != N_JOBS:
        raise RuntimeError("bad operation table")
    for job in operations:
        if not isinstance(job, list) or len(job) != N_MACHINES:
            raise RuntimeError("bad job route")
        for op in job:
            if (not isinstance(op, list) or len(op) != 2 or
                    type(op[0]) is not int or type(op[1]) is not int or
                    not 0 <= op[0] < N_MACHINES or op[1] <= 0):
                raise RuntimeError("bad operation entry")
        if sorted(op[0] for op in job) != list(range(N_MACHINES)):
            raise RuntimeError("every job must visit each machine exactly once")
    return operations


def _topology(machine_orders, operations):
    n = N_JOBS * N_MACHINES
    durations = [0] * n
    predecessors = [[] for _ in range(n)]
    successors = [[] for _ in range(n)]

    def node(job, index):
        return job * N_MACHINES + index

    job_op_for_machine = [[-1] * N_MACHINES for _ in range(N_JOBS)]
    for j, route in enumerate(operations):
        for k, (machine, duration) in enumerate(route):
            durations[node(j, k)] = duration
            job_op_for_machine[j][machine] = k
            if k:
                a, b = node(j, k - 1), node(j, k)
                successors[a].append(b)
                predecessors[b].append(a)

    machine_loads = []
    for machine, order in enumerate(machine_orders):
        machine_loads.append(sum(operations[j][job_op_for_machine[j][machine]][1]
                                 for j in range(N_JOBS)))
        for first, second in zip(order, order[1:]):
            a = node(first, job_op_for_machine[first][machine])
            b = node(second, job_op_for_machine[second][machine])
            successors[a].append(b)
            predecessors[b].append(a)

    indegree = [len(row) for row in predecessors]
    ready = deque(i for i, value in enumerate(indegree) if value == 0)
    starts = [0] * n
    finishes = [0] * n
    visited = 0
    while ready:
        current = ready.popleft()
        finishes[current] = starts[current] + durations[current]
        visited += 1
        for nxt in successors[current]:
            if finishes[current] > starts[nxt]:
                starts[nxt] = finishes[current]
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    if visited != n:
        raise ValueError("machine orders create a precedence cycle")
    job_loads = [sum(duration for _, duration in route) for route in operations]
    objective = max(finishes)
    return objective, starts, finishes, machine_loads, job_loads


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "machine_orders" not in solution:
        raise ValueError("solution must contain machine_orders")
    machine_orders = solution["machine_orders"]
    if not isinstance(machine_orders, list) or len(machine_orders) != N_MACHINES:
        raise ValueError("machine_orders must contain one sequence per machine")
    expected = list(range(N_JOBS))
    for order in machine_orders:
        if not isinstance(order, list) or len(order) != N_JOBS:
            raise ValueError("every machine sequence must contain all 30 jobs")
        if any(type(job) is not int or job < 0 or job >= N_JOBS for job in order):
            raise ValueError("machine sequence contains an invalid job index")
        if sorted(order) != expected:
            raise ValueError("each machine sequence must be a permutation of all jobs")
    operations = load_instance()
    objective, starts, finishes, machine_loads, job_loads = _topology(machine_orders, operations)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "instance": INSTANCE,
            "jobs": N_JOBS,
            "machines": N_MACHINES,
            "operations": N_JOBS * N_MACHINES,
            "makespan": objective,
            "critical_path_lower_bound": max(max(machine_loads), max(job_loads)),
            "machine_loads": machine_loads,
            "job_loads": job_loads,
            "claimed_objective_ignored": True,
        },
    }
