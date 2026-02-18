#include "Calendario.h"

// ----------------------------------------------- CALENDARIO  ----------------------------------------------- //


Calendario::Calendario(){ head  = nullptr; } // Constructor por defecto

// Constructor de copia
Calendario::Calendario(const Calendario& obj) {
    head = nullptr; // I S
    
    // punteros auxiliares de Nodo Calendario
    NodoCalendario* actual = obj.head;
    NodoCalendario* anterior = nullptr;

    // Recorremos la lista enlazada hasta el último elemento (actual == nullptr)
    while (actual != nullptr) {

        // Creamos un nuevo nodo copiando el evento del nodo original
        NodoCalendario* nuevoNodo = new NodoCalendario(nullptr, actual->getEvento());
        
        if (anterior == nullptr) {
            head = nuevoNodo;  // Si es el primer nodo, lo asignamos como head
        } else {
            // Al nodo Anterior le establecemos como siguiente el nuevo Nodo
            anterior->setSiguiente(nuevoNodo); 
        }
        
        anterior = nuevoNodo;               // Nos servirá para establecer el siguiente de cada Nodo
        actual = actual->getSiguiente();    // Pasamos al siguiente nodo en la lista original
    }
}

// Operador de asignación
Calendario& Calendario::operator=(const Calendario& obj) {
    if (this != &obj) {  // Comprobación de autoasignación
        //this->~Calendario();  // Liberamos la memoria actual

        head = nullptr;  // Inicializamos la cabeza como nullptr

        // Recorremos la lista del objeto 'obj' y copiamos sus nodos
        NodoCalendario* actual = obj.head;
        NodoCalendario* anterior = nullptr;
    
        while (actual != nullptr) {
            NodoCalendario* nuevoNodo = new NodoCalendario(nullptr, actual->getEvento());
            if (anterior == nullptr) {
                head = nuevoNodo;
            } else {
                anterior->setSiguiente(nuevoNodo);
            }
            anterior = nuevoNodo;
            actual = actual->getSiguiente();
        }
    }
    return *this;  // Retornamos el objeto actual
}

// Destructor
Calendario::~Calendario() {
    NodoCalendario* actual = head;
    while (actual) {
        NodoCalendario* siguiente = actual->getSiguiente();
        delete actual;  // Liberamos cada nodo
        actual = siguiente;
    }
}

//Devuelve un iterador al comienzo del calendario
IteradorCalendario Calendario::begin() const {
    IteradorCalendario it;
    it.pt = head;  // Apunta al primer nodo
    return it;
}

//Devuelve un iterador al final del calendario: puntero a nullptr
IteradorCalendario Calendario::end() const {
    IteradorCalendario it;
    it.pt = nullptr;  // Apunta a nullptr
    return it;
}

//Devuelve el evento apuntado por el iterador
Evento Calendario :: getEvento(const IteradorCalendario& it) const{
    return it.pt -> getEvento();
}


bool Calendario::insertarEvento(const Fecha& objFecha, const std::string& descripcion) {
    // Crear una copia de la fecha a insertar
    Fecha f = objFecha;

    /*
    Tenemos dos posibles casos:
        * La lista enlazada está vacía
        * La lista enlazada no está vacía
    */

    // Comprobar si ya existe un evento en esa fecha
    if (comprobarEvento(f)) return false; // Si ya existe, no insertamos y devolvemos false

    // Crear el evento que queremos insertar
    Evento eventoIntroducido(f, descripcion);
    NodoCalendario* nuevoNodo = new NodoCalendario(nullptr, eventoIntroducido);

    // La lista enlazada está vacía -> head ==nullptr
    if (head==nullptr || head->getEvento().getFecha() > f) { 
        nuevoNodo->setSiguiente(head);
        head = nuevoNodo;
        return true;
    }

    // La lista no está vacía, la recorremos con un puntero auxiliar del Nodo
    NodoCalendario* actual = head;
    while (actual->getSiguiente() && actual->getSiguiente()->getEvento().getFecha() < f) {
        actual = actual->getSiguiente();  
    }

    nuevoNodo->setSiguiente(actual->getSiguiente());
    actual->setSiguiente(nuevoNodo);
    return true;
}

