#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

FILE *out;
int rows, columns;
int depth;
int **data;
char* ext = ".pgm\0";
char* joined;
int silence = false;
int magic_number = 0;

int create_magic_number(char* magic_phrase);
void open_files();
void close_files();
void create_header();
void matrix_allocation();
void create_dark_pixel();
void shed_light(int magic_number, bool silence);
void cast_shadow();
char* concat(const char *s1, const char *s2);

int main(int argc, char *argv[]){
	if (argc >2){
		printf("Too much noise. One light, one word\n");
		exit(-1);
	}
	else if (argc < 2){
		printf("Tell me a word to shed some light\n");
		open_files(joined = concat("silence", ext));
		silence = true;
	} else {
		printf("One word is light in the darkness of silence\n");
		open_files(joined = concat(argv[1], ext));
		magic_number = create_magic_number(argv[1]);
	}
	
	
	create_header();
	matrix_allocation();
	create_dark_pixel();
	shed_light(magic_number, silence);
	cast_shadow();
	close_files();

	return 0;
}

int create_magic_number(char* magic_phrase){
	
	int index = 0;
	int magic_number = 0;
	for (;;){
		if (magic_phrase[index]!='\0'){
			magic_number += ((int) magic_phrase[index]) * index;
		} else {
			return magic_number;
		}
		index++;
	}
	
}

void open_files(char* immagine_invertita){
	out = fopen(immagine_invertita, "w");
	
	if (out == NULL){
		fprintf(stderr, "Error opening files. Execution aborted\n");
		exit(-1);
	}
}

void close_files(){
	fclose(out);
	free(joined);
}

void create_header(){
	char buffer[512];
	columns=1080;
	rows=1900;
	depth=rows/(strlen(joined)-4);
}

void matrix_allocation(){
	int i;

	data = (int**) malloc(rows * sizeof(int*));
	if (data == NULL){
		fprintf(stderr, "Impossibile to allocate the matrix space\n");
		exit(-2);
	}

	for (i=0; i<rows; i++){
		data[i] = (int*)malloc(columns * sizeof(int));
		if (data[i] == NULL){
			printf("Impossibile to allocate pointer to row pixel n: %d\n", i);
			exit(-2);
		}
	}
}

void create_dark_pixel(){
	int i, j;

	for (i=0; i<rows; i++){
		for (j=0; j<columns; j++){
			data[i][j] = 0;
		}
	}
}

void shed_light(int magic_number, bool silence){
	if (!silence){
		srand(magic_number);
		for (int i = 0; i < rows; i++){
			int shadow = rand() % depth;
			int s_c = shadow;
			//for (int j = 0; j < columns; j++){
			for (int j = columns - 1; j >=0; j--) {
				if (s_c > 0) {
					s_c--;
				}
				data[i][j]=s_c;
			}
		}
	}
}


void cast_shadow(){
	int i, j;
	
	fprintf(out, "P2\n");
	fprintf(out, "%d %d\n", rows, columns);
	fprintf(out, "%d\n", depth);
	
	for (i=0; i<rows; i++){
		for (j=0; j<columns; j++){
			fprintf(out, "%d\n", data[i][j]);
		}
	}
}

char* concat(const char *s1, const char *s2){
    char *result = malloc(strlen(s1) + strlen(s2) + 1);
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}
