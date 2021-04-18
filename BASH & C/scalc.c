/*
Program to implement a scientific calculator
***************************************************************
* Author	 Dept.			Date		Notes
***************************************************************
* Mia B.	 Comp. Science. 	Oct 30 2020 	Initial version.
* Mia B.	 Comp. Science. 	Nov 03 2020 	All Error Handeling.
* Mia B.	 Comp. Science.		Nov 04 2020	Large number addition.
*/

#include <stdio.h>

int main(int argc, char *argv[]){
	//Check number of integrers
	if (argc != 4){
		printf("Error: invalid number of arguments!\nscalc <operand1> <operator> <operand2>\n");
		return 1;
	}

	//Cgeck if operator is '+'
	if (*argv[2] != '+'){
		printf("Error: operator can only be + !\n");
		return 1;
	}
	
	//Check if operands are positive integrers
	const char *const number = argv[1];
	const char *digit = number;
	int length1 = 0;
	int arr1[999] = { 0 };

	while (digit != NULL && *digit != '\0') {
        	if (*digit < '0' || *digit > '9'){
			printf("Error!! operand can only be positive integers\n");
			return 1;
		}
		arr1[length1] = arr1[length1] * 10 + (*digit - 48);
        	++digit;
		length1++;
    	}

	const char *const num2 = argv[3];
	const char *digit2 = num2;
	int length2 = 0;
	int arr2[999] = { 0 };

	while (digit2 != NULL && *digit2 != '\0') {
                if (*digit2 < '0' || *digit2 > '9'){
                        printf("Error!! operand can only be positive integers\n");
                        return 1;
                }
		arr2[length2] = arr2[length2] * 10 + (*digit2 - 48);
                ++digit2;
		length2++;
        }

	//Calculate the sum of the two operands
	int a[999];
	a[0] = 0;
   	int b[999];
	b[0] = 0;
   	int n;
   	int m;
	
	if ( length1 >= length2) {
		n = length1;
		m = length2;
		
		int loop1;
		for(loop1 = 0; loop1 < length1; loop1++){
        		a[loop1 + 1] = arr1[loop1];
        	}

		int loop2;
		for(loop2 = 0; loop2 < length2; loop2++){
			b[loop2 + 1] = arr2[loop2];
		}
		
	} else {
		n = length2;
		m = length1;
		
		int loop1;
        	for(loop1 = 0; loop1 < length1; loop1++){
        	 	b[loop1 + 1] = arr1[loop1];
                }       

                int loop2;
                for(loop2 = 0; loop2 < length2; loop2++){
                        a[loop2 + 1] = arr2[loop2];
                }
	}

	int sum[1000];
   	int i = n, j = m, k = n;
   	int c = 0, s = 0;
   	while (j >= 0) {
      		s = a[i] + b[j] + c;
      		sum[k] = (s % 10);
      		c = s / 10;
      		k--;
      		i--;
      		j--;
   	}

   	while (i >= 0) {
      		s = a[i] + c;
      		sum[k] = (s % 10);
      		c = s / 10;
      		i--;
      		k--;
   	}
   	
	for (int i = 0; i <= n; i++) {
		if( i == 0 && sum[i] == 0){
			continue;
		} else {
      			printf("%d", sum[i]);
		}
   	}
	printf("\n");	

	return 0;
	
}
