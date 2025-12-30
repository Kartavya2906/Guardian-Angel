import os
import json
import yaml

from src.github_monitor import clone_or_pull_repo
from src.diff_extractor import extract_added_lines
from src.behavioral_analysis import behavioral_analysis
from src.cryptanalysis_engine import cryptanalysis
from src.ml_risk_engine import load_model, build_features, predict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "added_code.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "final_output.json")

def main(return_json=False):
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    repo_cfg = config["github"]

    repo = clone_or_pull_repo(
        repo_cfg["repo_url"],
        repo_cfg["local_path"],
        repo_cfg["branch"]
    )

    added = extract_added_lines(repo)

    behavior_score, behavior_triggers = behavioral_analysis(added)
    crypto = cryptanalysis(added)

    model = load_model()
    features = build_features(behavior_score, crypto, len(added))
    risk = predict(model, features)

    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    with open(RAW_PATH, "w") as f:
        f.write("\n".join(added))

    output = {
        "repo": repo_cfg["repo_url"],
        "commit": repo.head.commit.hexsha,
        "behavior_score": behavior_score,
        "behavior_triggers": behavior_triggers,
        "crypto_analysis": crypto,
        "risk": risk
    }

    if return_json:
        return output

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=4)

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()

