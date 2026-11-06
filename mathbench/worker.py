"""Separate child process for generation or trusted checking."""
import contextlib
import importlib.util
import json
import os
from pathlib import Path
import random
import resource
import sys


def load(path):
    path = Path(path).resolve()
    sys.path.insert(0, str(path.parent))
    root = Path(__file__).resolve().parents[1]
    try:
        relative = path.relative_to(root / "tasks")
        name = "tasks." + ".".join(relative.with_suffix("").parts)
    except ValueError:
        name = "mathbench_child_module"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def set_limits(memory, cpu):
    # macOS does not provide the Linux address-space limit used by this runner.
    if sys.platform != "darwin":
        resource.setrlimit(resource.RLIMIT_AS, (int(memory), int(memory)))
    resource.setrlimit(resource.RLIMIT_CPU, (int(cpu), int(cpu) + 1))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    if hasattr(os, "sched_getaffinity"):
        os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})


def main():
    mode, module_path, config_path, output_path, seed, strict, memory, cpu = sys.argv[1:]
    set_limits(memory, cpu)
    config = json.loads(Path(config_path).read_text())
    os.environ["MATHBENCH_CONFIG_ID"] = config["id"]
    os.environ["MATHBENCH_SEED"] = seed
    os.environ["MATHBENCH_STRICT"] = strict
    random.seed(int(seed))
    # Candidate diagnostics cannot corrupt the result channel.
    with open(os.devnull, "w") as quiet, contextlib.redirect_stdout(quiet), contextlib.redirect_stderr(quiet):
        import numpy as np
        np.random.seed(int(seed) % 2**32)
        module = load(module_path)
        if mode == "generate":
            result = module.run_code()
        else:
            solution = json.loads(Path(os.environ["MATHBENCH_SOLUTION_PATH"]).read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite JSON")))
            result = module.validate(solution, config, strict=(strict == "1"))
    def convert(value):
        if hasattr(value, "tolist"):
            return value.tolist()
        if isinstance(value, set):
            return sorted(value)
        raise TypeError("Return JSON data, not executable objects")
    payload = json.dumps(result, default=convert, allow_nan=False)
    if len(payload.encode()) > 16 * 1024 * 1024:
        raise ValueError("Result exceeds 16 MiB")
    Path(output_path).write_text(payload)


if __name__ == "__main__":
    main()
