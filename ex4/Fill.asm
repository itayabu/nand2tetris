// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

@SCREEN
D=A
@whitey
M=D
@nigga
M=D

(LOOP)
	@24576
	D=M	// Keyboard key
	@BLACK
	D;JNE	// If Key is pressed JUMP to BLACK
	@WHITE
	D;JEQ	// If Key isn't pressed JUMP to WHITE
(BLACK)
	@SCREEN
	D=A	
	@whitey
	M=D	// Set whiter to SCREEN
	
	@24576
	D=A
	@nigga
	D=M-D
	@LOOP
	D;JGE	// If nigga got to max value then jump to LOOP
	@nigga
	A=M
	M=-1	// Blacker the current pixel	
	@nigga
	M=M+1	//adds +1 to nigga address
	@LOOP
	0;JMP	// Return to LOOP
(WHITE)
	@SCREEN
	D=A	
	@nigga
	M=D	// Set whiter to SCREEN
	
	@24576
	D=A
	@whitey
	D=M-D
	@LOOP
	D;JGE	// If nigga got to max value then jump to LOOP
	@whitey
	A=M
	M=0	// Blacker the current pixel
	@whitey
	M=M+1	//adds +1 to nigga address
	@LOOP
	0;JMP	// Return to LOOP