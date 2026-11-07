"""Giffler-Thompson style active-schedule generation for ta41."""

import random

from tasks.t056.check import N_JOBS, N_MACHINES, load_instance

OPERATIONS = load_instance()


def generate_active_schedule(seed=0, rule="spt", randomized=False):
    rng = random.Random(seed)
    job_next = [0] * N_JOBS
    job_ready = [0] * N_JOBS
    machine_ready = [0] * N_MACHINES
    orders = [[] for _ in range(N_MACHINES)]
    dispatched = 0
    while dispatched < N_JOBS * N_MACHINES:
        ready = []
        for job in range(N_JOBS):
            index = job_next[job]
            if index == N_MACHINES:
                continue
            machine, duration = OPERATIONS[job][index]
            start = max(job_ready[job], machine_ready[machine])
            ready.append((start, start + duration, duration, job, index, machine))
        chosen = min(ready, key=lambda x: (x[1], x[3], x[5]))
        _, completion, _, _, _, conflict_machine = chosen
        conflict = [op for op in ready
                    if op[5] == conflict_machine and op[0] < completion]
        if randomized:
            op = rng.choice(conflict)
        elif rule == "spt":
            op = min(conflict, key=lambda x: (x[2], x[1], x[3]))
        elif rule == "lpt":
            op = min(conflict, key=lambda x: (-x[2], x[1], x[3]))
        elif rule == "fifo":
            op = min(conflict, key=lambda x: (x[3], x[1]))
        elif rule == "random_priority":
            op = min(conflict, key=lambda x: (rng.random(), x[3]))
        else:
            raise ValueError("unknown dispatch rule")
        start, _, duration, job, index, machine = op
        orders[machine].append(job)
        finish = start + duration
        job_ready[job] = finish
        machine_ready[machine] = finish
        job_next[job] += 1
        dispatched += 1
    return orders
