#include <unistd.h>
#include <sys/wait.h>

int pwncollege()
{
        int i = fork();

        if (i == 0)
        {
                char* envp[2] = {"iymohh=qzxdererie", NULL};
                execle("/challenge/embryoio_level32", "embryoio_level32", NULL, envp);
        }
        else
        {
                waitpid(i, NULL, 0);
        }
}

int main()
{
        pwncollege();
}