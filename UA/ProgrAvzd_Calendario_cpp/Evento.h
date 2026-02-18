#include "Fecha.h"

class Evento{
    private:
        Fecha f; // Antes de ejecutar constructores instanciamos nuestro objeto de tipo fecha
        string descripcion;

    public:
        //Constructor por defecto: inicializa la fecha a 1/1/1900 ...
        //y la descripción a "sin descripción"
        Evento();
        //Constructor sobrecargado: inicializa la fecha según los parámetros
        Evento(const Fecha &, const string &);
        //Constructor de copia
        Evento(const Evento&);
        //Operador de asignación
        Evento& operator=(const Evento &);
        //Destructor: pone la fecha a 1/1/1900 y la descripción a "sin descripción"
        ~Evento();

        bool operator==(const Evento &) const;
        //Operador de comparación
        bool operator!=(const Evento &) const;
        //Operador de comparación
        bool operator<(const Evento &) const;
        //Operador de comparación
        bool operator>(const Evento &) const;

        //Devuelve (una copia de) la fecha
        Fecha getFecha() const;
        //Devuelve (una copia de) la descripción
        string getDescripcion() const;
        //Modifica la fecha
        void setFecha(const Fecha &);
        //Modifica la descripción
        bool setDescripcion(const string &);
};