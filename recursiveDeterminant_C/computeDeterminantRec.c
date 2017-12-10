#include <stdio.h>
#define NMAX 255


int n, i, j;
double matrix[NMAX][NMAX];

void readInput() {
    scanf("%d", &n);
    for(i = 0; i<n; i++) {
        for(j = 0; j<n; j++) {
            scanf("%lf", &matrix[i][j]);
        }
    }
}

void print_matrix(double matrix[NMAX][NMAX], int n) {


    for(i = 0; i<n; i++) {
        for(j = 0; j<n; j++) {
            printf("%lf  ", matrix[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

double det2x2(double matrix[NMAX][NMAX], int end){
    return matrix[end - 1][end - 1] * matrix[end][end] - matrix[end - 1][end] * matrix[end][end - 1];
}

void add_col1_to_col2(int col1, int col2, double matrix[NMAX][NMAX], int n) {
    for(i = 0; i<n; i++) {
        matrix[i][col1] += matrix[i][col2];
    }
}

void diff_col1_to_col2(int col1, int col2, double matrix[NMAX][NMAX], int n) {
    for(i = 0; i<n; i++) {
        matrix[i][col1] -= matrix[i][col2];
    }
}


double computeDeterminant(double matrix[NMAX][NMAX], int start, int end) {

    if(start == end - 1) {
        return det2x2(matrix, end);
    }
    else {
        double prod = 1;
        if (matrix[start][start] == 0) {
            int found = 0;
            for(i = start; i<=end; i++) {
                if(matrix[start][i] != 0) {
                    add_col1_to_col2(start, i, matrix, end + 1);
                    found = 1;
                }
            }
            if(found == 0) {
                return 0;
                return;
            }
        }
        for(i = start + 1; i<=end; i++) {
                double div = matrix[start][i];
                prod *= (double)matrix[start][start]/div;
            for(j = start; j<=end; j++) {
               if(div != 0) {
                    matrix[j][i] = (double)(matrix[j][i]*matrix[start][start])/div;
               }
            }
        }
        for(j = start + 1; j <= end; j++) {
            int col = j;
            diff_col1_to_col2(col, start, matrix, end + 1);
        }
        print_matrix(matrix, n);
        return matrix[start][start]/prod*computeDeterminant(matrix, start + 1, end);
    }

}

int main() {
   FILE *f = freopen("inputFile.txt", "r", stdin);
   FILE *g = freopen("outputFile.txt", "w", stdout);
   readInput();
   printf("%lf", computeDeterminant(matrix, 0, n - 1));
   return 0;
}
