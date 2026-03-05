import re

PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret": r"(?i)aws(.{0,20})?(secret|key)[\"'=:\s]{0,5}[A-Za-z0-9\/+=]{40}",
    "Google API": r"AIza[0-9A-Za-z\-_]{35}",
    "Stripe Secret": r"sk_live_[0-9a-zA-Z]{24}",
    "Slack Token": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
    "JWT": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Private Key": r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----",
    "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
    "Password": r"(?i)password\s*[=:]\s*[\"'][^\"']+[\"']",
}

COMPILED_PATTERNS = {
    k: re.compile(v)
    for k, v in PATTERNS.items()
}