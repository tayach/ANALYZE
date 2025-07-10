"""Standalone MIDAS scenario runner for the minimal 4-bus example.

Running this script will launch the power system co-simulation without
any reinforcement learning agent attached.  It can be used to quickly
check that the scenario itself executes and produces reasonable power
flow results.
"""
import os
import midas.api as mia


def main():
    # Resolve the YAML path relative to this script
    scenario_path = os.path.join(
        os.path.dirname(__file__), "four_bus_der.yml"
    )
    # Run the scenario for one simulated day
    mia.run("four_bus_der", {"end": 24 * 60 * 60}, scenario_path)
    # After completion the ``minimal_fourbus.hdf5`` file can be inspected with
    # your favourite pandas or HDF5 viewer to check bus voltages and generator
    # outputs over time.


if __name__ == "__main__":
    main()
