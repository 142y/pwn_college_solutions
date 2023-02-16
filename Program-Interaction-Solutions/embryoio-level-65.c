#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <glob.h>
#include <libgen.h>
#include <string.h>

char* glob_embryoio() {
    glob_t result;
    glob("/challenge/em*", 0, NULL, &result);
    return result.gl_pathv[0];
}

int pwncollege() {
        int fd1[2];
        int fd2[2];
        if (pipe(fd1) == -1) {
                printf("Error occured with opening a pipe1!\n");
                return 1;
        }
        if (pipe(fd2) == -1) {
                printf("Error occured with opening a pipe2!\n");
                return 1;
        }
        if (fork()){
                if(fork()) {
                        /* Explanation - https://stackoverflow.com/questions/1720535/practical-examples-use-dup-or-dup2
                        One example use would be I/O redirection. For this you fork a child process and close the stdin or stdout file descriptors (0 and 1) and then you do a 
                        dup() on another filedescriptor of your choice which will now be mapped to the lowest available file descriptor, which is in this case 0 or 1. Using this you 
                        can now exec any child process which is possibly unaware of your application and whenever the child writes on the stdout (or reads from stdin, whatever you 
                        configured) the data gets written on the provided filedescriptor instead. 
                        Shells use this to implement commands with pipes, e.g. /bin/ls | more by connecting the stdout of one process to the stdin of the other.*/
                        sleep(1);
                        close(fd1[0]);

                        char pass[10] = "kficcenn\n";

                        write(fd1[1], pass, strlen(pass));
                        close(fd1[1]);

                        wait(NULL);
                } else {
                        close(fd1[1]);

                        dup2(fd1[0], 0);
                        
                        close(fd2[0]);
                        dup2(fd2[1], 1);
                        dup2(fd2[1], 2);

                        execlp("rev", "rev", NULL);
                }
        }
        else {
                close(fd1[0]);
                close(fd1[1]);
                close(fd2[1]);
                dup2(fd2[0], 0);

                char* envp[] = {NULL};
                char* bin_path = glob_embryoio();
                char* base_name = basename(bin_path);

                execle(bin_path, base_name, NULL, envp);
        }
    }

int main() {
    pwncollege();
}