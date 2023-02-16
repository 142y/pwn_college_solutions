#include <unistd.h>
#include <sys/wait.h>

int pwncollege()
{
        int i = fork();

        if (i == 0)
        {
                execve("/challenge/embryoio_level29", NULL, NULL);
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