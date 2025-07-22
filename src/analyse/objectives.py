from __future__ import annotations

from functools import partial
from typing import Optional

from palaestrai.agent import Objective
from palaestrai.agent.memory import Memory
from midas_palaestrai.objectives import normal_distribution_pdf


class PowerGridAttackerObjective(Objective):
    """Custom version compatible with newer palaestrAI memory API."""

    VM_PU_NORM = partial(normal_distribution_pdf, mu=1.0, sigma=-0.05, c=-1.2, a=-2.5)

    def __init__(self, is_defender: bool = False) -> None:
        self.sign_factor = -1.0 if is_defender else 1.0

    def internal_reward(self, memory: Memory, **_: Optional[object]) -> float:
        """Compute internal reward based on latest stored rewards."""
        try:
            shard = memory.tail(1)
            max_vm = shard.rewards["vm_pu-max"].iloc[0]
            median_ll = shard.rewards["lineload-median"].iloc[0]
        except Exception:
            return 0.0

        return self.sign_factor * float(
            PowerGridAttackerObjective.VM_PU_NORM(max_vm) + 2 * median_ll / 100.0
        )

