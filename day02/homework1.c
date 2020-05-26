#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

double get_time()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + tv.tv_usec * 1e-6;
}

int main(int argc, char** argv)
{
  if (argc != 2) {
    printf("usage: %s N\n", argv[0]);
    return -1;
  }

  int n = atoi(argv[1]);
  double* a = (double*)malloc(n * n * sizeof(double)); // Matrix A
  double* b = (double*)malloc(n * n * sizeof(double)); // Matrix B
  double* c = (double*)malloc(n * n * sizeof(double)); // Matrix C

  // Initialize the matrices to some values.
  int i, j;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      a[i * n + j] = i * n + j; // A[i][j]
      b[i * n + j] = j * n + i; // B[i][j]
      c[i * n + j] = 0; // C[i][j]
    }
  }

  double begin = get_time();

  for(int i=0;i<n;i++){
      for(int j=0;j<n;j++){
          for(int k=0;k<n;k++){
              c[i*n+j]+=a[i*n+k]*b[k*n+j];
          }
      }
  }

  double end = get_time();
  printf("%.10lf\n", end - begin);
  free(a);
  free(b);
  free(c);
  return 0;
}