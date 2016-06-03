#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

int
fib(int n) {
  switch (n) {
    case 0:
      return 0;
    case 1:
      return 1;
    default:
      return fib(n-1) + fib(n-2);
        }
}

void
server() {
  int server_sock = socket(AF_INET, SOCK_STREAM, 0);
  int childfd;
  int optval = 1;
  int n;
  char buf[10];
  int val;
  struct sockaddr_in my_addr;
  struct sockaddr_in clientaddr;
  unsigned int clientlen = sizeof(clientaddr);
  setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));

  memset(&my_addr, 0, sizeof(my_addr));

  my_addr.sin_family = AF_INET;
  my_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  my_addr.sin_port = htons((unsigned short)9090);
    
  bind(server_sock, (struct sockaddr *)&my_addr, sizeof(my_addr));
    
  listen(server_sock, 5);

  while(1) {
    childfd = accept(server_sock, (struct sockaddr *) &clientaddr, &clientlen);
    while (1) {
      memset(buf, 0, sizeof(buf));
      n = read(childfd,  buf, 10);
      buf[n+1] = '\0';
      val = atoi(buf);
      memset(buf, 0, sizeof(buf));
      sprintf(buf, "%d", fib(val));
      write(childfd, buf, 10);
    }
  }
}


int
main() {
  server();
  return 0;
    }
