// Box Program - K = 69
// Starting row = 69
// Height = 20 rows
// Width = 32 pixels (2 words per row)

(START)
    // Check whether a key is pressed
    @KBD
    D=M
    @SETBLACK
    D;JNE

    // No key pressed: select white (clear)
    @R15
    M=0
    @INIT
    0;JMP

(SETBLACK)
    // Key pressed: select black
    @R15
    M=-1

(INIT)
    // Starting screen address = 16384 + (32 * 69) = 18592
    @18592
    D=A
    @R13
    M=D

    // Number of rows = 20
    @20
    D=A
    @R14
    M=D

(ROW)
    // Get the selected colour
    @R15
    D=M

    // Draw first 16-pixel word
    @R13
    A=M
    M=D

    // Draw second 16-pixel word
    @R13
    A=M+1
    M=D

    // Move to the next screen row (32 words)
    @R13
    D=M
    @32
    D=D+A
    @R13
    M=D

    // Decrease remaining row count
    @R14
    M=M-1
    D=M
    @ROW
    D;JGT

    // Check keyboard again
    @START
    0;JMP
