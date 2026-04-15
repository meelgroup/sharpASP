import os, argparse, subprocess, shutil, tempfile

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input ASP program', required=True)
parser.add_argument('-t','--t', help='timeout', default=5000, required=False)
parser.add_argument('-c','--c', help='counter name', default='std', required=False)
args = parser.parse_args()


if shutil.which("clingo"):
    # print("Gringo Installed")
    pass
else:
    print("clingo is not installed. Please install clingo")
    exit(1)

if not os.path.exists(args.i):
    print("Input file {0} does not exist".format(args.i))
    exit(1)

if not os.path.exists("./lp2normal-2.27"):
    print("lp2normal-2.27 does not exist in current directory")
    exit(1)

def get_time(file, solver):
    file_name = os.path.basename(file)
    res_dir = "."
    output_file = res_dir + "/" + solver + "_" + \
        file_name[len("output_"):-len(".out")] + ".timeout"
    time = subprocess.Popen('grep "User time (seconds)" {0}'.format(
        output_file), shell=True, stdout=subprocess.PIPE).stdout
    time = time.read().decode("utf-8").strip().split()
    user_time = float(time[-1])

    time = subprocess.Popen('grep "System time (seconds)" {0}'.format(
        output_file), shell=True, stdout=subprocess.PIPE).stdout
    time = time.read().decode("utf-8").strip().split()
    system_time = float(time[-1])
    return user_time + system_time


total_time = int(args.t)
counter_name = args.c if args.c else "std"
if counter_name != "std" and counter_name != "ganak" and counter_name != "d4":
    print("Counter {0} is not supported. Supported counters are std, ganak and d4".format(counter_name))
    counter_name = "std"
    print("Using default counter {0}".format(counter_name))

with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name
    os.system("cp {0} {1}".format(args.i, temp_file))
    input_file = os.path.basename(temp_file)

os.system("clingo --mode=gringo -o smodels {0} | ./lp2normal-2.27 > normalized-{0}".format(input_file))
os.system("python clark_completion_extended.py normalized-{0}".format(input_file, args.i))

print(f'Invoking the SharpASP ({counter_name})... ')

count = 0
if counter_name == "std":
    if not os.path.exists('./sharpSAT') or not os.path.exists('./flow_cutter_pace17'):
        print("Tools ./sharpSAT or ./flow_cutter_pace17 do not exist")
        exit(1)
    os.system('timeout {0}s /usr/bin/time --verbose -o {1}.timeout ./sharpSAT -decot 10 -decow 100 -tmpdir . -cs 4000 comp_copy_normalized-{1}.cnf > output_{1}.out'.format(total_time, input_file))
elif counter_name == "ganak":
    if not os.path.exists('./ganak'):
        print("Tool ./ganak does not exist")
        exit(1)
    os.system('timeout {0}s /usr/bin/time --verbose -o {1}.timeout ./ganak -noPCC -cs 4000 -noIBCP comp_copy_normalized-{1}.cnf > output_{1}.out'.format(total_time, input_file))
elif counter_name == "d4":
    if not os.path.exists('./d4_bin'):
        print("Tool ./d4_bin does not exist")
        exit(1)
    os.system('timeout {0}s /usr/bin/time --verbose -o {1}.timeout ./d4_bin -pv=NO -mc comp_copy_normalized-{1}.cnf > output_{1}.out'.format(total_time, input_file))


# count the (projected) models of the second formula
out_file = open('output_{0}.out'.format(input_file), 'r')
for line in out_file:
    if counter_name == "std":
        if line.startswith("c s exact arb int"):
            l = line.strip().split()
            count = int(l[-1])
    if counter_name == "ganak":
        if line.startswith("s pmc"):
            l = line.strip().split()
            count = int(l[-1])
    if counter_name == "d4":
        if line.startswith("s"):
            l = line.strip().split()
            count = int(l[-1])

print("SharpASP Count: {0}".format(count))
os.system("rm -f {0} *.timeout {1} {2} {3}".format(temp_file, "normalized-{0}".format(input_file), "comp_copy_normalized-{0}.cnf".format(input_file), "output_{0}.out".format(input_file)))
