#include <stdlib.h>
#include <unistd.h>
#include <glob.h>
#include <sys/wait.h>
#include <libgen.h>
#include <fcntl.h>

char* glob_embryoio() {
    glob_t result;
    glob("/challenge/em*", 0, NULL, &result);
    return result.gl_pathv[0];
}

void pwncollege() {
    mkfifo("/tmp/fifo", 0666);
    if (fork()) {
        int fd = open("/tmp/fifo", O_RDONLY);
        char buf[4096] = {};
        read(fd, buf, 4096);
        write(1, buf, 4096);
        wait(NULL);
    } else {
        int fd = open("/tmp/fifo", O_WRONLY);
        dup2(fd, 1);
        dup2(fd, 2);
        char* bin_path = glob_embryoio();
        execve(bin_path, NULL, NULL);
    }
}

int main() {
    pwncollege();
}