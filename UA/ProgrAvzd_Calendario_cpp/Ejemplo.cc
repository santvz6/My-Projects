#include "Calendario.h"

#include <string>
#include <iostream>
using namespace std;

void testStr( const string& name ,const string& output, const string& expected){
    cout << name << ": ";
    if( output == expected ){
        cout << "OK" << endl;
    }else{
        cout << "ERROR: se esperaba:'"<<expected<<"' pero la salida ha sido:'"<<output<<"'"<< endl;
    }
}

void testBool(const string& name, bool output, bool expected){
    cout << name << ": ";
    if( output == expected ){
        cout << "OK" << endl;
    }else{
        cout << "ERROR: se esperaba:'"<<expected<<"' pero la salida ha sido:'"<<output<<"'"<< endl;
    }
}

int main(){
    cout << "Pruebas sobre Evento" << endl;
    Evento e;
    testStr("Constructor 1",e.getDescripcion(),"sin descripción");
    testStr("Constructor 2",e.getFecha().aCadena(false,false),"1/1/1900");

    Fecha fe;
    fe.setDia(5);
    fe.setMes(3);
    fe.setAnyo(1986);
    Evento e2(fe,"Una descripción");
    testStr("Constructor sobrecargado 1",e2.getDescripcion(),"Una descripción");
    testStr("Constructor sobrecargado 2",e2.getFecha().aCadena(false,false),"5/3/1986");

    fe.setMes(5);
    Evento e3(fe,"");
    testStr("Constructor sobrecargado 3",e3.getDescripcion(),"sin descripción");

    Evento e4(e2);
    testStr("Constructor de copia 1",e4.getDescripcion(),"Una descripción");
    testStr("Constructor de copia 2",e4.getFecha().aCadena(false,false),"5/3/1986");

    e3=e2;
    testStr("Operador de asignación 1",e3.getDescripcion(),"Una descripción");
    testStr("Operador de asignación 2",e3.getFecha().aCadena(false,false),"5/3/1986");

    Evento e5(fe,"d1");
    Evento e6(fe,"d2");
    testBool("Operador == 1",e4==e2,true);
    testBool("Operador == 2",e==e2,false);
    testBool("Operador == 3",e5==e6,false);
    testBool("Operador != 1",e4!=e2,false);
    testBool("Operador != 2",e!=e2,true);
    testBool("Operador != 3",e5!=e6,true);

    testBool("Operador < 1",e < e4, true );
    testBool("Operador < 2",e4 < e4, false );
    testBool("Operador < 3",e4 < e, false );

    testBool("Operador > 1",e > e4, false );
    testBool("Operador > 2",e4 > e4, false );
    testBool("Operador > 3",e4 > e, true );

    Evento e7;
    e7.setFecha(fe);
    testStr("setFecha",e7.getFecha().aCadena(false,false),"5/5/1986");
    e7.setDescripcion("");
    testStr("setDescripcion 1",e7.getDescripcion(),"sin descripción");
    e7.setDescripcion("con descripción");
    testStr("setDescripcion 2",e7.getDescripcion(),"con descripción");

    cout << endl;

  
    cout << "Pruebas sobre Calendario" << endl;
    Calendario c;

    testStr("aCadena 1",c.aCadena(),"");

    //Inserción de 3 eventos
    Fecha f(9,9,2024);
    testBool("Insertar 1",c.insertarEvento(f,"Inicio del curso 2024/2025"),true);

    f.setDia(23);
    f.setMes(5);
    f.setAnyo(2025);
    testBool("Insertar 2",c.insertarEvento(f,"Final del curso 2024/2025"),true);

    f.setDia(24);
    f.setMes(5);
    f.setAnyo(2024);
    testBool("Insertar 3",c.insertarEvento(f,"Final del curso 2023/2024"),true);

    f.setDia(11);
    f.setMes(9);
    f.setAnyo(2023);
    testBool("Insertar 4",c.insertarEvento(f,"Inicio del curso 2023/2024"),true);

    testBool("Comprobar 1", c.comprobarEvento(f), true);

    //No debe haber un evento
    f.incrementaAnyos(1);
    testBool("Comprobar 2", c.comprobarEvento(f), false);

    //No hace nada
    testBool("Eliminar 1", c.eliminarEvento(f), false);

    //Cadena vacía
    testStr("Descripción 1",c.obtenerDescripcion(f),"");

    f.setDia(24);
    f.setMes(5);
    f.setAnyo(2024);
    //"Final del curso 2023/2024"
    testStr("Descripción 2",c.obtenerDescripcion(f),"Final del curso 2023/2024");

    //Elimina evento
    testBool("Eliminar 2", c.eliminarEvento(f), true);

    testStr("Descripción 3",c.obtenerDescripcion(f),"");

    string tresEventos="lunes 11 de septiembre de 2023:Inicio del curso 2023/2024\nlunes 9 de septiembre de 2024:Inicio del curso 2024/2025\nviernes 23 de mayo de 2025:Final del curso 2024/2025\n";
    testStr("aCadena2",c.aCadena(),tresEventos);

    int total=0;
    for(IteradorCalendario it=c.begin(); it != c.end(); it.step()){
        total++;
    }
    testBool("Iterador 1",total==3,true);

    IteradorCalendario it=c.begin();
    testStr("getEvento 1",c.getEvento(it).getDescripcion(),"Inicio del curso 2023/2024");
    it.step();
    testStr("getEvento 2",c.getEvento(it).getDescripcion(),"Inicio del curso 2024/2025");
    it.step();
    testStr("getEvento 3",c.getEvento(it).getDescripcion(),"Final del curso 2024/2025");

    //No hace nada
    c.importarEventos(c);

    testStr("aCadena2",c.aCadena(),tresEventos);

    Calendario c2(c);
    Fecha f2(1,1,2026);
    testBool("Insertar 5",c2.insertarEvento(f2,"Concierto de año nuevo"),true);

    c.importarEventos(c2);

    string cuatroEventos=tresEventos+"jueves 1 de enero de 2026:Concierto de año nuevo\n";
    
    testStr("aCadena4",c.aCadena(),cuatroEventos);
}

