# SM4SH3R

## Description

The PYRATE software suite, better known as "SM4SH3R" is the fearless beast that can take down whole energy grids in a simulation just by pure artificial intelligence!

Maybe. Sometimes. In the future!

## Getting Started

This section will guide you through the installation process and show you how to start a basic scenario.

## Download the Sources

First, you have to download the source files, i.e., this repository.
This can be done either with git

```bash
git clone https://gitlab.com/pyrate-project/smasher.git
```

or if you click on the Download button.
For the rest of this guide it is assumed, that you have a command line running in the top-level source folder.

### Python and Dependencies

Make sure you have Python >=3.8, <3.10 available on your system. 
If you use MacOS, install xcode developer tools:

```bash
xcode-select --install
```

Then, install all Python deps with the `requirements.txt` (including ARL, midas and rettij) into a `venv`:

```bash
# create venv
python3 -m venv ./venv

# activate venv
source venv/bin/activate

# install requirements (run this in the project's root directory)
pip install -r requirements.txt
```

### Setup Kubernetes

Rettij requires a Kubernetes cluster up and running to execute the simulation. Please follow [the official instructions](https://medit.pages.frihsb.de/rettij/docs/getting-started.html#step-by-step-guide-for-installing-rettij-based-on-k3d-for-linux) from the rettij documentation to setup a local cluster correctly. (you can skip the sections about installing rettij via pip as this has been done by the `requirements.txt` already)

## Scenarios

There are 3 different scenarios (MIDAS yaml files) that are located in `src/smasher/scenarios` and python scripts in `src/smasher/scripts` to start each of those (names end with `_scenario.py`).

### Power Grid Focus Scenario

This scenario concentrates on the power grid only.
It consists of a power grid model, provider for load profiles, and Photovoltaic simulation models including weather data.
This scenario is used in the power grid attack experiment.
Start this with

```bash
python3 src/smasher/scripts/powergrid_focus_scenario.py
```

### Market Focus Scenario

This scenario concentrates on a reactive power market.
Because a reactive power market does only work well with a power grid model, most of the components of the power grid focus scenario are included here as well (although there are some minor differences that do not really matter).
This scenario is used in the qmarket attack experiment.
Start this with

```bash
python3 src/smasher/scripts/qmarket_focus_scenario.py
```

### ICT Focus Scenario

This scenario concentrates on ICT and is a direct extension for the market focus scenario.
Certain connections, namely from Photovoltaic to market agents and from market agents to the market model, will now be redirected through the ICT simulator rettij.
This scenario is used in the ict data manipulation experiment. 

![ICT focus scenario image](pyrate%20ICT-scenario.png "Overall topology of the ICT focus scenario.")

## Experiments

There are 3 different experiments (palaestrai experiment yaml files) that are located in `src/smasher/experiments` and python scripts in `src/smasher/scripts` to start each of those (names end with `_experiment.py`).


### Power Grid Attack Experiment

*Write me*

### Market Attack Experiment

*Write me*

### ICT Data Manipulation Experiment

*Write me*
