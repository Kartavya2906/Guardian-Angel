def extract_added_lines(repo, commits=5):
    added = []

    commits_list = list(repo.iter_commits(max_count=commits))
    for i in range(len(commits_list) - 1):
        newer = commits_list[i]
        older = commits_list[i + 1]

        diffs = older.diff(newer, create_patch=True)
        for diff in diffs:
            if diff.diff:
                for line in diff.diff.decode(errors="ignore").split("\n"):
                    if line.startswith("+") and not line.startswith("+++"):
                        added.append(line[1:])
    return added

