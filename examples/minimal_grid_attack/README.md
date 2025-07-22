# Minimal Grid Attack Example

This directory contains a stripped down co-simulation setup showing how to run
ANALYSE with only a small pandapower grid and a single reinforcement learning
agent.  It reuses the `four_bus` example network shipped with MIDAS and omits
any ICT components.

* `four_bus.yml` – base MIDAS scenario with a small four bus system and time
  varying load profiles.
* `four_bus_der.yml` – extension adding two DER units with weather dependent
  generation. Loads and weather vary over time so the grid is not static.
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

If this is the first time you run palaestrAI on your system, create the
experiment database once with:

```bash
palaestrai database-create
```
