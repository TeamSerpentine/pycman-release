"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import sqlite3
import pandas as pd
import os
import sys
from contextlib import closing


class PersistentStorage:
    """Controls the saving and recovery of data from the hard-drive"""

    def __init__(self, compressor, save_folder, games_to_store=1):
        self._save_path = None
        self._compressor = None
        self._games_to_store = games_to_store
        self._save_path = self.set_path(save_folder)
        self._compressor = self.set_compressor(compressor)
        self._first_time_save = True

    def set_compressor(self, compressor):
        """
        Sets the algorithm_base to compress visual data with

        Parameters
        ----------
        compressor : Compressor
            The compressor to be used until a new one will be set.

        Modifies
        --------
        compressor
        """

        # Set an empty compressor if none exists, that will return entered values
        if compressor is None:
            compressor = type('', (), dict(compress=lambda x: x,
                                                 decompress=lambda x: x
                                                 ))
        elif compressor == "Empty":
            compressor = type('', (), dict(compress=lambda x: "",
                                                 decompress=lambda x: x
                                                 ))
        else:
            compressor = compressor
        print('Using Compressor: ', type(compressor).__name__)
        return compressor

    def get_compressor(self):
        """
        Gets the algorithm_base to compress visual data with

        Returns
        -------
        compressor
        """

        return self._compressor

    def get_path(self):
        """
        Gets the path to the DB.

        Returns
        -------
        string
            Path where the DB is located
        """

        return self._save_path

    @staticmethod
    def set_path(save_folder):
        """
        Sets the path to the database to save the data in.

        Parameters
        ----------
        save_folder : string
            Path to the folder where the database will be created
        """

        # This is for in memory sql tables, can be used for testing
        if save_folder == "" or save_folder == ":memory:":
            return save_folder

        return os.path.join(save_folder, "GameInfo.db")

    def store(self, data):
        """
        Compresses and stores the data passed to it

        Parameters
        ----------
        data : dict(pd.DataFrame)
            Data to be stored. ndarrays should be passed as lists

        """

        with sqlite3.connect(self._save_path) as conn:  # Connect to the data base
            data = PersistentStorage._copy_data(data)  # Make the data safe to modify

            # Compressing the observation
            data["evaluation_step_data"]["observation"] = self._compressor.compress(
                data["evaluation_step_data"]["observation"])

            # Set the schema for the database
            with closing(conn.cursor()) as curr:
                PersistentStorage._create_schemas(curr)

            # Store the contents of the dataframes
            data["evaluation_step_data"].to_sql("evaluation_step_data", conn, if_exists="append", index=False)
            data["evaluation_game_data"].to_sql("evaluation_game_data", conn, if_exists="append", index=False)
            data["training_step_data"].to_sql("training_step_data", conn, if_exists="append", index=False)
            data["training_game_data"].to_sql("training_game_data", conn, if_exists="append", index=False)
            data["epoch_data"].to_sql("epoch_data", conn, if_exists="append", index=False)

            if self._first_time_save:
                data["running_session_data"].to_sql("running_session_data", conn, if_exists="append", index=False)
                self._first_time_save = False

            conn.commit()

    def load(self):
        """
        Recovers and decompresses the data stored at SAVE_PATH

        Returns
        -------
        data :  dict(pd.DataFrame)
            Data returned. Identical to the one stored up to the order of the columns in the DataFrames
        """

        with sqlite3.connect(self._save_path) as conn:  # Connect to the data base
            data = dict()

            data["evaluation_step_data"] = pd.read_sql_query("SELECT * FROM evaluation_step_data", conn)
            data["evaluation_game_data"] = pd.read_sql_query("SELECT * FROM evaluation_game_data", conn)
            data["training_step_data"] = pd.read_sql_query("SELECT * FROM training_step_data", conn)
            data["training_game_data"] = pd.read_sql_query("SELECT * FROM training_game_data", conn)
            data["epoch_data"] = pd.read_sql_query("SELECT * FROM epoch_data", conn)
            data["running_session_data"] = pd.read_sql_query("SELECT * FROM running_session_data", conn)

            # Decompress the observation
            data["evaluation_step_data"]["observation"] = self._compressor.decompress(
                 data["evaluation_step_data"]["observation"])

            with closing(conn.cursor()) as curr:
                PersistentStorage._enforce_indices(data, curr)

            return data

    # Create tables in the target SQLite database (through cursor)
    @staticmethod
    def _create_schemas(sqlite_cursor):
        sqlite_cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluation_step_data (
                    step_id INTEGER,
                    evaluation_id	INTEGER,
                    running_session_id	STRING,
                    observation	 STRING,
                    reward	FLOAT,
                    done	BOOLEAN,
                    info	STRING,
                    action	INTEGER,
                    CONSTRAINT con1 PRIMARY KEY (step_id, evaluation_id, running_session_id)
                );
               """)
        sqlite_cursor.execute("""
               CREATE TABLE IF NOT EXISTS evaluation_game_data (
                    evaluation_id	INTEGER,
                    epoch	INTEGER,
                    running_session_id	STRING,
                    reward_sum	FLOAT,
                    step_count	INTEGER,
                    actions	 STRING,
                    CONSTRAINT con2 PRIMARY KEY (evaluation_id, epoch, running_session_id)
               );
               """)
        sqlite_cursor.execute("""
               CREATE TABLE IF NOT EXISTS training_step_data (
                    step_id	 INTEGER,
                    game_id	 INTEGER,
                    running_session_id	STRING,
                    reward	FLOAT,
                    done	BOOLEAN,
                    info	STRING,
                    action	INTEGER,
                    CONSTRAINT con3 PRIMARY KEY (step_id, game_id, running_session_id)
               );
               """)
        sqlite_cursor.execute("""
               CREATE TABLE IF NOT EXISTS training_game_data (
                    game_id	 INTEGER,
                    epoch	INTEGER,
                    running_session_id	STRING,
                    reward_sum	FLOAT,
                    step_count	INTEGER,
                    actions	 STRING,
                    CONSTRAINT con4 PRIMARY KEY (game_id, epoch, running_session_id)
               );
               """)
        sqlite_cursor.execute("""
               CREATE TABLE IF NOT EXISTS epoch_data (
                    running_session_id	STRING,
                    epoch	INTEGER,
                    training_episode_count	INTEGER,
                    training_step_count	INTEGER,
                    training_time	float,
                    training_average_reward	FLOAT,
                    training_actions	STRING,
                    training_average_steps	FLOAT,
                    evaluation_average_reward	FLOAT,
                    evaluation_actions	STRING,
                    evaluation_average_steps	FLOAT,
                    algorithm_field_1_value	FLOAT,
                    algorithm_field_2_value	FLOAT,
                    algorithm_field_3_value	FLOAT,
                    CONSTRAINT con5 PRIMARY KEY (epoch, running_session_id)

               );
               """)
        sqlite_cursor.execute("""
               CREATE TABLE IF NOT EXISTS running_session_data (
                    running_session_id	STRING,
                    session_name	STRING,
                    previous_session	INTEGER,
                    algorithm_name	STRING,
                    algorithm_config_file	STRING,
                    compressor_name 	STRING,
                    preprocessor_name	STRING,
                    preprocessor_config_file	STRING,
                    hardware	STRING,
                    game_name	STRING,
                    platform	STRING,
                    user	STRING,
                    algorithm_field_1_name	STRING,
                    algorithm_field_2_name	STRING,
                    algorithm_field_3_name	STRING,
                    CONSTRAINT con6 PRIMARY KEY (running_session_id)
               );
               """)

    # Set the index of the dataframes in data to the primary keys given in the database (connected through curr)
    @staticmethod
    def _enforce_indices(data, curr):
        for table_name in data.keys():
            primary_key = []

            curr.execute("""
                   PRAGMA table_info({});
               """.format(table_name))
            schema = curr.fetchall()

            for column in schema:
                if column[-1] != 0:
                    primary_key.append(column[1])

            data[table_name].set_index(primary_key, inplace=True)

    # Returns a deep copy of a dictionary of dataframes
    @staticmethod
    def _copy_data(data):
        copied_data = dict()

        # Make copy of each dataframe
        for table_name in data.keys():
            copied_data[table_name] = data[table_name].copy()

        return copied_data

    @staticmethod
    def print_msg(msg):
        sys.stdout.write("\r" + msg)
        sys.stdout.flush()
