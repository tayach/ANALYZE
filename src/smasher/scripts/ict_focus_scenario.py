import os
import sys

import midas.api as mia


def main():
    project_root = os.path.abspath(os.path.join(__file__, "..", ".."))
    sys.path.insert(0, project_root)

    scenario_path = (
        os.path.join(project_root,"scenarios", "qmarket_mv.yml"),
        os.path.join(project_root, "scenarios","rettij_midas_mv.yml")
    )

    mia.run("ict_focus", {"end": 15*60*60}, scenario_path)


if __name__ == "__main__":
    main()
