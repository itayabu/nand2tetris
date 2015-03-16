// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

	@R2
	M=0	// R2=0
	@i
	M=1	// i=1
(LOOP)
	@i
	D=M	// D=i
	@R1
	D=D-M	// D=i-R1
	@END
	D;JGT	// if (i-R1)>0 goto END
	@R0
	D=M	// D=R0
	@R2
	M=D+M	// R2=R2+R0
	@i
	M=M+1	// i=i+1
	@LOOP
	0;JMP	// goto LOOP
(END)
	@END
	0;JMP	// infinite loop