// Eliminar un evento del calendario
bool Calendario :: eliminarEvento(const Fecha& fecha) {
    if (!head) return false; // No hay ningún nodo

    // El primer nodo coincide con la fecha
    if (head->getEvento().getFecha() == fecha) {
        NodoCalendario* temporal = head;
        head = head->getSiguiente();
        delete temporal;
        return true;
    }

    // Recorremos todos los nodos hasta que encontremos una fecha que coincida o hasta llegar al final
    NodoCalendario* actual = head;
    while (actual->getSiguiente() && actual->getSiguiente()->getEvento().getFecha() != fecha) {
        actual = actual->getSiguiente();
    }

    // Comprobamos que no hemos llegado al final ( != nullptr)
    if (actual->getSiguiente()) {
        NodoCalendario* temporal = actual->getSiguiente();
        actual->setSiguiente(temporal->getSiguiente());
        delete temporal;
        return true;
    }
    return false;
}

// Comprobar si existe un evento en una fecha
bool Calendario :: comprobarEvento(const Fecha& fecha) const {
    NodoCalendario* actual = head;
    while (actual) {
        if (actual->getEvento().getFecha() == fecha) return true;
        actual = actual->getSiguiente();
    }
    return false;
}

//Obtiene la descripción asociada al evento. Si no hay ningún evento asociado a la fecha,
//devuelve la cadena vacía
string Calendario :: obtenerDescripcion(const Fecha& obj) const{
    NodoCalendario* actual = head;
    while (actual) {
        if (actual->getEvento().getFecha() == obj) {
            return actual->getEvento().getDescripcion();  // Retorna la descripción si coincide
        }
        actual = actual->getSiguiente();
    }
    return "";  // Si no hay evento, retorna una cadena vacía
}

//Añade todos los eventos del calendario que se pasa como parámetro al calendario actual,
//excepto los que están en una fecha que ya existe en el calendario
void Calendario :: importarEventos(const Calendario& obj){
    //obj metodo imposible tio
}


string Calendario :: aCadena() const {
    NodoCalendario* actual = head;
    string cadena; 

    while (actual) {
        
        cadena += actual->getEvento().getFecha().aCadena(true, true) + ":" + actual->getEvento().getDescripcion() + "\n";
        actual = actual->getSiguiente();    
    }
    
    return cadena;  
}

// ----------------------------------------------- NODO CALENDARIO ----------------------------------------------- //


//Constructor por defecto
NodoCalendario :: NodoCalendario(){
    Evento();
    siguiente = nullptr;
    // No hace falta hacer nada con evento, ya se instancia por defecto
}

//Constructor sobrecargado
NodoCalendario :: NodoCalendario(NodoCalendario* ptr, const Evento& obj) {
    siguiente = ptr;
    evento = obj;
}

//Constructor de copia
NodoCalendario :: NodoCalendario(const NodoCalendario& obj) {
    siguiente = obj.siguiente;
    evento = obj.evento;
}

//Operador de asignación
NodoCalendario& NodoCalendario :: operator=(const NodoCalendario& obj) {
    if (this != &obj) {  // Comprobación de autoasignación
        (*this).~NodoCalendario();
        siguiente = obj.siguiente;
        evento = obj.evento;
    }
    return (*this); // devolvemos el valor del puntero
}

//Destructor
NodoCalendario :: ~NodoCalendario(){
}

//Devuelve el puntero al siguiente nodo de la lista
NodoCalendario* NodoCalendario :: getSiguiente() const {
    return siguiente; // siguiente ya es un puntero
}

//Devuelve el evento almacenado en el nodo
Evento NodoCalendario :: getEvento() const {
    return evento;
}

//Modifica el puntero al siguiente nodo de la lista
void NodoCalendario :: setSiguiente(NodoCalendario* ptr) {
    siguiente = ptr;
}

//Modifica el evento
void NodoCalendario :: setEvento(const Evento& obj){
    evento = obj;
}

// ----------------------------------------------- ITERADOR CALENDARIO  ----------------------------------------------- //

//Constructor por defecto: puntero a nullptr
IteradorCalendario :: IteradorCalendario(){
    pt = nullptr;
}
//Constructor de copia
IteradorCalendario :: IteradorCalendario(const IteradorCalendario& obj){
    pt = obj.pt;
}
//Destructor: puntero a nullptr
IteradorCalendario :: ~IteradorCalendario(){
}
//Operador de asignación
IteradorCalendario& IteradorCalendario :: operator=(const IteradorCalendario& obj){
    if (this != &obj){
        (*this).~IteradorCalendario();
        pt = obj.pt;
    }
    return (*this);
}
//Incrementa el iterador en un paso
void IteradorCalendario :: step(){
    if (pt) pt = pt->getSiguiente();
}
//Operador de comparación
bool IteradorCalendario :: operator==(const IteradorCalendario& obj) const{
    return (pt == obj.pt);
}
//Operador de comparación
bool IteradorCalendario :: operator!=(const IteradorCalendario& obj) const{
    return !(*this == obj);
}
