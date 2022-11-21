import ast
from typing import List
import logging
import numpy as np
from palaestrai.agent import (
    ActuatorInformation,
    RewardInformation,
    SensorInformation,
)
from palaestrai.types import Box

# TODO when new palaestrai online: from palaestrai.environment.reward import Reward
from midas.tools.palaestrai.reward import Reward

LOG = logging.getLogger(__name__)


class ProfitReward(Reward):
    def __init__(self, attacker_idxs=(0, 1), **params):
        super().__init__(**params)
        self.attacker_idxs = attacker_idxs
        self.act_names = [
            "QMarket-0.QMarketModel_0.agent_bid_" + str(idx)
            for idx in self.attacker_idxs
        ]
        self.agent_ids = [
            "MarketAgents-0.MarketAgentModel_PV_" + str(idx)
            for idx in self.attacker_idxs
        ]

    def __call__(
        self,
        state: List[SensorInformation],
        actuators: List[ActuatorInformation],
        *arg,
        **kwargs
    ) -> List[RewardInformation]:

        rewards = []
        # TODO: This could be more efficient
        for sensor in state:
            if "q_accept" in sensor.sensor_id:
                q_setpoints = ast.literal_eval(sensor.sensor_value)
                break
        else:
            LOG.critical("No information about q_accept in state information!")

        for act in actuators:
            if act.actuator_id in self.act_names:
                idx = act.actuator_id.split("_")[-1]
                uid = "MarketAgents-0.MarketAgentModel_PV_" + str(idx)
                q_setpoint = q_setpoints.get(uid, 0)
                if act.setpoint is None:
                    price = 0
                else:
                    price = act.setpoint[1]  # idx 0 is amount, idx 1 is price

                rewards.append(price * abs(q_setpoint))

        final_reward = RewardInformation(
            sum(rewards), Box(-np.inf, np.inf, shape=(1,)), "qmarket profit"
        )
        return [final_reward]
