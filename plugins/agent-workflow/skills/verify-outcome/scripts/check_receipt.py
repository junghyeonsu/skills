#!/usr/bin/env python3
"""Run one check and detect failed or stale file-scoped evidence. Python stdlib only."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


def digest(path):
    value = hashlib.sha256()
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Expected a regular non-symlink file: {path}")
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def run(args):
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise ValueError("Provide a command after --")
    receipt = Path(args.receipt).absolute()
    log = receipt.with_suffix(receipt.suffix + ".log")
    # Inspect symlinks before resolving; never silently replace an old receipt.
    inputs = sorted({Path(p).absolute() for p in args.input})
    before = {str(p): digest(p) for p in inputs}
    if receipt in inputs or log in inputs:
        raise ValueError("Receipt and log must be outside the input files")
    if receipt.exists() or receipt.is_symlink() or log.exists() or log.is_symlink():
        raise ValueError("Receipt or log already exists; use a new path for the next check")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    started = now()
    with log.open("xb") as stream:
        try:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)
            code = result.returncode
        except OSError as error:
            stream.write(str(error).encode("utf-8"))
            code = 127
    after = {}
    for path in inputs:
        try:
            after[str(path)] = digest(path)
        except (OSError, ValueError):
            after[str(path)] = None
    value = {
        "schema_version": 1,
        "cwd": os.getcwd(),
        "started_at": started,
        "finished_at": now(),
        "command": command,
        "exit_code": code,
        "inputs_before": before,
        "inputs_after": after,
        "inputs_changed_during_check": before != after,
        "log": str(log),
        "log_sha256": digest(log),
        "scope_limit": "Only selected file contents and process exit code; no semantic or environment proof.",
    }
    with receipt.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"receipt": str(receipt), "exit_code": code,
                      "inputs_changed_during_check": before != after}, ensure_ascii=False))
    # Preserve failures, and reject a success that modified its evidence inputs.
    return 0 if code == 0 and before == after else 1


def verify(args):
    value = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
    errors = []
    if value.get("schema_version") != 1:
        errors.append("Unsupported receipt schema")
    if value.get("exit_code") != 0:
        errors.append("The recorded command did not pass")
    before = value.get("inputs_before")
    after = value.get("inputs_after")
    if not isinstance(before, dict) or not before:
        errors.append("Missing input scope")
    elif before != after or value.get("inputs_changed_during_check") is not False:
        errors.append("Inputs changed during the check")
    if isinstance(before, dict):
        for name, expected in before.items():
            if digest(Path(name)) != expected:
                errors.append(f"Stale input: {name}")
    log = value.get("log")
    if not isinstance(log, str) or digest(Path(log)) != value.get("log_sha256"):
        errors.append("Missing or modified command log")
    print(json.dumps({"receipt": str(Path(args.receipt).absolute()),
                      "valid_for_selected_inputs": not errors, "errors": errors,
                      "scope_limit": "Not a claim of application correctness or goal completion."},
                     ensure_ascii=False))
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    runner = commands.add_parser("run", help="Execute argv directly and save a fresh receipt/log")
    runner.add_argument("--receipt", required=True)
    runner.add_argument("--input", action="append", required=True,
                        help="Existing regular file in the evidence scope; repeat for more files")
    runner.add_argument("command", nargs=argparse.REMAINDER)
    validator = commands.add_parser("verify", help="Reject failed, changed, or stale scoped evidence")
    validator.add_argument("receipt")
    args = parser.parse_args()
    try:
        return run(args) if args.action == "run" else verify(args)
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
