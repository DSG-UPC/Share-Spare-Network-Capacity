/*
 * Stjepan Groš
 *
 * Example code that retrieves congestion control algorithm used on
 * a specific socket and to change it to reno.
 */

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/tcp.h>
#include <netinet/ip.h>

/*
 * The following constant isn't defined in user space include files so
 * we have to define them "manually".
 */
#define TCP_CA_NAME_MAX		16

int main(int argc, char **argv)
{
	int s, ns, optlen;
	char optval[TCP_CA_NAME_MAX];
	struct sockaddr_in addr, raddr;
	socklen_t nslen = sizeof(struct sockaddr_in);

	/*
	 * What follows is a standard boilerplate code to listen to
	 * some specified port for a new connections. This is a
	 * sequence of: socket/bind/accept system calls.
	 */
	if ((s = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		perror("socket");
		return 1;
	}

	addr.sin_family = AF_INET;
	addr.sin_port = htons(10004);
	addr.sin_addr.s_addr = 0;
	if (bind(s, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)) < 0) {
		perror("bind");
		return 1;
	}

	listen(s, 5);

	/*
	 * Waiting for a connection. You can use telnet client program to
	 * connect to this server (i.e. telnet localhost 10000)
	 */
	if ((ns = accept(s, (struct sockaddr *)&raddr, &nslen)) < 0) {
		perror("accept");
		return 1;
	}

	/*
	 * Now that we established connection, we can retrieve which
	 * congestion control algorithm is used.
	 */
	optlen = TCP_CA_NAME_MAX;
	if (getsockopt(ns, IPPROTO_TCP, TCP_CONGESTION, optval, &optlen) < 0) {
		perror("getsockopt");
		return 1;
	}

	printf("optlen=%d optval=%s\n", optlen, optval);

	/*
	 * We can also set another congestion control algorithm, i.e.
	 * reno in this case.
	 */
	strcpy(optval, "lp");
	optlen = strlen(optval);
	if (setsockopt(ns, IPPROTO_TCP, TCP_CONGESTION, optval, optlen) < 0) {
		perror("setsockopt");
		return 1;
	}

	/*
	 * Retrieve congestion control algorithm so that we check if
	 * it was really changed...
	 */
	optlen = TCP_CA_NAME_MAX;
	if (getsockopt(ns, IPPROTO_TCP, TCP_CONGESTION, optval, &optlen) < 0) {
		perror("getsockopt");
		return 1;
	}

	printf("optlen=%d optval=%s\n", optlen, optval);

	close(s);
}

