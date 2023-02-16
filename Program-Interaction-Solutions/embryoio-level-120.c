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
        int fd1 = open("/tmp/fifo", O_WRONLY);
        write(fd1, "gfqvsyib", 8);
        close(fd1);
        wait(NULL);

    } else {
        int fd1 = open("/tmp/fifo", O_RDONLY);
        dup2(fd1, 152);
        char* bin_path = glob_embryoio();
        execve(bin_path, NULL, NULL);
    }
}

int main() {
    pwncollege();
}