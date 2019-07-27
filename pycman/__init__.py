from pycman.core.utils.decorators import timer
from pycman.core.session.session import Session, AgentSet, SelectedEnv
from pycman.core.env.env_base import Env


__all__ = ["env", "agent"]

# Creating global classes
env = SelectedEnv()
agent = AgentSet()
__session = Session(agent, env)

# Function facade
run = __session.run
clear = __session.clear
