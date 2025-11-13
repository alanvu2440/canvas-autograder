import requests

def get_last_commit_date(repo_url):
    parts = repo_url.rstrip('/').split('/')
    print("URL parts:", parts)
    if "github.com" in parts:
        idx = parts.index("github.com")
        if len(parts) > idx + 2:
            owner = parts[idx + 1]
            repo = parts[idx + 2].replace('.git', '')  # Remove .git if present
        else:
            print("URL format error")
            return None
    else:
        print("URL format error")
        return None
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    resp = requests.get(api_url)
    if resp.status_code == 200:
        commits = resp.json()
        if commits:
            return commits[0]['commit']['committer']['date']
    return None