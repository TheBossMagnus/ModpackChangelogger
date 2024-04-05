def add_overrides(old_overrides, new_overrides, added, removed, updated):

    identical_entries = set(old_overrides.values()) & set(new_overrides.values())
    old_overrides = {key: value for key, value in old_overrides.items() if value not in identical_entries}
    new_overrides = {key: value for key, value in new_overrides.items() if value not in identical_entries}

    print("Overrides detection is not implemented yet")
    print("old_overrides:", old_overrides)
    print("new_overrides:", new_overrides)
    return added, removed, updated
