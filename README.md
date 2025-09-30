# Bartosz Virtual Machine – EPITA Project

## Authors
- Paulo Guimaraes  
- Nam Khanh  
- Kelyan Ihinack  

## Context
This project was developed as part of a course at **EPITA – Kremlin-Bicêtre**.  
The assignment consisted of implementing a simplified **virtual machine** in Python, along with a set of instructions and unit tests to validate its behavior.

## Delivered Files
The following files are included in the submission:

- `bartosz_vm.py` – core virtual machine implementation  
- `bartosz_stack.py` – stack operations  
- `bartosz_flow.py` – control flow instructions  
- `bartosz_memory.py` – memory operations  
- `bartosz_arith.py` – arithmetic and logical instructions  
- `bartosz_assembler.py` – assembler and helper functions (`assemble`, `justify`, etc.)  
- `bartosz_absval.py` – absolute value function implementation  
- `bartosz_fibonacci.py` – Fibonacci and factorial implementations  
- `bartosz_sanity_test.py` – sanity test cases for the VM  
- `bartosz_sample_test.py` – additional sample tests

## How to Run
Run the sanity test to check the virtual machine:

```bash
python3 bartosz_sanity_test.py
