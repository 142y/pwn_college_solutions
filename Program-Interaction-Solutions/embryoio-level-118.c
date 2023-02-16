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
    mkfifo("/tmp/fifo_stdin", 0666);
    mkfifo("/tmp/fifo_stdout", 0666);

    if (fork()) {
        int fd1 = open("/tmp/fifo_stdin", O_WRONLY);
        int fd2 = open("/tmp/fifo_stdout", O_RDONLY);
        write(fd1, "evjkclja", 8);
        close(fd1);
        wait(NULL);

        char buf[4096] = {};
        read(fd2, buf, 4096);
        write(1, buf, 4096);
    } else {
        int fd1 = open("/tmp/fifo_stdin", O_RDONLY);
        int fd2 = open("/tmp/fifo_stdout", O_WRONLY);
        dup2(fd1, 0);
        dup2(fd2, 1);
        char* bin_path = glob_embryoio();
        execve(bin_path, NULL, NULL);
    }
}

int main() {
    pwncollege();
}