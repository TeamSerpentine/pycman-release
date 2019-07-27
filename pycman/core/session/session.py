from ..env.env_gym import _GymWrapper
from pycman.core.utils.decorators import _timer
from pycman.core.session.run_procedures import _run_parallel, _run_sequential
from pycman.core.logger.simple_logger import Log

class _Session:

    def __init__(self, agents, env):
        self.agents = agents
        self.env = env
        pass

    @_timer
    def run(self, order='sequential'):
        """"Start running the agent with a particular environment. Can use different processing techniques."""

        if order == 'sequential':
            _run_sequential(self.agents, self.env)
        else:
            _run_parallel(self.agents, self.env)


class _SelectedEnv:
    """ Wrapper for all the different environment wrappers. Global access point for the currently
        selected environment in Pycman.
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
    """ Global collection of agent instances. """

    def __init__(self):
        self._nested_store = []
        self._nested_indices = []

    def add(self, item):
        """"Adds an agent to the current list of agents."""
        if not isinstance(item, list):
            raise TypeError("Agent must be contained inside a list!")
        self._nested_store.append(item)
        new_indices = [len(self)+i for i in range(len(item))]
        self._nested_indices.append(new_indices)

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
