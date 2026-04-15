# sharpASP
This is the codebase of SharpASP. The related publication is [here](https://ojs.aaai.org/index.php/AAAI/article/view/28927).

## Clone 
Clone the repository including all the submodules via
```
git clone --recursive git@github.com:meelgroup/sharpASP.git
```

## Requirement
You need to install `cmake`, `gmp` and `mpfr`.
```
sudo apt-get install build-essential cmake libgmp-dev libmpfr-dev libboost-all-dev
```

We use `gringo` as grounder. The best way to install gringo is to install via clingo:
```
pip install clingo
```

After install you should be able to check `gringo`:
```
$ gringo --version
gringo version XXX
```

You need normalization tool `lp2normal` [1] of ASP programs. You can download a (linux) static binary of lp2normal from [1]. We used `lp2normal-2.27`. Please use the command to download `lp2normal-2.27` in the current directory:
```
wget https://research.ics.aalto.fi/software/asp/lp2normal/binary-x86-64/lp2normal-2.27
chmod +x lp2normal-2.27
```

## Build 
First build our code as follows:
```
chmod +x build.sh
./build.sh
```
The command should build D4, Ganak, and SharpSAT-TD versions for SharpASP.

## Benchmark
The benchmark, experimental log files, binaries, and others are available here: [artifact](https://zenodo.org/records/19442660)


## Run sharpASP

Make sure that the complied binaries (from build) of D4, sharpSAT-TD, ganak, flow_cutter_pace17, and lp2normal-2.27 exist in the current directory. Please check as follows:
```
ls d4_bin sharpSAT ganak flow_cutter_pace17 lp2normal-2.27
```

Run `graph_reach.random-graph-20-3-3.zip.lp` using SharpASP `SharpSAT-TD` as follows:
```
python run-sharpasp.py -i graph_reach.random-graph-20-3-5.zip.lp -c std
```
it should print the count: `SharpASP Count: 99086`


Run `graph_reach.random-graph-20-3-3.zip.lp` using SharpASP `ganak` as follows:
```
python run-sharpasp.py -i graph_reach.random-graph-20-3-5.zip.lp -c ganak
```
it should print the count: `SharpASP Count: 99086`

Run `graph_reach.random-graph-20-3-3.zip.lp` using SharpASP `d4` as follows:
```
python run-sharpasp.py -i graph_reach.random-graph-20-3-5.zip.lp -c d4
```
it should print the count: `SharpASP Count: 99086`

## Experimental Log files
The experimental log files of our evaluation are available [here](https://zenodo.org/record/8265182).

## References
- [https://research.ics.aalto.fi/software/asp/lp2normal/](https://research.ics.aalto.fi/software/asp/lp2normal/)

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


