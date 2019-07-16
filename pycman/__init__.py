
from pycman.core.run.run import Run
from pycman.core.stat.logging.logger import Logger
from pycman.core.agent.global_agents import GlobalAgentSet
from pycman.core.env.global_env import GlobalEnv
from pycman.core.utils.decorators import timer


__all__ = ["env", "agent", "run", "core", "timer"]


env = GlobalEnv()
agent = GlobalAgentSet()
logger = Logger("N/A")
run = Run(agent, env).run
