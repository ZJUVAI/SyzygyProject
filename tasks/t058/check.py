"""Exact pair-conflict checker for the 35-player Social Golfer configuration."""


CONFIG_ID = "T058-C01"
PARAMETERS = {
    "players": 35,
    "groups_per_round": 7,
    "players_per_group": 5,
    "constraint": "each player appears once per round; each unordered pair shares a group at most once",
    "objective": "number of valid rounds",
}


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix 35 players in seven groups of five")


def validate(solution, config, strict=False):
    """Validate all rounds and count them; no candidate score is trusted."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    rounds = solution.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("rounds must be a nonempty list")
    if len(rounds) > 8:
        raise ValueError("more than eight rounds exceeds the pair-count upper bound")

    player_set = set(range(35))
    used_pairs = set()
    round_pair_counts = []
    for round_index, groups in enumerate(rounds, start=1):
        if not isinstance(groups, list) or len(groups) != 7:
            raise ValueError(f"round {round_index} must contain exactly seven groups")
        seen_players = set()
        pairs_this_round = 0
        for group_index, group in enumerate(groups, start=1):
            if not isinstance(group, list) or len(group) != 5:
                raise ValueError(f"round {round_index}, group {group_index} must contain exactly five players")
            if any(type(player) is not int or player not in player_set for player in group):
                raise ValueError(f"round {round_index}, group {group_index} has an invalid player ID")
            if len(set(group)) != 5:
                raise ValueError(f"round {round_index}, group {group_index} repeats a player")
            for player in group:
                if player in seen_players:
                    raise ValueError(f"player {player} appears in multiple groups in round {round_index}")
                seen_players.add(player)
            for offset, left in enumerate(group):
                for right in group[offset + 1:]:
                    pair = (left, right) if left < right else (right, left)
                    if pair in used_pairs:
                        raise ValueError(f"players {pair} meet more than once")
                    used_pairs.add(pair)
                    pairs_this_round += 1
        if seen_players != player_set:
            raise ValueError(f"round {round_index} must cover each player exactly once")
        round_pair_counts.append(pairs_this_round)

    return {
        "objective": len(rounds),
        "verification_status": "exact",
        "details": {
            "players": 35,
            "groups_per_round": 7,
            "players_per_group": 5,
            "round_count": len(rounds),
            "distinct_pairs_used": len(used_pairs),
            "pair_count_upper_bound": 8,
            "pairs_per_round": round_pair_counts,
            "claimed_objective_ignored": True,
        },
    }
