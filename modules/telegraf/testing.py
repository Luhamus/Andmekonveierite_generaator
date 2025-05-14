import toml

def modify_input(template, new_pipeline_path, key, value):
    data = toml.load(template)
    pluggin = data["inputs"]["http"][0]

    if key in pluggin:

        print(f"Before: {key} = {http_input[key]}")
        http_input[key] = value
        print(f"After:  {key} = {http_input[key]}")


    with open(new_pipeline_path, "w") as f:
        toml.dump(data, f)

modify_input("templates/basic_ETL.toml", "test_pipers.toml, "urls", ["stillTesting"])
