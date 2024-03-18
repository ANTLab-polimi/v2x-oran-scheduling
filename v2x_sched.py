# from commands import run_command, fatal, CommandError
import os
import subprocess

import sys
import math
import random
from datetime import datetime
from typing import List
import shutil
import psutil
from os import walk
from os import listdir
from os.path import isfile, join
# import numpy as np
import numpy as np
import platform

class SchedulerType(Enum):
    UE_SELECTED = 2
    ORAN_SELECTED = 3

_n_traces_path = "tracesPath"
_n_relay_time = "relayTime"
_n_tx_power = "transmitPowerdBm"
_n_e2_ltePlmnId = 'ltePlmnId'
_n_e2_starting_port = 'e2StartingPort'
_n_e2_is_xapp_enabled = 'isXappEnabled'
_n_e2_sim_tag = 'simTag'
_n_e2_output_dir = 'outputDir'
_n_ue_number = "ueNumber"
_n_is_decentralized_relay = 'isDecentralizedRelay'
_n_snr_decentralized_relay = 'decentralizedRelaySnr'
_n_nr_active_groups = 'activeGroups'

_v_parameters_file = "parameters.txt"

_REWRITE_TEXT_FILES = True
_EXCLUDE_NO_RELAY = False

if __name__ == '__main__':
    _base_path = "" #if platform.node() == 'antilion2' else '/home/fgjeci'
    _v_output_dir_name = _base_path+"/storage/franci/simulations/nr-v2x/"
    working_path = "/home/fgjeci/workspace/ns3-v2x/"

    _all_loads =  [20, 50, 75, 100, 150, 200]
    _all_scheduling_types = [SchedulerType.UE_SELECTED, SchedulerType.ORAN_SELECTED]
    _all_simulations = []

    _l_command_list = []
    _l_log_files = []

    _v_e2_starting_port = 48470

    _v_simulation_index = -1

    # append no relay
    # first simulation of no relay
    # _all_simulations.append((0, 'no_relay'))

    # simulations with xapp
    for _load in _all_loads:
        for _sched_type in _all_scheduling_types:
            _all_simulations.append((_sched_type, _load))

    for _single_sim in _all_simulations:
        _sched_type = _single_sim[0]
        _load = _single_sim[2]
        # change the execution file in base of the load
        _exec_file_name = "nr-v2x-test"

        _v_sim_tag_name = "load_" + str(_load) + "_sched_type_" + str(_sched_type)

        _v_simulation_index += 1

        _v_param_map = {
            # _n_traces_path: os.path.join(_v_output_dir_name, _v_sim_tag_name),
            _n_e2_sim_tag: _v_sim_tag_name,
            _n_e2_output_dir: _v_output_dir_name,
            _n_e2_is_xapp_enabled: False,
            _n_ue_number: _load,
            _n_e2_ltePlmnId: str(111 + _v_simulation_index),
            _n_e2_starting_port: _v_e2_starting_port + 100 * _v_simulation_index
        }

        _v_param_single_str = " ".join(
            "--{!s}={!s}".format(key, val) for (key, val) in _v_param_map.items())

        _v_sim_directory = _v_output_dir_name

        # Deleting the directory to remove old content
        if _REWRITE_TEXT_FILES:
            if os.path.isdir(os.path.join(_v_sim_directory, _v_sim_tag_name)):
                shutil.rmtree(os.path.join(_v_sim_directory, _v_sim_tag_name))

        _v_sim_directory = os.path.join(_v_output_dir_name, _v_sim_tag_name)

        # check if it exists and create it if it does not exist
        if _REWRITE_TEXT_FILES:
            if not os.path.isdir(_v_sim_directory):
                os.mkdir(_v_sim_directory)

        _t_parameters_file = open(os.path.join(_v_sim_directory, _v_parameters_file), "w")
        _t_parameters_file.write("std::string {} = {};\n".format(_n_traces_path, _v_sim_directory))
        # _t_parameters_file.write("double {} = {};\n".format(_n_relay_time, _relay_time))
        # _t_parameters_file.write("double {} = {};\n".format(_n_tx_power, _tx_power))
        _t_parameters_file.write("std::string {} = {};\n".format(_n_e2_ltePlmnId, str(111 + _v_simulation_index)))
        _t_parameters_file.write("uint16_t {} = {};\n".format(_n_e2_starting_port, _v_e2_starting_port + 100 * _v_simulation_index))
        _t_parameters_file.close()

        _t_readme_text_file = open(os.path.join(_v_sim_directory, "README.txt"), "w")
        _t_readme_text_file.write("Traces path n: {}\n".format(_v_sim_directory))
        # _t_readme_text_file.write("Relay time: {}\n".format(_relay_time))
        # _t_readme_text_file.write("Tx power: {}\n".format(_tx_power))
        _t_readme_text_file.write("Lte plmn: {}\n".format(str(111 + _v_simulation_index)))
        _t_readme_text_file.write("Port number: {}\n".format(_v_e2_starting_port + 100 * _v_simulation_index))
        _t_readme_text_file.write("Load: {}\n".format(_load))
        _t_readme_text_file.write("Scheduling type: {}\n".format(_sched_type))
        _v_sim_start_time = datetime.now()
        _t_readme_text_file.write("Simulation starting time: " + str(_v_sim_start_time) + "\n")
        _t_readme_text_file.write("Command: \n")
        _t_readme_text_file.write('./ns3' + ' run ' + r"{} {!s}".format(_exec_file_name, _v_param_single_str))
        _t_readme_text_file.close()

        _l_command_list.append(['./ns3', 'run', r"{} {!s}".format(_exec_file_name, _v_param_single_str)])
        _l_log_files.append(_v_sim_directory)

    ### Run simulation
    os.chdir(working_path)
    processes = []
    log_files_objs = [open(os.path.join(_log_file_full_path, "logfile.log"), 'w') for _log_file_full_path in
                      _l_log_files]

    _processes_id = []

    for _single_command_ind in range(0, len(_l_command_list)):
        _single_command = _l_command_list[_single_command_ind]
        _output_file = log_files_objs[_single_command_ind]
        p = subprocess.Popen(_single_command,
                             stdout=_output_file,
                             stderr=subprocess.STDOUT,
                             )
        _processes_id.append(p.pid)
        processes.append(p)

    # _v_output_dir_name insert the process id numbers in a text file to make it easier to kill them afterwards
    # _kill_cmd = "kill " + " ".join(str(psutil.Process(process.pid).parent().pid) for process in processes)
    _kill_cmd = "kill " + " ".join(str(process.pid) for process in processes) + "\n"

    _t_kill_cmd_file = open(os.path.join(_v_output_dir_name, "kill_cmd.txt"), "w")
    _t_kill_cmd_file.write(_kill_cmd)
    _t_kill_cmd_file.write(str(os.getpid()))
    _t_kill_cmd_file.close()

    for p_ind in range(0, len(processes)):
        p = processes[p_ind]
        p.wait()
        _v_sim_stop_time = datetime.now()
        # Add to read me file
        _t_readme_text_file = open(os.path.join(_l_log_files[p_ind], "README.txt"), "a")
        _t_readme_text_file.write("\n\nSimulation ending time: " + str(_v_sim_stop_time))
        _t_readme_text_file.close()
