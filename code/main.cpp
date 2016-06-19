#include <iostream>
#include "nao.h"
extern "C" {
    #include "extApi.h"
}

using namespace std;

int main(int argc, char *argv[]) {
	int portNb=25000;

	int clientID=simxStart((simxChar*)"127.0.0.1",portNb,true,true,2000,5);
	if (clientID!=-1) {
		cout << "Connected\n";

		NAO nao;
		nao.start(clientID);

		simxFinish(clientID);
	} else {
		cout << "Not connected\n";
	}
	return(0);
}
