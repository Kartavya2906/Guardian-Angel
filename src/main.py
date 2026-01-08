import os
import json
import yaml

from src.github_monitor import clone_or_pull_repo
from src.diff_extractor import extract_added_lines
from src.behavioral_analysis import behavioral_analysis
from src.cryptanalysis_engine import cryptanalysis
from src.ml_risk_engine import load_model, build_features, predict

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "added_code.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "final_output.json")

# ---------------- Entropy Tracking ----------------
def compute_entropy_delta(current_entropy, previous_entropy):
    if previous_entropy is None:
        return 0.0
    return round(current_entropy - previous_entropy, 3)

def load_previous_entropy(repo_name):
    path = os.path.join(BASE_DIR, "data", f"{repo_name}_last_entropy.txt")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return float(f.read().strip())

def save_current_entropy(repo_name, entropy):
    path = os.path.join(BASE_DIR, "data", f"{repo_name}_last_entropy.txt")
    with open(path, "w") as f:
        f.write(str(entropy))

# ---------------- Main Engine ----------------
def main(return_json=False, override_repo=None):

    # Load config
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    repo_cfg = config["github"]

    if not override_repo:
        raise ValueError("repo_url must be provided via API or UI")

    repo_url = override_repo

    local_path = repo_cfg["local_path"]
    

    # Clone or pull repo
    repo = clone_or_pull_repo(repo_url, local_path)

    # ---------------- Language Risk Detection ----------------
    file_types = set()

    for blob in repo.tree().traverse():
        if blob.type == "blob" and "." in blob.path:
            ext = blob.path.rsplit(".", 1)[-1].lower()
            file_types.add(ext)

    language_risk = "Low"

    if {"c", "cpp", "h"}.intersection(file_types):
        language_risk = "Medium"

    if {"sh", "ps1", "bat"}.intersection(file_types):
        language_risk = "High"

    # Extract diff (multi-commit)
    added = extract_added_lines(repo, commits=7)

    # Analyses
    behavior_score, behavior_triggers = behavioral_analysis(added)
    crypto = cryptanalysis(added)

    normalized_behavior = round(
        behavior_score / max(len(added), 1), 3
    )

    # Entropy delta
    repo_name = repo_url.split("/")[-1]
    previous_entropy = load_previous_entropy(repo_name)
    current_entropy = crypto["avg_entropy"]

    entropy_delta = compute_entropy_delta(current_entropy, previous_entropy)
    save_current_entropy(repo_name, current_entropy)

    # ML risk
    model = load_model()
    features = build_features(normalized_behavior, crypto, len(added))
    risk = predict(model, features)

    # Risk escalation
    if risk["risk"] == "Medium" and entropy_delta > 1.0:
        risk["risk"] = "High"

    if risk["risk"] == "Low" and crypto.get("max_encoded_length", 0) > 200:
        risk["risk"] = "Medium"

    if crypto.get("entropy_variance", 0) > 1.5:
        risk["risk"] = "High"
    if (crypto.get("base64_payload_count", 0) > 0 and crypto.get("avg_entropy", 0) > 3.8 ):
         risk["risk"] = "High"

    # Save added code
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    with open(RAW_PATH, "w") as f:
        f.write("\n".join(added))

    repo_size_signal = len(added)
    activity_level = "Low"

    if repo_size_signal > 500:
        activity_level = "High"
    elif repo_size_signal > 100:
        activity_level = "Medium"

    # Output
    output = {
        "repo": repo_url,
        "commit": repo.head.commit.hexsha,
        "behavior_score": behavior_score,
        "behavior_triggers": behavior_triggers,
        "crypto_analysis": crypto,
        "entropy_delta": entropy_delta,
        "risk": risk,
        "explanation": explain_result(
            behavior_score,
            crypto,
            entropy_delta,
            risk,
            language_risk,
            activity_level
        ),
        "language_risk": language_risk,
        "repo_activity": activity_level


    }
    


    if return_json:
        return output

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=4)

    print(json.dumps(output, indent=4))

# ---------------- Explainability ----------------
def explain_result(behavior_score, crypto, entropy_delta, risk,language_risk,activity_level):
    reasons = []

    if entropy_delta > 1.0:
        reasons.append("Sudden increase in entropy compared to previous commit")

    if crypto.get("max_encoded_length", 0) > 200:
        reasons.append("Large encoded payload detected in code changes")

    if behavior_score > 5:
        reasons.append("Suspicious behavioral patterns detected in code")

    if crypto.get("avg_entropy", 0) > 4.8:
        reasons.append("High entropy indicates possible encrypted payload")

    if crypto.get("base64_payload_count", 0) > 0:
        reasons.append("Encoded payload detected in code changes")

    if not reasons:
        reasons.append("No anomalous behavior detected")

    reasons.append(f"Detected languages risk level: {language_risk}")
    reasons.append(f"Repository activity level: {activity_level}")



    return reasons


# ---------------- Local Run ----------------
if __name__ == "__main__":
    main()

