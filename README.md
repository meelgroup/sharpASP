# sharpASP
This is the codebase of SharpASP. The related publicatin is [here](https://ojs.aaai.org/index.php/AAAI/article/view/28927).

## Requirement
You need to install `gmp` and `mpfr`.
```
sudo apt-get install libgmp-dev libmpfr-dev
```

## Clone 
Clone the repository including all the submodules via
```
git clone --recursive git@github.com:meelgroup/sharpASP.git
```

## Build
You implement SharpASP within \#SAT solvers D4, Ganak, and SharpSAT-TD.

To build D4
```
cd d4
make 
```
It should create a binary `d4`.

To build Ganak:
```
cd ganak-asp && cd script
./build_norm.sh
```
It should create a binary `ganak`

To build SharpSAT-TD:
```
cd sharpsat-td
./setupdev.sh
```
It should create binaries `flow_cutter_pace17` and `sharpSAT`.

## Benchmark
The benchmark, experimental log files, binaries, and others are available here: [artifact](https://zenodo.org/records/19442660)


# Run sharpASP

Make sure that the complied binaries (from build) of D4, sharpSAT-TD, ganak, and flow_cutter_pace17 exist in the current directory.

Run the ganak version of SharpASP using the following command (input: `asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf`):
```
./ganak -noPCC -cs 4000 -noIBCP asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf
```
Run sharpSAT-TD version of SharpASP using the following command (it will run the tree decomposition for 10 seconds):
```
./sharpSAT -decot 10 -decow 100 -tmpdir . -cs 4000 asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf
```
Run D4 version of SharpASP using the following command:
```
./d4 -pv=NO -mc asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf
```

## Preprocessing 
Before running SharpASP, you need to ground and normalize the input ASP program and compile it in CNF as Completion + Copy format. We used `gringo` [potassco](https://potassco.org/clingo/) and `lp2normal-2.27` [asptools](https://github.com/asptools/software) for grounding and normalization, respectively. 

Let the normalized input file is `normalized-inputfile`, then run the command to get it in Completion + Copy format:
```
python clark_completion_extended.py normalized-inputfile
```
the command will create a CNF file named `comp_copy_normalized-inputfile.cnf` (which is the target Completion + Copy format)

## Experimental Log files
The experimental log files of our evaluation are available [here](https://zenodo.org/record/8265182).

## How to cite
Please cite our work if you use it:
```
@inproceedings{KCM2024,
  title={Exact ASP counting with compact encodings},
  author={Kabir, Mohimenul and Chakraborty, Supratik and Meel, Kuldeep S},
  booktitle={AAAI},
  volume={38},
  number={9},
  pages={10571--10580},
  year={2024}
}
```

