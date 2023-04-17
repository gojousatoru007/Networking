#include <stdio.h>
#include <winsock2.h>
#include <string.h>
#include <stdlib.h>

#define MAX_INPUT_SIZE 256

int main(int argc, char *argv[])
{
    WSADATA wsaData;
    int sockfd, portnum, n;
    struct sockaddr_in server_addr;

    char inputbuf[MAX_INPUT_SIZE];
    if (argc < 3) {
       fprintf(stderr,"usage %s <server-ip-addr> <server-port>\n", argv[0]);
       exit(0);
    }

    portnum = atoi(argv[2]);

    /* Initialize Winsock */
    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        fprintf(stderr, "WSAStartup failed\n");
        exit(1);
    }

    /* Create client socket */
    sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockfd == INVALID_SOCKET) {
        fprintf(stderr, "ERROR opening socket\n");
        WSACleanup();
        exit(1);
    }

    /* Fill in server address */
    memset((char *) &server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(argv[1]);
    server_addr.sin_port = htons(portnum);

    /* Connect to server */
    if (connect(sockfd,(struct sockaddr *)&server_addr,sizeof(server_addr)) < 0) 
      {
	fprintf(stderr, "ERROR connecting\n");
	closesocket(sockfd);
	WSACleanup();
	exit(1);
      }
    printf("Connected to server\n");
    
    do
      {
	/* Ask user for message to send to server */
	printf("Please enter the message to the server: ");
	memset(inputbuf, 0, MAX_INPUT_SIZE);
	fgets(inputbuf,MAX_INPUT_SIZE-1,stdin);
	
	/* Write to server */
	n = send(sockfd,inputbuf,strlen(inputbuf), 0);
	if (n < 0) 
	  {
	    fprintf(stderr, "ERROR writing to socket\n");
	    closesocket(sockfd);
	    WSACleanup();
	    exit(1);
	  }
	
	/* Read reply */
	memset(inputbuf, 0, MAX_INPUT_SIZE);
	n = recv(sockfd,inputbuf,(MAX_INPUT_SIZE-1), 0);
	if (n < 0) 
	  {
	    fprintf(stderr, "ERROR reading from socket\n");
	    closesocket(sockfd);
	    WSACleanup();
	    exit(1);
	  }
	printf("Server replied: %s\n",inputbuf);

      } while(1);

    closesocket(sockfd);
    WSACleanup();
    return 0;
}
