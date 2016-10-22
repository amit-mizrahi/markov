def sort_keys_by_value(dictionary):
    return sorted(
        dictionary.keys(),
        reverse = True,
        key = dictionary.get
    )
