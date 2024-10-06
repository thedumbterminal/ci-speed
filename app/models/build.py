from functools import reduce


def find_by_ref(project, ref):
    return reduce(
        lambda acc, item: item if item.ref == ref else acc, project.builds, None
    )
