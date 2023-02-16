#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <glob.h>

char* glob_embryoio() {
    glob_t result;
    glob("/challenge/em*", 0, NULL, &result);
    return result.gl_pathv[0];
}

int pwncollege() {
    if (!fork()) {
        char* binary = glob_embryoio();
        execl(binary, "challenge", NULL);
    }

    sleep(1);
    
    int s = socket(AF_INET, SOCK_STREAM, 0);
    int client_fd;
    struct sockaddr_in servaddr;
    char buffer[1024] = {};
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(1678);

    if (s < 0) {
        printf("\nSocket creation error\n");
        return -1;
    }

    if ((client_fd = connect(s, (const struct sockaddr *)&servaddr, sizeof(servaddr))) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }
    
    sleep(1);
    char sock_fd[16] = {};
    sprintf(sock_fd, "%d", s);
    if (!fork()) {
        execl("/usr/bin/python", "python", "embryoio-level-142.py", sock_fd, NULL);
    }
    close(s);
    while(wait(NULL) > 0);
}

int main() {
    pwncollege();
}