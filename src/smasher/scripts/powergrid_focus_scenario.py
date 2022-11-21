import os
import midas.api as mia


def main():
    scenario_path = os.path.abspath(
        os.path.join(__file__, "..", "..", "scenarios", "powergrid_mv.yml")
    )

    mia.run("powergrid_focus", {"end": 60 * 60}, scenario_path)


if __name__ == "__main__":
    main()
