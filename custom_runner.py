"""Custom runner: executes the behave suite for a given tag and writes Allure results."""
import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(ROOT, "reports", "allure-results")


def run_tests(tag):
    # Start every run from a clean results folder
    if os.path.exists(RESULTS_DIR):
        shutil.rmtree(RESULTS_DIR)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # NOTE: behave pairs each --outfile with the --format given *before* it.
    # The Allure formatter must therefore come first, followed by -o <dir>;
    # the "pretty" formatter comes last with no outfile so it prints to the console.
    command = [
        sys.executable, "-m", "behave",
        "--tags", tag,
        "--no-skipped",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", RESULTS_DIR,
        "-f", "pretty",
    ]

    print("=" * 60)
    print(f"Executing JSONBin tests with tag: {tag}")
    print("=" * 60, flush=True)

    return subprocess.run(command, cwd=ROOT).returncode


def main():
    parser = argparse.ArgumentParser(description="Run JSONBin BDD tests by tag")
    parser.add_argument("--tag", choices=["@tag1", "@tag2"], required=True)
    args = parser.parse_args()
    return run_tests(args.tag)


if __name__ == "__main__":
    sys.exit(main())
