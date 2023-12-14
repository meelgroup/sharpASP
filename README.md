# sharpASP
sharpASP - Exact ASP Counting with Compact Encodings

## Requirement
- GMPlib

## Clone 
Clone the repository including all the submodules via
```
git clone --recursive git@github.com/meelgroup/sharpASP.git
```

## Build
To build ``sharpASP(D4)``:
```
cd d4
make 
```

To build ``sharpASP(ganak)``:
```
cd ganak-asp && cd script
./build_norm.sh
```

To build ``sharpASP(sharpsat-td)``:
```
cd sharpsat-td
./setupdev.sh
```

## Input CNF Files
The input CNFs are available [here](https://zenodo.org/records/8265042). The CNFs are in ``completion + copy`` format. The CNFs can be used as SharpASP input file without any processing.

# Quick Run of sharpASP

**We run our experiment in linux system**

__Make sure that the complied binaries of D4, sharpSAT-TD, ganak, and flow_cutter_pace17 exist in the current directory__

Run `sharpASP(GANAK)` using the following command (with input: `asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf`):
The input file contains ``Completion & Copy`` of program
```
./ganak -noPCC -cs 4000 -noIBCP asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf
```
Run `sharpASP(sharpSAT-TD)` using the following command:
```
./sharpSAT -decot 100 -decow 100 -tmpdir . -cs 4000 CNF/asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf
```
Run `sharpASP(D4)` using the following command:
```
./d4 -pv=NO -mc CNF/asp_normalized-hamiltonian_cycle.random-graph-20-4-16.zip.lp.cnf
```

## Experimental Log files
The experimental log files are available [here](https://zenodo.org/record/8265182).
