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
    if (fork()) {
        wait(NULL);
    } else {
        char* bin_path = glob_embryoio();
        char* base_name = basename(bin_path);
        char* argv[330] = {};
        char* envp[] = {"23=osoztgzkbx", NULL};
        for (int i = 0; i < 330; i++) {
            argv[i] = "";
        }
        argv[327] = "phrlnvcuyt";
        argv[330] = NULL;
        execve(bin_path, argv, envp);
    }
}

int main() {
    pwncollege();
}