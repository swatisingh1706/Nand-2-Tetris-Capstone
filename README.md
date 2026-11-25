# Nand2Tetris Capstone Project
## Make the Computer Draw a Box

**Student Name:** Swati Singh  
**Roll Number:** 2501730269  
**Program:** B.Tech CSE (AI & ML)  
**Course:** Nand2Tetris – I  
**K Value:** 69

---

## Project Overview

This project implements the Hack computer using Hardware Description Language (HDL), develops a two-pass Hack assembler in Python, and creates a screen-drawing program that displays a rectangular box when a keyboard key is pressed.

## Project Structure

- **Part A – Hardware Implementation**
  - `CPU.hdl`
  - `Memory.hdl`
  - `Computer.hdl`
  - Test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`)

- **Part B – Python Hack Assembler**
  - `assembler.py`
  - Assembly programs: `Add.asm`, `Max.asm`, `Rect.asm`, `Pong.asm`
  - Generated machine-code files (`.hack`)
  - `symbols.txt`

- **Part C – Box Drawing Program**
  - `Box.asm`
  - `Box.hack`

- **Screenshots**
  - Test results and CPU Emulator outputs.

## K-Based Configuration

For K = 69:

- Starting row: 69
- Box height: 20 rows
- Box width: 32 pixels
- Starting screen address: 18592
- Required assembler feature: Save labels and variables with their addresses in `symbols.txt` (K mod 3 = 0).

## Implementation Summary

1. **Hardware Implementation:** CPU, Memory and Computer chips were implemented and tested using the supplied test scripts.
2. **Assembler:** A two-pass Python assembler translates Hack assembly programs into 16-bit machine instructions and stores custom symbols in `symbols.txt`.
3. **Box Program:** `Box.asm` uses the keyboard and screen memory to draw a 32 × 20 pixel rectangle at row 69.

## Tools and Technologies

- Hack Hardware Simulator
- Hack CPU Emulator
- Python
- HDL
- Hack Assembly Language
- GitHub

## Author

**Swati Singh**  
