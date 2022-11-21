import os
import sys

from palaestrai.cli.manager import cli


def main():
    project_root = os.path.abspath(os.path.join(__file__, "..", ".."))
    sys.path.insert(0, project_root)

    run_file = os.path.abspath(
        os.path.join(project_root, "experiments", "powergrid_attack_experiment.yml")
    )
    cli(["-v", "start", run_file])


if __name__ == "__main__":
    main()
