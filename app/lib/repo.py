from flask_dance.contrib.github import github
from yarl import URL


def _wrapped_get(url):
    print("Url", url)
    relativeUrl = url.path_qs

    resp = github.get(relativeUrl)
    if not resp.ok:
        print("Failed to fetch: ", relativeUrl, resp.text)
        return []
    return resp.json()


def _user_repos():
    url = URL.build(
        scheme="https",
        host="api.github.com",
        path="/user/repos",
        query={"per_page": 100, "sort": "full_name"},
    )
    return _wrapped_get(url)


def repo_list():
    repos = _user_repos()
    repo_names = list(map(lambda x: x["full_name"], repos))
    return repo_names
