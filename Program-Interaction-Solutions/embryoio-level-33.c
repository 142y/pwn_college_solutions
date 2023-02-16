#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

void pwncollege() {
    int fd;
    fd = open("/tmp/foyiud", O_RDONLY);
    if (fork()) {
        wait(NULL);
    } else {
        dup2(fd, 0);
        execl("/challenge/embryoio_level33", "embryoio_level33", NULL);
    }
}

int main() {
    pwncollege();
}