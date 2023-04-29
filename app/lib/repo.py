from flask_dance.contrib.github import github
from yarl import URL


def repo_list():
    url = URL.build(
        scheme="https",
        host="api.github.com",
        path="/user/repos",
        query={"per_page": 100},
    )
    print("url", url)
    relativeUrl = url.path_qs

    repos_resp = github.get(relativeUrl)
    if not repos_resp.ok:
        print("Failed to fetch user repos.")
        return []
    repos = repos_resp.json()
    print("num repos found: ", len(repos))
    repo_names = list(map(lambda x: x["full_name"], repos))
    return repo_names
