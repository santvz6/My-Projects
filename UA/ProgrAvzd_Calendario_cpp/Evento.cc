#include "Evento.h"

// Constructor por defecto
Evento::Evento() {
    f = Fecha(1, 1, 1900);
    descripcion = "sin descripción";
}

// Constructor sobrecargado: inicializa la fecha según los parám    etros
Evento::Evento(const Fecha& obj, const string& desc) {
    f = obj;
    setDescripcion(desc); // se encargará si es un string vacío
}

// Constructor de copia
Evento::Evento(const Evento& obj) {
    f = obj.f;
    descripcion = obj.descripcion;
}

// Operador de asignación
Evento& Evento::operator=(const Evento& obj) {
    if (this != &obj) {  // Evitamos la autoasignación
        f = obj.f;
        descripcion = obj.descripcion;
    }
    // Devolvemos el objeto
    return (*this);
}

bool Evento::operator==(const Evento &obj) const{
    return (f == obj.f && descripcion == obj.descripcion);

}

// Operador de comparación
bool Evento::operator!=(const Evento &obj) const{
    return !(*this == obj); // reutilizamos la lógica de operator ==
}

//Operador de comparación
bool Evento::operator<(const Evento &obj) const{
    return (f < obj.f);
}
//Operador de comparación
bool Evento::operator>(const Evento &obj) const{
    return (f > obj.f);
}

// Destructor
Evento::~Evento() {
    f = Fecha(1, 1, 1900); 
    descripcion = "sin descripción";
}

// Devuelve (una copia de) la fecha
// Lo pasamos por valor para mantener el valor original
Fecha Evento::getFecha() const {
    return f;
}

// Devuelve (una copia de) la descripción
// Lo pasamos por valor para no modificar el valor original
string Evento::getDescripcion() const {
    return descripcion;
}

// Modifica la fecha
void Evento::setFecha(const Fecha& obj) {
    f = obj;
}

// Modifica la descripción
bool Evento::setDescripcion(const string& nuevaDesc) {
    if (nuevaDesc != "") {
        descripcion = nuevaDesc;
        return true;
    }
    descripcion = "sin descripción";
    return false;
}
