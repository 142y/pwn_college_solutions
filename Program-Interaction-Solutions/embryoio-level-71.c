#include <stdlib.h>
#include <unistd.h>

int main() {
    char* argv[110] = {};
    for (int i = 0; i < 110; i++) {
        argv[i] = "";
    }
    argv[0] = "embryoio_level71";
    argv[108] = "cphyfkuiac";
    argv[110] = NULL;
    char* envp[] = {"129=inieelbywd", NULL};
    execve("/challenge/embryoio_level71", argv, envp);
    return 0;
}