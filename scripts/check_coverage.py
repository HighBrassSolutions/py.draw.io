import json
import sys


def main():
    coverage_file = sys.argv[1]
    with open(coverage_file) as f:
        data = json.load(f)

    totals = data["totals"]

    line_cov = totals["percent_covered"]
    branch_cov = totals["percent_branches_covered"]

    print(f"[i] Line coverage: {line_cov}%")
    print(f"[i] Branch coverage: {branch_cov}%")

    fail = False

    if line_cov < 100:
        print("[err] Line coverage is below 100%")
        fail = True

    elif branch_cov < 100:
        print("[err] Branch coverage is below 100%")
        fail = True

    if fail:
        sys.exit(1)

    print("[success] Coverage is 100% for both lines and branches")


if __name__ == "__main__":
    main()
