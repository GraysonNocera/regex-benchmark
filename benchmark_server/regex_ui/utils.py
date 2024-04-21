import json
import os

from .constants import BUILDS, ENGINE_STATUS, PROJECT_ROOT, RUN_STATUS


def create_dir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def parse_output(test_name):

    data = {}

    json_file_path = os.path.join(PROJECT_ROOT, f'benchmarks/{test_name}.json')
    run_file_output = os.path.join(PROJECT_ROOT, f'runs/{test_name}_out.txt')
    run_file_error = os.path.join(PROJECT_ROOT, f'runs/{test_name}_err.txt')
    if not os.path.exists(json_file_path) or not os.path.exists(run_file_output) or not os.path.exists(run_file_error):
        data['state'] = str(RUN_STATUS.NOT_STARTED)
        return data
    
    with open(run_file_output, 'r') as file:
        output = file.readlines()

    with open(run_file_error, 'r') as file:
        error = file.readlines()

    if len(output) == 0:
        data['state'] = str(RUN_STATUS.NOT_STARTED)
        return data
    
    if len(error) > 0:
        print("Error: ", error)
        data['state'] = str(RUN_STATUS.FAILED)
        data['error'] = error
        return data

    if len(output) <= 2:
        data['state'] = str(RUN_STATUS.COMPILING)
        return data

    with open(json_file_path, 'r') as json_file:
        test_json = json.load(json_file)[0]
    engines_to_build = set(BUILDS).intersection(set(test_json['engines']))

    if len(output) <= 2 + len(engines_to_build):
        data['compiling'] = {engine: False for engine in engines_to_build}
        data['state'] = str(RUN_STATUS.COMPILING)
        for output_line in output[2:]:
            if "built." in output_line:
                engine = output_line.split("built.")[0].strip()
                assert engine in engines_to_build
                data['compiling'][engine] = True
        data["progress"] = str(sum(data['compiling'].values()) * 100 // len(data['compiling']))
        return data

    if len(output) <= 2 + len(engines_to_build) + 4 + (3 * len(test_json['engines'])):
        data['state'] = str(RUN_STATUS.RUNNING)
        data['running'] = {engine: str(ENGINE_STATUS.NOT_STARTED) for engine in test_json['engines']}
        index = 2 + len(engines_to_build) + 4
        while index < len(output):
            if index + 2 < len(output) and "ran." in output[index + 2]:
                engine = output[index + 2].split("ran.")[0].strip()
                assert engine in test_json['engines'], f"{engine} not in {test_json['engines']}"
                data['running'][engine] = str(ENGINE_STATUS.COMPLETED)
            else:
                engine = output[index].split("running.")[0].strip()
                assert engine in test_json['engines']
                data['running'][engine] = str(ENGINE_STATUS.RUNNING)
                total = int(output[index].split(", ")[-1].strip())
                if index + 1 < len(output):
                    data['progress'] = output[index + 1].count(".") * 100 // total
            index += 3

        return data

    if len(output) == 2 + len(engines_to_build) + 4 + (3 * len(test_json['engines'])) + 2:
        data['state'] = str(RUN_STATUS.COMPLETED)
        return data

    return data
    