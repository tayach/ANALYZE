"""This module contains the MIDAS upgrade for rettij."""
import logging
import os
from pathlib import Path
from typing import Any, Dict

import smasher_rettij.rettij_mosaik
from midas.util.upgrade_module import UpgradeModule
from pyparsing import Optional

LOG = logging.getLogger(__name__)
SMASHER_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
CUSTOM_COMPONENTS_DIR = Path(os.path.dirname(smasher_rettij.rettij_mosaik.__file__)) / "custom-components"

rettij_node_actuators = {}
rettij_node_sensors = {}

class RettijModule(UpgradeModule):
    """Rettij upgrade module for MIDAS 1.0."""

    def __init__(self):
        super().__init__(
            module_name="rettij",
            default_scope_name="rettij_mv",
            default_sim_config_name="SimRettijPyrate",
            default_import_str="smasher_rettij.rettij_mosaik.rettij_mosaik_pyrate:SimRettijPyrate",
            default_cmd_str="",
            log=LOG,
        )
        self.model_key: Optional[str] = None

    def check_module_params(self, module_params: Dict[str, Any]):
        """Check the module params: If all expected values are set; provide default values."""

        module_params.setdefault(
            "topology_path", Path(SMASHER_DIR) / "rettij_midas" / "midas_mv_topology.yml"
        )
        module_params.setdefault("sequence_path", "")
        module_params.setdefault("kubeconfig_path", None)
        # check if in yaml defined
        module_params.setdefault("components_dir_path", Path(CUSTOM_COMPONENTS_DIR))
        module_params.setdefault("monitoring_config_path", None)

        # We should probably set step_size in the yaml
        module_params["step_size"] = self.scenario.base.step_size // 4

    def check_sim_params(self, module_params: Dict[str, Any]):
        """Check the params for the simulator instance."""
        self.sim_params.setdefault("topology_path", module_params["topology_path"])
        self.sim_params.setdefault("sequence_path", module_params["sequence_path"])
        self.sim_params.setdefault("kubeconfig_path", module_params["kubeconfig_path"])
        self.sim_params.setdefault("components_dir_path", module_params["components_dir_path"])
        self.sim_params.setdefault("monitoring_config_path", module_params["monitoring_config_path"])

        # obtain rettij_mappings from yaml and put them to list for later connections
        # (they have to be defined in the yaml file)
        rettij_mappings = self.scenario.create_shared_mapping(self)
        for key, val in self.sim_params["rettij_mappings"].items():
            rettij_mappings[key] = val

        self.sim_params.pop("rettij_mappings")

    def start_models(self):
        """Start all models defined in the mapping of a certain simulator."""
        # get model key
        self.model_key = self.scenario.generate_model_key(self, "rettij")
        params = {}  # rettij doesn't require params, so empty dict

        full_id = self.start_model(self.model_key, "Rettij", params)
        rettij_model_mock = self.scenario.get_model(self.model_key, self.sim_key)
        rettij_nodes = {entity.eid: entity for entity in rettij_model_mock.children}
        for node_id, node in rettij_nodes.items():
            rettij_node_actuators[node_id] = {}
            rettij_node_sensors[node_id] = {}
            child_key = f"{self.model_key}_{node_id}"
            self.scenario.add_model(child_key, self.sim_key, node)
            self.scenario.script.model_start.append(
                f"{child_key} = [e for e in {self.model_key}.children " f'if e.eid == "{node_id}"][0]\n'
            )
            # loop over actuator entities with type "actuator"
            for actuator_entity in filter(lambda x: x.type == "actuator", node.children):
                actuator_id = actuator_entity.eid[len(f"{node_id}/actuator-"):]
                rettij_node_actuators[node_id][actuator_id] = actuator_entity

            # loop over sensor entities with type "sensor"
            for sensor_entity in filter(lambda x: x.type == "sensor", node.children):
                sensor_id = sensor_entity.eid[len(f"{node_id}/sensor-"):]
                rettij_node_sensors[node_id][sensor_id] = sensor_entity

    def connect(self):
        ict_mappings = self.scenario.get_ict_mappings()
        rettij_sim = self.scenario.get_sim(self.sim_key)
        rettij_mappings = self.scenario.create_shared_mapping(self)
        for ict_mapping in ict_mappings:
            model_key_sender = ict_mapping["sender"]
            model_key_receiver = ict_mapping["receiver"]
            sender_before_ict = ict_mapping["sender_before_ict"]
            receiver_before_ict = ict_mapping["receiver_before_ict"]
            attrs = ict_mapping["attrs"]
            mosaik_full_id_sender = self.scenario.get_model(model_key_sender, self.sim_key).full_id
            mosaik_full_id_receiver = self.scenario.get_model(model_key_receiver, self.sim_key).full_id
            rettij_node_id_sender = rettij_mappings[mosaik_full_id_sender]
            rettij_node_id_receiver = rettij_mappings[mosaik_full_id_receiver]
            rettij_node_id_model_key_sender = f"{self.model_key}_{rettij_node_id_sender}"
            rettij_node_id_model_key_receiver = f"{self.model_key}_{rettij_node_id_receiver}"

            sender_attrs = []
            receiver_attrs = []
            for attr in attrs:
                if isinstance(attr, tuple):
                    sender_attrs.append((attr[0], attr[1]))
                    receiver_attrs.append((attr[1], attr[1]))
                else:
                    receiver_attrs.append((attr, attr))
                    sender_attrs.append((attr, attr))

            LOG.debug(
                f"model_key_sender: {model_key_sender}; rettij_node_id_model_key_sender: "
                f"{rettij_node_id_model_key_sender}; sender_attrs: {sender_attrs}"
            )
            LOG.debug(
                f"rettij_node_id_model_key_receiver: {rettij_node_id_model_key_receiver}; model_key_receiver: "
                f"{model_key_receiver}; receiver_attrs: {receiver_attrs}"
            )

            if "initial_data" in ict_mapping:
                initial_data = {key: None for key in ict_mapping["initial_data"]}

                # connect mosaik entity model to rettij node (for timeshifted connections)
                self.connect_entities(
                    model_key_sender,
                    rettij_node_id_model_key_sender,
                    sender_attrs,
                    time_shifted=True,
                    initial_data=initial_data,
                )

                initial_data = {}
                for attr in receiver_attrs:
                    initial_data[attr[0]] = None

                if (sender_before_ict and not receiver_before_ict) or (not sender_before_ict and receiver_before_ict):
                    self.connect_entities(
                        rettij_node_id_model_key_receiver,
                        model_key_receiver,
                        receiver_attrs,
                        time_shifted=True,
                        initial_data=initial_data,
                    )
                elif not sender_before_ict and not receiver_before_ict:
                    self.connect_entities(
                        rettij_node_id_model_key_receiver,
                        model_key_receiver,
                        receiver_attrs,
                    )
                else:
                    LOG.error(f"Unexpected case of ict_mapping! ict_mapping: {ict_mapping}")
            else:
                # connect mosaik entity model to rettij node (for normal connections)
                if sender_before_ict and not receiver_before_ict:
                    self.connect_entities(model_key_sender, rettij_node_id_model_key_sender, sender_attrs)
                elif not sender_before_ict and not receiver_before_ict:
                    initial_data = {}
                    for attr in sender_attrs:
                        initial_data[attr[0]] = None
                    self.connect_entities(
                        model_key_sender,
                        rettij_node_id_model_key_sender,
                        sender_attrs,
                        time_shifted=True,
                        initial_data=initial_data,
                    )
                else:
                    LOG.error(f"Unexpected case of ict_mapping! ict_mapping: {ict_mapping}")

                self.connect_entities(
                    rettij_node_id_model_key_receiver,
                    model_key_receiver,
                    receiver_attrs,
                )

            # connect rettij's node with each other
            target_interface_name = "i0"  # hardcoded as each target node currently only has a i0 interface
            for attr in receiver_attrs:
                connect_config = {
                    "attribute": attr[1],
                    "target_interface_name": target_interface_name,
                }
                rettij_sim.connect(rettij_node_id_sender, rettij_node_id_receiver, **connect_config)
                LOG.debug(
                    f"Connected {rettij_node_id_model_key_sender} --> {rettij_node_id_model_key_receiver}; "
                    f"attr: {attr}"
                )

    def get_actuators(self):
        for node_id, node in rettij_node_actuators.items():
            for actuator in node.values():
                actuator_full_id= actuator.full_id
                action_space = self.scenario.get_sim(self.sim_key).get_actuator(actuator.eid).get_action_space()
                act = {
                    "actuator_id": f"{actuator_full_id}.value",
                    "action_space": action_space
                }
                self.scenario.actuators.append(act)

    def get_sensors(self):
        for node_id, node in rettij_node_sensors.items():
            for sensor in node.values():
                sensor_full_id= sensor.full_id
                observation_space = self.scenario.get_sim(self.sim_key).get_sensor(sensor.eid).get_action_space()
                self.scenario.sensors.append({"sensor_id": f"{sensor_full_id}.value", "observation_space": observation_space })

    def connect_to_db(self):
        pass
