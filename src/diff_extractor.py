def extract_added_lines(repo):
    commit = repo.head.commit
    if not commit.parents:
        return []

    parent = commit.parents[0]
    diffs = parent.diff(commit, create_patch=True)

    added = []
    for diff in diffs:
        if diff.diff:
            for line in diff.diff.decode(errors="ignore").split("\n"):
                if line.startswith("+") and not line.startswith("+++"):
                    added.append(line[1:])
    return added

