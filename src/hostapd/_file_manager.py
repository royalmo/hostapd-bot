import pathlib, os, json

JSON_PATH = os.path.join(pathlib.Path().parent.resolve(), "data.json")

DEFAULT_DATA = {
    "admins" : [],
    "subscribed" : [],
    "pending-notifications" : [],
    "hour-ranges" : [ ([]*24) ] # 24 empty lists for each range (hour of day)
}

def get_json_path():
    return JSON_PATH

def set_json_path(json_path):
    global JSON_PATH
    JSON_PATH = json_path

def get_json_data():
    try:
        with open(JSON_PATH, 'r') as f:
            return json.read(f)
    except FileNotFoundError:
        print(f"[HostAPd Module] Generating data file at {JSON_PATH}")
        write_json_data(DEFAULT_DATA)
        return DEFAULT_DATA

def write_json_data(data):
    with open(JSON_PATH, 'w') as f:
        json.dump(data, f, indent=2)
