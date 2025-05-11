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

def modify_agent(new_pipeline_path, key, value):
    data = toml.load(new_pipeline_path)
    pluggin = data["agent"]

    if key in pluggin:

        #print(f"Before: {key} = {pluggin[key]}")
        pluggin[key] = value
        #print(f"After:  {key} = {pluggin[key]}")


    with open(new_pipeline_path, "w") as f:
        toml.dump(data, f)


def modify_output(new_pipeline_path, key, value):
    data = toml.load(new_pipeline_path)
    pluggin = data["outputs"]["influxdb"][0]

    if key in pluggin:

        #print(f"Before: {key} = {pluggin[key]}")
        pluggin[key] = value
        #print(f"After:  {key} = {pluggin[key]}")


    with open(new_pipeline_path, "w") as f:
        toml.dump(data, f)




### different_jsonPaths_ETL template funcs ###


#def modify_processorsConventer(new_pipeline_path, key, value):
#    data = toml.load(new_pipeline_path)
#    #print(data)
#    pluggin = data["processors"]["converter"][0]["fields"]
#    print(pluggin)
#
#    if key in pluggin:
#        pluggin[key] = value
#    with open(new_pipeline_path, "w") as f:
#        toml.dump(data, f)
#
#
#def modify_processorsRename(new_pipeline_path, key, value):
#    data = toml.load(new_pipeline_path)
#    pluggin = data["processors"]["rename"][0]["replace"][0]
#    print(pluggin)
#    pluggin = data["processors"]["rename"][0]["replace"][1]
#    print(pluggin)
#
#    if key in pluggin:
#        pluggin[key] = value
#    with open(new_pipeline_path, "w") as f:
#        toml.dump(data, f)
#








### ChatGPT was used in the procesess of creating this function
##   def add_new_replace_block(new_pipeline_name):
##   
##   new_block = """  [[processors.rename.replace]]
##       field = "placeholder"
##       dest = "placeholder"
##   """
##   
##   with open(new_pipeline_name, "r") as file:
##       lines = file.readlines()
##   
##   # Find the last occurrence of '[[processors.rename.replace]]'
##   insert_index = -1
##   for i, line in enumerate(lines):
##       if line.strip().startswith("[[processors.rename.replace]]"):
##           insert_index = i
##   
##   while insert_index + 1 < len(lines) and lines[insert_index + 1].startswith(" "):
##       insert_index += 1
##   
##   # Insert the new block
##   lines.insert(insert_index + 1, new_block + "\n")
##   
##   with open(new_pipeline_name, "w") as file:
##       file.writelines(lines)
##   
