# Proving bounds on program size

After a participant in our freshers events found a program that solves towers
of hanoi in our language in just 9 characters, we were intrigued if that was
the smallest program to solve it.

In this folder is a state machine model of the interpreter written in
SystemVerilog, with which we have proved the smallest program to solve Hanoi for
3 towers takes 9 characters.

To run the proofs, you need [Yosys](https://github.com/YosysHQ/yosys),
[SymbiYosys](https://github.com/YosysHQ/sby), [sv2v](https://github.com/zachjs/sv2v) and
[GTKWave](https://gtkwave.sourceforge.net/) to view the resulting waveforms.

# Finding a length 9 program

```bash
# This may take up to ~20 minutes to find a trace. Don't worry about red text,
# it is expected that this command fails, as it has found a counterexample
# showing that "there are no successful length 9 programs" is false
sby -f hanoi_9.sby
# View the trace
gtkwave
# Click `hanoi` in the SST window on the left, then drag `mem` from the bottom
# left window into the box on the right. Then right click `mem` in the `Signals`
# window and Data Format>Decimal. The value of the memory can then be read out
# of the simulator and decoded with a python script:
python3 decode_enum_str.py <value>
```

# Proving there are no length 2-8 programs

```
# This may take up to ~20 minutes to get proofs, and runs a lot of threads in
# parallel, proving a range of combinations of initial character and program
# length
sby -f hanoi_8.sby
```
