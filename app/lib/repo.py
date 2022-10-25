from flask_dance.contrib.github import github


def repo_list():
    repos_resp = github.get("/user/repos")
    if not repos_resp.ok:
        print("Failed to fetch user repos.")
        return []
    repos = repos_resp.json()
    repo_names = list(map(lambda x: x["full_name"], repos))
    return repo_names
