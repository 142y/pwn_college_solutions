#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

void pwncollege() {
    int fd;
    fd = open("/tmp/dylgre", O_WRONLY | O_CREAT);
    if (fork()) {
        wait(NULL);
    } else {
        dup2(fd, 1); // stdout
        dup2(fd, 2); // stderr
        execl("/challenge/embryoio_level34", "embryoio_level34", NULL);
    }
}

int main() {
    pwncollege();
}