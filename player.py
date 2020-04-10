from typing import List
from environment import ConnectFourEnvironment


class Player:

    def action_values(self, env: ConnectFourEnvironment) -> List[float]:
        pass

    def play(self, env: ConnectFourEnvironment) -> [ConnectFourEnvironment, int]:
        pass
