from functools import reduce


def find_by_id(user, project_id):
    return reduce(
        lambda acc, item: item if item.id == project_id else acc, user.projects, None
    )


def find_by_name(user, name):
    return reduce(lambda acc, item: item if item.name == name else acc, user.projects, None)
