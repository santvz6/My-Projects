
COMP=g++
OPT=-Wall -g -std=c++11

main: Ejemplo.o Fecha.o Evento.o Calendario.o
	$(COMP) $(OPT) -o main Ejemplo.o Fecha.o Evento.o Calendario.o

Ejemplo.o: Ejemplo.cc Fecha.h Evento.h Calendario.h
	$(COMP) $(OPT) -c  Ejemplo.cc

Fecha.o: Fecha.cc Fecha.h
	$(COMP) $(OPT) -c Fecha.cc

Evento.o: Evento.cc Evento.h Fecha.h
	$(COMP) $(OPT) -c Evento.cc
	
Calendario.o: Calendario.cc Calendario.h Fecha.h Evento.h
	$(COMP) $(OPT) -c Calendario.cc

clean:
	rm *.o main