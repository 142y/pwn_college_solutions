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
        char* argv[110] = {};
        for (int i = 0; i < 110; i++) {
            argv[i] = "";
        }
        argv[101] = "slwqlpkoln";
        argv[110] = NULL;
        execve(bin_path, argv, NULL);
    }
}

int main() {
    pwncollege();
}