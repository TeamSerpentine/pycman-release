""" This file contains the functionality required to create, step and reset environments """

from abc import ABC, abstractmethod


class Env(ABC):
    @abstractmethod
    def make(env_name):
        """"Creates an environment from one of the supported standard environments (Gym). """
        pass

    @abstractmethod
    def step(*args, **kwargs):
        """"Perform one step in the environment with the provided arguments. """
        pass

    @abstractmethod

    def reset(*args, **kwargs):
        """"Resets the environment"""
        pass

