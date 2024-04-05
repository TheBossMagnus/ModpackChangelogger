def add_overrides(old_overrides, new_overrides, added, removed, updated):
    old_overrides = {'yosbr-0.1.1.jar': '797b4096ccf2b22a76a28471836a178316042a2f490faea02ab25b75edd5c77a'}
    new_overrides = {'yosbr-0.1.1.jar': '797b4096ccf2b22a76a28471836a178316042a2f490faea02ab25b75edd5c77a'}
    
    identical_entries = {key: value for key, value in old_overrides.items() if new_overrides.get(key) == value}
    old_overrides = {key: value for key, value in old_overrides.items() if key not in identical_entries}
    new_overrides = {key: value for key, value in new_overrides.items() if key not in identical_entries}



    print("Overrides detection is not implemented yet")
    print("old_overrides:", old_overrides)
    print("new_overrides:", new_overrides)
    return added, removed, updated
