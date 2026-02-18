#include "Evento.h"


class NodoCalendario {

    private:
        Evento evento;
        NodoCalendario* siguiente;


    public:
        //Constructor por defecto
        NodoCalendario();
        //Constructor sobrecargado
        NodoCalendario( NodoCalendario*, const Evento& );
        //Constructor de copia
        NodoCalendario(const NodoCalendario&);
        //Operador de asignación
        NodoCalendario& operator=(const NodoCalendario &);
        //Destructor
        ~NodoCalendario();
        //Devuelve el puntero al siguiente nodo de la lista
        NodoCalendario* getSiguiente() const;
        //Devuelve el evento almacenado en el nodo
        Evento getEvento() const;
        //Modifica el puntero al siguiente nodo de la lista
        void setSiguiente(NodoCalendario* );
        //Modifica el evento
        void setEvento(const Evento& );

};




class IteradorCalendario{
// Puntero a un objeto de tipo NodoCalendario
    private:
        NodoCalendario* pt;
        friend class Calendario;    // De esta manera Calendario puede acceder a NodoCalendario
                                    // Consiguiendo así no formar ciclos de dependencias

    public:
        //Constructor por defecto: puntero a nullptr
        IteradorCalendario();
        //Constructor de copia
        IteradorCalendario(const IteradorCalendario&);
        //Destructor: puntero a nullptr
        ~IteradorCalendario();
        //Operador de asignación
        IteradorCalendario& operator=(const IteradorCalendario&);
        //Incrementa el iterador en un paso
        void step();
        //Operador de comparación
        bool operator==(const IteradorCalendario&) const;
        //Operador de comparación
        bool operator!=(const IteradorCalendario&) const;

};

class Calendario {
    private:
        NodoCalendario *head; 

    public:
        // Constructor por defecto
        Calendario();

        // Constructor de copia
        Calendario(const Calendario&);

        // Operador de asignación
        Calendario& operator=(const Calendario&);

        // Destructor
        ~Calendario();

        //Devuelve un iterador al comienzo del calendario
        IteradorCalendario begin() const;
        
        //Devuelve un iterador al final del calendario: puntero a nullptr
        IteradorCalendario end() const;
        
        //Devuelve (una copia de) el evento apuntado por el iterador
        Evento getEvento(const IteradorCalendario& it) const;
        
        //Añade un evento al calendario. Si ya existía un evento en esa fecha,
        //devuelve false y no hace nada. En caso contrario, devuelve true.
        bool insertarEvento(const Fecha&, const string&);
        
        //Elimina un evento del calendario. Si no había ningún evento asociado a esa fecha,
        //devuelve false y no hace nada. En caso contrario, devuelve true.
        bool eliminarEvento(const Fecha&);
        
        //Comprueba si hay algún evento asociado a la fecha dada
        bool comprobarEvento(const Fecha&) const;
        
        //Obtiene la descripción asociada al evento. Si no hay ningún evento asociado a la fecha,
        //devuelve la cadena vacía
        string obtenerDescripcion(const Fecha&) const;
        
        //Añade todos los eventos del calendario que se pasa como parámetro al calendario actual,
        //excepto los que están en una fecha que ya existe en el calendario
        void importarEventos(const Calendario& );
        
        //Devuelve una cadena con el contenido completo del calendario
        string aCadena() const;
};

