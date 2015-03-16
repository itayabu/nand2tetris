@i  //reset i counter
M = 0
@j  //reset j counter
M = 0

(OUTERLOOP)
@i
D = M
@R15
D = M - D
@END //check if (n-i) <= 0
D;JLE // jump to end


(INNERLOOP)
@j
M = M + 1 //advance j by 1 on each iteration
D = M
@R15
D = M - D
@ENDIN // check if (n-j) <= 0
D;JLE // jump to end of inner loop
@j
D = M
@R14
A = M + D // jump to address of a[j]
D = M
@R1 // temp loaction of a[j]
M = D
@i
D = M
@R14
A = M + D // jump to address of a[i]
D = M
@R2 // temp location of a[i]
M = D
@R1
D = M - D
@SWAP //check if a[i]>a[j]
D;JGT // jump to swap function
@INNERLOOP // jump to inner lop start
0;JMP

(SWAP) //swaps a[i] with a[j]
@i
D = M
@R14
A = M + D
D = A
@R3 // address of a[i]
M = D
@j
D = M
@R14 
A = M + D
D = A
@R4 //address of a[j]
M = D
@R1 //value of a[j]
D = M
@R3
A = M
M = D
@R2 // value of a[i]
D = M
@R4
A = M
M = D
@INNERLOOP // jump back to inner loop
0;JMP

(ENDIN) //end of inner loop
@i //advance i by 1
M = M + 1
D = M
@j
M = D
@OUTERLOOP //go back to outer loop
0;JMP


(END)
0;JMP