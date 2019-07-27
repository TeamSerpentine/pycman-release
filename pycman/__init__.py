from pycman.core.utils.decorators import timer
from pycman.core.session.session import Session, AgentSet, SelectedEnv
from pycman.core.env.env_base import Env


__all__ = ["env", "agent", "session", "timer"]


env = SelectedEnv()
agent = AgentSet()
session = Session(agent, env)
run = session.run

