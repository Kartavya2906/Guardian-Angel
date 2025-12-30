import math
from collections import Counter
import re

BASE64_RE = re.compile(r"^[A-Za-z0-9+/=]{40,}$")

def entropy(s):
    if not s:
        return 0.0
    c = Counter(s)
    l = len(s)
    return -sum((v/l) * math.log2(v/l) for v in c.values())

def cryptanalysis(lines):
    entropies = []
    base64_hits = []

    for line in lines:
        if len(line) > 30:
            e = entropy(line)
            entropies.append(e)

        for token in line.split():
            if BASE64_RE.match(token):
                base64_hits.append(token)

    return {
        "avg_entropy": round(sum(entropies)/len(entropies), 3) if entropies else 0,
        "high_entropy_lines": sum(1 for e in entropies if e > 4.5),
        "base64_payload_count": len(base64_hits)
    }

