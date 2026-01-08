import math
import re
import statistics
from collections import Counter

BASE64_RE = re.compile(r"^[A-Za-z0-9+/=]{40,}$")

def entropy(s):
    if not s:
        return 0.0
    c = Counter(s)
    l = len(s)
    return -sum((v / l) * math.log2(v / l) for v in c.values())

def cryptanalysis(lines):
    entropies = []
    base64_hits = []

    for line in lines:
        if len(line) > 30:
            entropies.append(entropy(line))
        if "base64.b64decode" in line:
            base64_hits.append(line)


        for token in line.split():
            if BASE64_RE.match(token):
                base64_hits.append(token)

    avg_entropy = round(sum(entropies) / len(entropies), 3) if entropies else 0

    entropy_variance = (
        round(statistics.variance(entropies), 3)
        if len(entropies) > 1 else 0
    )

    return {
        "avg_entropy": avg_entropy,
        "entropy_variance": entropy_variance,
        "high_entropy_lines": sum(1 for e in entropies if e > 4.0),
        "base64_payload_count": len(base64_hits),
        "max_encoded_length": max((len(x) for x in base64_hits), default=0)
    }

