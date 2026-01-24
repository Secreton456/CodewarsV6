import inspect
from config import TEAM_MODULES, EXPECTED_VARIABLES, EXPECTED_CLASSES, DEBUG
from game import Game


def validate_module(module, idx):
    name = f"TEAM {idx+1}"
    attributes = dir(module)

    # Variables
    variables = {
        attr for attr in attributes
        if not callable(getattr(module, attr))
        and not attr.startswith("__")
        and not inspect.ismodule(getattr(module, attr))
        and not inspect.isclass(getattr(module, attr))
    }

    # Classes
    classes = {
        attr for attr in attributes
        if inspect.isclass(getattr(module, attr))
    }

    if variables != EXPECTED_VARIABLES:
        print(f"[FAIL] {name}: Variables mismatch. Found: {variables}")
        return False

    if classes != EXPECTED_CLASSES:
        print(f"[FAIL] {name}: Classes mismatch. Found: {classes}")
        return False

    if len(module.troops) != len(set(module.troops)):
        print(f"[FAIL] {name}: troops must be unique")
        return False

    if DEBUG:
        print(f"[PASS] {name}: {module.team_name}")

    return True


def main():
    valid_teams = []

    for i, module in enumerate(TEAM_MODULES):
        if validate_module(module, i):
            valid_teams.append(module)
        else:
            print(f"[ERROR] Team {i+1} failed validation. Exiting.")
            return

    # Extract data for engine
    team_names = [t.team_name for t in valid_teams]
    team_troops = [t.troops for t in valid_teams]

    # Run game
    Game(team_troops, team_names).run()


if __name__ == "__main__":
    main()
