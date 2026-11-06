# Search-system integration

The task evaluator has the `evaluate(program_path) -> dict` interface used by SimpleTES and DREAM-RSI.
Install this project in the Python environment that runs the external evaluator. Use a matching task's instruction, seed, and configuration.

SimpleTES example:

```sh
python main.py --init-program /path/to/SyzygyProject/tasks/t073/init_program.py --evaluator /path/to/SyzygyProject/examples/simpletes_evaluator.py --instruction /path/to/SyzygyProject/tasks/t073/instruction.txt --model YOUR_MODEL --max-generations 5
```

For DREAM-RSI, pass `tasks/t005/instruction.txt`, `tasks/t005/init_program.py`, and `examples/dream_rsi_evaluator.py` to the external launcher's `--problem`, `--init-program`, and `--evaluator` options. Set `MATHBENCH_CONFIG_ID=T005-C02` when preparing the instruction. The adapter selects the same configuration for generation and checking.

The adapter preserves raw objectives. Its compatibility score uses this project's frozen human baseline. It does not reproduce the upstream paper's score normalization or use candidate-reported scores.

The local smoke test calls both adapter interfaces without a language-model service. Full external search runs need the chosen upstream version and model credentials; they are outside the first release.

Run the two interface checks with `.venv/bin/python -m pytest tests/test_integration.py -q -k upstream_interface`.
Both example adapters request strict verification. Their local smoke checks exercise the public evaluator signature and the returned scalar feedback. They do not run the upstream orchestration engines.

Interface sources checked 2026-11-04: [SimpleTES task guide](https://github.com/wq-will/SimpleTES/blob/main/datasets/README.md), [DREAM-RSI task guide](https://github.com/google-research/dream-rsi/blob/main/tasks/README.md). The [AlphaEvolve problem repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems) informed the separation of prompts, starter code, verification, and reproduced constructions. This package supplies its own strict checkers and normalization.
