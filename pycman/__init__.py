from pycman.core.utils.decorators import _timer
from pycman.core.session._session import _Session, _AgentSet, _SelectedEnv
from pycman.core.env.env_base import EnvBase
from pycman.core.agent.agent_base import AgentBase


__all__ = ["env", "agent", "run", "clear", "EnvBase", "AgentBase"]

# Creating global classes
env = _SelectedEnv()
agent = _AgentSet()
__session = _Session(agent, env)

# Function facade
run = __session.run
clear = __session.clear