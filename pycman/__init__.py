from pycman.core.utils.decorators import _timer
from pycman.core.session.session import _Session, _AgentSet, _SelectedEnv
from pycman.core.env.env_base import EnvBase
from pycman.core.agent.agent_base import AgentBase
from pycman.core.logger.simple_logger import Log

__all__ = ["env", "agent", "run", "EnvBase", "AgentBase"]

# Creating global classes
env = _SelectedEnv()
agent = _AgentSet()
log = Log(env, "pycman_log")
__session = _Session(agent, env, log)

# Function facade
run = __session.run
