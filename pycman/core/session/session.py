from ..env.env_gym import _GymWrapper
from pycman.core.utils.decorators import _timer
from pycman.core.session.run_procedures import _run_parallel, _run_sequential, _run_single
from pycman.core.logger.simple_logger import _Log
import pycman
import pandas as pd
import matplotlib.pyplot as plt


class _Session:
    """""Wrapper for pycman.functions."""

    def __init__(self, agents, env, log):
        self.agents = agents
        self.env = env
        self.log = log
        pass

    @_timer
    def run(self, order='sequential'):
        """"Start running the agent with a particular environment. Can use different processing techniques."""
        print("Start simulation with ", len(self.agents))
        if len(self.agents) == 0:
            raise RuntimeError("No agent has been specified. Add an agent with pycman.agent.add([your_agent_instance])")
        if self.env.get() is None:
            raise RuntimeError("No environment has been specified. Add an enviroment with pycman.env.set(your_env)"
                               " or with pycman.env.gym(env_name)")

        if len(self.agents) == 1:
            _run_single(self.agents, self.env)
        elif order == 'sequential':
            _run_sequential(self.agents, self.env)
        elif order == 'parallel':
            _run_parallel(self.agents, self.env)
        else:
            raise ValueError(order + " is not a valid procedure to run pycman! Please select one from the docs!")


class _Stat:

    logger = None

    def __init__(self, logger):
        self.logger = logger

    def plot(self, x_col, y_cols, title='', legend=True, grid=True, group_on_agent=False):
        if self.logger._line_log:
            open_at_end = True
            self.logger.close()
        else:
            open_at_end = False

        data = pd.read_csv(self.logger._last_log, sep=';')

        if x_col in data:
            plt.title(title)
            if group_on_agent:
                for _, group in data.groupby('agent_id'):
                    self._plot_results(plt, x_col, y_cols, group)
            else:
                self._plot_results(plt, x_col, y_cols, data)
            if grid: plt.grid()
            if legend: plt.legend()
            plt.xlabel(x_col)
            plt.show()
        else:
            raise ValueError(str(x_col) + ' is not valid column name!')

        if open_at_end:
            self.logger._open_last()

    def _plot_results(self, plt,  x_col, y_cols, data):

            if not isinstance(y_cols, list):
                y_cols = [y_cols]
            for y in y_cols:
                if y in data:
                    plt.plot(data[x_col].tolist(), data[y].tolist(), label=y)



class _SelectedEnv:
    """ Wrapper for all the different environment wrappers. Global access point for the currently
        selected environment in Pycman. The global instance is called with with pycman.env
    """

    _environment = None
    _game_name = None

    def gym(self, name):
        """"Choose a gym environment by name as the newly selected environment."""
        self._environment = _GymWrapper(name)
        self._game_name = name

    def set(self, environment, game_name):
        """"Set a third party environment as the newly selected environment."""
        self._environment = environment
        self._game_name = game_name

    def get(self):
        """"Get the current environment."""
        return self._environment

    def info(self):
        """"Get information about the current environment."""
        if self._environment is None:
            return None
        else:
            return self._environment.info()


class _AgentSet:
    """ Global collection of agent instances. The global instance is called with with pycman.agent"""

    def __init__(self):
        self._nested_store = []
        self._nested_indices = []
        self._unique_id = 0

    def add(self, item):
        """"Adds an agent to the current list of agents."""
        if not isinstance(item, list):
            raise TypeError("Agent must be contained inside a list!")
        self._nested_store.append(item)
        new_indices = [len(self) + i for i in range(len(item))]
        self._nested_indices.append(new_indices)

        for agent in item:
            agent.agent_id = self._unique_id
            self._unique_id += 1

    def clear(self):
        """"Removed all agents from the list."""
        self._nested_store = []
        self._nested_indices = []

    def __get_complex_index(self, idx):
        nr = 0  # elements seen
        i = 0  # list index
        while i < len(self._nested_store) and nr + len(self._nested_store[i]) <= idx:
            nr += len(self._nested_store[i])
            i = i + 1
        j = idx - nr  # element from the ith list
        return i, j

    def __setitem__(self, idx, val):
        i, j = self.__get_complex_index(idx)
        self._nested_store[i][j] = val

    def __getitem__(self, idx):
        i, j = self.__get_complex_index(idx)
        return self._nested_store[i][j]

    def __str__(self):
        return str(self._nested_store)

    def __repr__(self):
        return f"<class '{_AgentSet.__name__}'>"

    def __iter__(self):
        return iter([agent for agents in self._nested_store for agent in agents])

    def __len__(self):
        return len([agent for agents in self._nested_store for agent in agents])
