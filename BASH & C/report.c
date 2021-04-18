/*
Program to check collaborators for a student
***************************************************************
* Author         Dept.                  Date            Notes
***************************************************************
* Mia B.         Comp. Science.         Nov 16 2020     Initial version.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

struct logrecord {
	char name[100];
	char IPAddress[50];
};

char* getfield(char* line, int num){
	char* name;
	char* ip;
	
	int init_size = strlen(line);
	char delim[] = ",";

	char *ptr = strtok(line, delim);
	int counter = 0;

	while (ptr != NULL){
		if (counter == 0){
			name = ptr;
		} else if (counter == 6) {
			ip = ptr;
		}
		counter += 1;
		ptr = strtok(NULL, delim);
	}

	if (num == 1) {
		return name;
	}
	return ip;
}

bool checkNameExists(FILE* csvfile, char* name){
	char line[200];
	int counter = 0;

    	while (fgets(line, 200, csvfile)){
		if (strcmp(getfield(line,1), name) == 0){
			return true;
		}
		counter += 1;
	}

	return false;
}

char* findIP(FILE* file, char* n){
	char line[200];
	char* ip;
	ip = (char*)malloc( 50 * sizeof(char) ); /* allocating memory dynamically */

	while (fgets(line, 200, file)){
		if (strcmp(getfield(line,1), n) == 0){
			strcpy(ip, getfield(line, 6));
			return ip;
		}
        }
	
        return ip;
}

void findCollaborators(char* sname, char* sip, FILE* csvfile, FILE* rptfile){
	char line[200];
	char* prevname;

	while (fgets(line, 200, csvfile)){
		if (strcmp(getfield(line,6), sip) == 0 && strcmp(getfield(line,1), sname) != 0 && strcmp(getfield(line,1), prevname) != 0){
			prevname = getfield(line,1);
			fputs(getfield(line,1), rptfile);
			fputs("\n", rptfile);
		}
	}	
	
	fseek (rptfile, 0, SEEK_END);
 	char size = ftell(rptfile);

	if (0 == size) {
        	fputs("No collaborators found for ", rptfile);
		fputs(sname, rptfile);
		fputs("\n", rptfile);
	}
}

int main(int argc, char *argv[])
{
	//ERRORS
	//Check number of arguments
	if (argc != 4){
                fprintf(stderr, "Usage ./report <csvfile> \"<student name>\" <reportfile>\n");
                return 1;
        }

	//Check if csv file can be read
	FILE *csvfile;
	csvfile = fopen(argv[1], "r");

	if (csvfile == NULL) {
		fprintf(stderr, "Error, unable to open csv file %s\n", argv[1]);
		return 1;
	}

	//Check if user present in file
	char* name = argv[2];
	if (!checkNameExists(csvfile, name)){
		fprintf(stderr, "Error, unable to locate %s\n", argv[2]);
		return 1;
	}

	//Check if output file can be created
	FILE *outputfile;
	outputfile = fopen(argv[3], "w");

	if (outputfile == NULL){
		fprintf(stderr, "Error, unable to open the output file %s\n", argv[3]);
		return 1;
	}

	//Check for collaborators
	char* userip = findIP(csvfile, name);

	findCollaborators(name, userip, csvfile, outputfile);

	return 0;
}




