from collections import defaultdict

CRYPTO = ["base64", "xor", "aes", "des", "rsa"]
DANGEROUS = ["eval(", "exec(", "os.system", "subprocess"]
NETWORK = ["socket", "requests.", "http"]

def behavioral_analysis(lines):
    score = 0
    triggers = defaultdict(int)

    for line in lines:
        l = line.lower()

        for k in CRYPTO:
            if k in l:
                score += 2
                triggers["crypto"] += 1

        for k in DANGEROUS:
            if k in l:
                score += 3
                triggers["dangerous"] += 1

        for k in NETWORK:
            if k in l:
                score += 2
                triggers["network"] += 1

        if len(line) > 120:
            score += 1
            triggers["obfuscation"] += 1

    return score, dict(triggers)

