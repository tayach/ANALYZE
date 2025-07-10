# Minimal Grid Attack Example

This directory contains a stripped down co-simulation setup showing how to run
ANALYSE with only a small pandapower grid and a single reinforcement learning
agent.  It reuses the `four_bus` example network shipped with MIDAS and omits
any ICT components.

* `four_bus_der.yml` – MIDAS scenario describing the four bus system with two
  PV/CHP units.  Loads and weather vary over time so the grid is not static.
* `minimal_grid_attack.yml` – palaestrAI run file training a simple PPO agent
  that manipulates the reactive power of one PV unit.  The reward is the
  voltage deviation on all buses.
* `minimal_scenario.py` – script to execute the scenario without RL to verify
  that it runs standalone.

Run the RL experiment with:

```bash
palaestrai experiment-start examples/minimal_grid_attack/minimal_grid_attack.yml
```

After the run you can inspect `minimal_arl.hdf5` for the agent's actions and
`minimal_fourbus.hdf5` for the raw simulation outputs.
