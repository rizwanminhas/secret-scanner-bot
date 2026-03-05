import subprocess
import multiprocessing
import os

from scanner import scan_text
from github_api import comment_pr


IGNORE_EXT = [
    ".png",".jpg",".gif",".lock",".map",".min.js"
]


def run(cmd):

    return subprocess.check_output(cmd).decode().strip()


def changed_files():

    base = os.getenv("GITHUB_BASE_REF")

    if base:

        cmd = ["git","diff",f"origin/{base}","--name-only"]

    else:

        cmd = ["git","diff","HEAD~1","--name-only"]

    out = run(cmd)

    return [f for f in out.split("\n") if f]


def file_content(path):

    try:

        with open(path,"r",errors="ignore") as f:

            return f.read()

    except:

        return ""


def should_ignore(path):

    for ext in IGNORE_EXT:

        if path.endswith(ext):

            return True

    return False


def scan_file(path):

    if should_ignore(path):

        return None

    text = file_content(path)

    findings = scan_text(text)

    if findings:

        return (path, findings)

    return None


def parallel_scan(files):

    pool = multiprocessing.Pool(4)

    results = pool.map(scan_file, files)

    pool.close()
    pool.join()

    findings = {}

    for r in results:

        if r:

            findings[r[0]] = r[1]

    return findings


def history_scan():

    commits = run(["git","rev-list","--all"]).split("\n")

    findings = []

    for commit in commits[:50]:

        diff = run(["git","show",commit])

        res = scan_text(diff)

        if res:

            findings.append((commit,res))

    return findings


def build_report(results):

    text = "🚨 **Secrets detected**\n\n"

    for file,items in results.items():

        text += f"### {file}\n"

        for i in items:

            val = i.get("secret") or i.get("value")

            text += f"- {i['type']} → `{val}`\n"

        text += "\n"

    return text


def main():

    print("\nAdvanced Secret Scanner\n")

    files = changed_files()

    print("Scanning files:",len(files))

    results = parallel_scan(files)

    if not results:

        print("No secrets detected")

        return

    print("Secrets found!")

    report = build_report(results)

    repo = os.getenv("GITHUB_REPOSITORY")
    pr = os.getenv("GITHUB_REF")

    if pr and "pull" in pr:

        pr_num = pr.split("/")[2]

        comment_pr(repo,pr_num,report)

    print(report)

    exit(1)


if __name__ == "__main__":

    main()