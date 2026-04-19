#!/usr/bin/env python3

import os
import argparse
import subprocess
import shutil
import tempfile
import sys


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--i", help="input ASP program", required=True)
parser.add_argument("-t", "--t", help="timeout", default=5000, required=False, type=float)
parser.add_argument("-c", "--c", help="counter name", default="std", required=False)
args = parser.parse_args()


def fail(msg):
    print(msg)
    sys.exit(1)


if shutil.which("gringo") is None:
    fail("gringo is not installed. Please install gringo")

if not os.path.exists(args.i):
    fail("Input file {0} does not exist".format(args.i))

if not os.path.exists("./lp2normal-2.27"):
    fail("lp2normal-2.27 does not exist in current directory")


counter_name = args.c if args.c else "std"
if counter_name not in ("std", "ganak", "d4"):
    print("Counter {0} is not supported. Supported counters are std, ganak and d4".format(counter_name))
    counter_name = "std"
    print("Using default counter {0}".format(counter_name))


if counter_name == "std":
    if not os.path.exists("./sharpSAT") or not os.path.exists("./flow_cutter_pace17"):
        fail("Tools ./sharpSAT or ./flow_cutter_pace17 do not exist")
elif counter_name == "ganak":
    if not os.path.exists("./ganak"):
        fail("Tool ./ganak does not exist")
elif counter_name == "d4":
    if not os.path.exists("./d4_bin"):
        fail("Tool ./d4_bin does not exist")


def parse_count(output_file, counter):
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            if counter == "std" and line.startswith("c s exact arb int"):
                return int(line.strip().split()[-1])
            if counter == "ganak" and line.startswith("s pmc"):
                return int(line.strip().split()[-1])
            if counter == "d4" and line.startswith("s "):
                return int(line.strip().split()[-1])
    return None


def run_counter(counter, cnf_file, output_file, timeout_seconds):
    if counter == "std":
        cmd = [
            "./sharpSAT",
            "-decot", "10",
            "-decow", "100",
            "-tmpdir", ".",
            "-cs", "4000",
            cnf_file,
        ]
    elif counter == "ganak":
        cmd = [
            "./ganak",
            "-noPCC",
            "-cs", "4000",
            "-noIBCP",
            cnf_file,
        ]
    else:
        cmd = [
            "./d4_bin",
            "-pv=NO",
            "-mc",
            cnf_file,
        ]

    try:
        with open(output_file, "w", encoding="utf-8") as out:
            subprocess.run(
                cmd,
                stdout=out,
                stderr=subprocess.DEVNULL,
                timeout=timeout_seconds,
                check=True,
                text=True,
            )
    except subprocess.TimeoutExpired:
        fail("SharpASP timeouted")
    except subprocess.CalledProcessError:
        fail("SharpASP failed")

    count = parse_count(output_file, counter)
    if count is None:
        fail("SharpASP failed to parse the counter output")
    return count


temp_file = None
input_file = None
normalized_file = None
cnf_file = None
output_file = None

try:
    with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
        temp_file = f.name

    shutil.copyfile(args.i, temp_file)
    input_file = os.path.basename(temp_file)
    normalized_file = "normalized-{0}".format(input_file)
    cnf_file = "comp_copy_{0}.cnf".format(normalized_file)
    output_file = "output_{0}.out".format(input_file)

    with open(normalized_file, "w", encoding="utf-8") as norm_out:
        gringo_proc = subprocess.Popen(
            ["gringo", "-o", "smodels", input_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        try:
            subprocess.run(
                ["./lp2normal-2.27"],
                stdin=gringo_proc.stdout,
                stdout=norm_out,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        finally:
            if gringo_proc.stdout is not None:
                gringo_proc.stdout.close()
            gringo_proc.wait()

    subprocess.run(
        [sys.executable, "clark_completion_extended.py", normalized_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    if not os.path.exists(cnf_file):
        fail("Failed to create CNF file {0}".format(cnf_file))

    print("Invoking the SharpASP ({0})...".format(counter_name))
    count = run_counter(counter_name, cnf_file, output_file, float(args.t))
    print("SharpASP Count: {0}".format(count))

finally:
    for path in [temp_file, normalized_file, cnf_file, output_file]:
        if path is not None and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass