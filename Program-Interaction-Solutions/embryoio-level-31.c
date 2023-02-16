#include <unistd.h>
#include <sys/wait.h>

int pwncollege()
{
	int i = fork();

	if (i == 0)
	{
		execl("/challenge/embryoio_level31", "embryoio_level31", "befntrcaez", NULL);
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
