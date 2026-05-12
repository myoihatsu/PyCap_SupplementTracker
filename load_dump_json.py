import json


#
#* function - connect to json file
#
def load_from_json(directory):
    try:
        with open(directory,'r') as x_file:
            data_file = json.load(x_file)    
        return data_file
    except FileNotFoundError:
        print("Error: The file 'data.json' was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (invalid JSON format).")

#
#* function - update / dump to json file
#
def dump_to_json(directory,data_to_dump):
    try:
        with open(directory,'w') as x_file:
            json.dump(data_to_dump,x_file,indent=4)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
