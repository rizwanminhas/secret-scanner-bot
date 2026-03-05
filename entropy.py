import math
import re

TOKEN_REGEX = re.compile(r"[A-Za-z0-9/\+=]{20,}")

def shannon_entropy(data):

    entropy = 0

    for c in set(data):

        p = float(data.count(c)) / len(data)
        entropy += - p * math.log2(p)

    return entropy


def detect_entropy(text, threshold=4.5):

    findings = []

    for token in TOKEN_REGEX.findall(text):

        ent = shannon_entropy(token)

        if ent > threshold:

            findings.append({
                "type": "High Entropy",
                "value": token[:10] + "...",
                "entropy": ent
            })

    return findings