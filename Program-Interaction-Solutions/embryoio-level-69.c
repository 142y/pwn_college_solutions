#include <stdlib.h>
#include <unistd.h>

int main() {
    char* argv[] = {NULL};
    char* env[] = {NULL};
    execve("/challenge/embryoio_level69", argv, env);
    return 0;
}