CFLAGS = -Ivrep-api/remoteApi -Ivrep-api/include -DNON_MATLAB_PARSING -DMAX_EXT_API_CONNECTIONS=255

OS = $(shell uname -s)
ifeq ($(OS), Linux)
	CFLAGS += -D__linux
else
	CFLAGS += -D__APPLE__
endif

default: all

run: all
	./bin/naoClient

clean:
	@rm -f bin/*.*
	@rm -f *.o

all: clean
	g++ $(CFLAGS) -c nao.cpp -o nao.o
	g++ $(CFLAGS) -c main.cpp -o main.o
	gcc $(CFLAGS) -c vrep-api/remoteApi/extApi.c -o extApi.o
	gcc $(CFLAGS) -c vrep-api/remoteApi/extApiPlatform.c -o extApiPlatform.o
	@mkdir -p bin
	g++ extApi.o extApiPlatform.o main.o nao.o -o bin/naoClient -lpthread
