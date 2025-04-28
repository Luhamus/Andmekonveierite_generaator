import toml

def modify_input(new_pipeline_path, key, value):
    data = toml.load(new_pipeline_path)
    pluggin = data["inputs"]["http"][0]

    if key in pluggin:

        #print(f"Before: {key} = {pluggin[key]}")
        pluggin[key] = value
        #print(f"After:  {key} = {pluggin[key]}")


    with open(new_pipeline_path, "w") as f:
        toml.dump(data, f)


##modify_input("templates/basic_ETL.toml", "test_pipers.toml, "urls", ["stillTesting"])


## TODO
def modify_agent(new_pipeline_path, key, value):
    data = toml.load(new_pipeline_path)
    pluggin = data["agent"]

    if key in pluggin:

        #print(f"Before: {key} = {pluggin[key]}")
        pluggin[key] = value
        #print(f"After:  {key} = {pluggin[key]}")


    with open(new_pipeline_path, "w") as f:
        toml.dump(data, f)




## TODO
def modify_output(new_pipeline_path, key, value):
    data = toml.load(new_pipeline_path)
    pluggin = data["outputs"]["influxdb"][0]

    if key in pluggin:

        print(f"Before: {key} = {pluggin[key]}")
        pluggin[key] = value
        print(f"After:  {key} = {pluggin[key]}")


    with open(new_pipeline_path, "w") as f:
        toml.dump(data, f)
