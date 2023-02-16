#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <glob.h>
#include <libgen.h>

char* glob_embryoio() {
        glob_t result;
        glob("/challenge/em*", 0, NULL, &result);
        return result.gl_pathv[0];
}

int pwncollege() {
        int fd[2];
        if (pipe(fd) == -1) {
                printf("Error occured with opening a pipe!\n");
                return 1;
        }
        if (fork()){
                if(!fork()) {
                        dup2(fd[0], 0);
                        execlp("cat", "cat", NULL);
                }
                wait(NULL);
        }
        else {
                dup2(fd[1], 1);
                dup2(fd[1], 2);

                char* envp[] = {NULL};
                char* bin_path = glob_embryoio();
                char* base_name = basename(bin_path);

                sleep(1);
                execle(bin_path, base_name, NULL, envp);
        }
    }

int main() {
    pwncollege();
}