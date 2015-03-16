@R15 //answer register
M=0
@R1 //temp answer
M=1
@R13
D = M
@R2 //mone
M = D
@R14
D = M
@R3 //mechane
M = D
@R4 //counter
M = 0

(STARTLOOP) // if mechane bigger than mone jump to 0
@R2 // mone 
D = M
@R3 // temp mechane
D = D - M
@END
D;JLT

(DIVLOOP)
@R2 // mone 
D = M
@R3 // temp mechane
D = D - M
@MANAGEMINUS
D;JLE
@R3
M = M<<
@R4 //counter
M = M + 1
@DIVLOOP
0;JMP

(MANAGEMINUS)
@R4 // counter
M = M - 1
D = M
@ENDCOUNT
D; JLE
@R1
M = M <<
@R4
@MANAGEMINUS
0;JMP

(ENDCOUNT)
@R1
D = M 
@R15
M = M + D
@R3
D = M >>
@R2
M = M - D 
@R14
D = M 
@R3
M = D 
@R1
M = 1
@STARTLOOP
0;JMP

(END)
0;JMP