from patterns import COMPILED_PATTERNS
from entropy import detect_entropy


def scan_patterns(text):

    findings = []

    for name, pattern in COMPILED_PATTERNS.items():

        for m in pattern.finditer(text):

            findings.append({
                "type": name,
                "secret": m.group()[:12] + "...",
                "line": text[:m.start()].count("\n") + 1
            })

    return findings


def scan_text(text):

    results = []

    results.extend(scan_patterns(text))
    results.extend(detect_entropy(text))

    return results