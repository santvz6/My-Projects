#include "Fecha.h" 

Fecha::Fecha(){
    dia = 1;
    mes = 1;
    año = 1900;
}

Fecha::Fecha(int diai,int mesi,int añoi){
    if (esValida(diai, mesi, añoi)){
        dia = diai;
        mes = mesi;
        año = añoi;
    }
    
    else{
        dia = 1;
        mes = 1;
        año = 1900;
    }
}

Fecha::~Fecha(){
    dia = 1;
    mes = 1;
    año = 1900;
}

Fecha::Fecha(const Fecha &obj) {
    dia = obj.dia;
    mes = obj.mes;
    año = obj.año;
}

Fecha& Fecha::operator=(const Fecha &obj) {

    // this -> dirección de memoria del objeto
    // *this -> objeto real

    // Evitar la autoasignación (comparamos dirección del objeto actual con la del objeto argumento)
    if (this!=&obj){
        (*this).~Fecha();
        dia = obj.dia;
        mes = obj.mes;
        año = obj.año;
    }

    // Devolver la referencia al objeto actual
    return (*this);
}

bool Fecha::operator==(const Fecha &obj) const{
    if(dia == obj.dia && mes == obj.mes && año == obj.año){
        return true;
    }    
    return false;
}

bool Fecha::operator!=(const Fecha &obj) const{
    if(dia != obj.dia || mes != obj.mes || año != obj.año){
        return true;
    }    
    return false;
}

bool Fecha::operator<(const Fecha& obj) const {
    if (año < obj.año) return true;
    if (año == obj.año && mes < obj.mes) return true;
    if (año == obj.año && mes == obj.mes && dia < obj.dia) return true;
    return false;
}

bool Fecha::operator>(const Fecha& obj) const {
    if (año > obj.año) return true;
    if (año == obj.año && mes > obj.mes) return true;
    if (año == obj.año && mes == obj.mes && dia > obj.dia) return true;
    return false;
}


int Fecha::getDia() const{
    return dia;
}

int Fecha::getMes() const{
    return mes;
}

int Fecha::getAnyo() const{
    return año;
}

bool Fecha::setDia(int diai){
    if (esValida(diai, mes, año)){
        dia = diai;
        return true;
    }
    return false;
}

bool Fecha::setMes(int mesi){
    if (esValida(dia, mesi, año)){
        mes = mesi;
        return true;
    }
    return false;
}

bool Fecha::setAnyo(int añoi){
    if (esValida(dia, mes, añoi)){
        año = añoi;
        return true;
    }
    return false;
}

bool Fecha::incrementaAnyos(int inc){
    int diai = dia;
    int mesi = mes;
    int añoi = año;
    if (esValida(dia, mes, año+inc)){
        año += inc;
        return true;
    }
    return resetAtributos(diai, mesi, añoi);
}
    
bool Fecha::incrementaMeses(int inc){
    int diai = dia;
    int mesi = mes;
    int añoi = año;

    while (inc != 0){
        // Incremento Positivo
        if (inc>0){
            if (inc > 12-mes){
                mes = 1;
                año++;
                inc -= 12 - mes + 1; // +1: Establecemos el mes a 1
            }
            else{
                mes += inc;
                inc = 0;
            }
        }
        // Incremento Negativo
        else{
            if(-inc >= mes){
                mes = 12;
                año --;
                inc -= mes;
            }
            else{
                mes += inc;
                inc = 0;
            }
        }
    }

    if (esValida(dia, mes, año))
        return true;
    else
        return resetAtributos(diai, mesi, añoi);
}

bool Fecha::incrementaDias(int inc){
    int diai = dia;
    int mesi = mes;
    int añoi = año;

    while (inc!=0){
        // INCREMENTO POSITIVO
        if (inc > 0){
            // AÑOS
            if (esBisiesto(año) && inc >= 366){
                año ++;
                inc -= 366;
            }       
            else if (!esBisiesto(año) && inc >= 365){
                año ++;
                inc -= 365;
            }  
            else{
                // MESES
                int mesact = getMesCant(mes, año);
                if (inc > mesact - dia){
                    if (mes != 12){
                        inc -= mesact - dia + 1;
                        mes ++;
                        dia = 1;   
                    }
                    else{
                        inc -= 31 - dia + 1;
                        mes = dia = 1;
                        año++;
                    }
                }
                else{
                    // DÍAS  
                    dia += inc;
                    inc = 0;
                    }
            }  
        }
        // INCREMENTO NEGATIVO
        else{
            // AÑOS
            if (esBisiesto(año) && -inc >= 366 && (mes > 2 || (mes == 2 && dia == 29))){    
                año --;
                inc += 366;
            }       
            else if ((!esBisiesto(año) && -inc >= 365) || (esBisiesto(año) && mes <= 2 && !(mes == 2 && dia ==29))){
                año --;
                inc += 365;
            }  
            else{
                // MESES
                if (-inc >= dia){
                    if (mes != 1){
                        inc += dia; // Quitamos al mes lo que queda
                        mes--;
                        dia = getMesCant(mes, año);     
                    }
                    else{
                        inc += dia;
                        mes = 12;
                        año--;
                        dia = getMesCant(mes, año);
                    }
                } 
                else{
                    dia += inc;
                    inc = 0;
                }
            }  
        }
    }

    if (esValida(dia, mes, año)){
        return true;
    }
    else{
        resetAtributos(diai, mesi, añoi);
        return false;
    }
    
}

bool Fecha::esValida(int diai ,int mesi, int añoi){
    int tipo_mes = getMesCant(mesi, añoi);
    if (0 < diai && diai <= tipo_mes && 0 < mesi && mesi <= 12 && añoi >= 1900)
        return true;
    return false;
}

bool Fecha::esBisiesto(int año){
    if (año % 4 == 0) {
        if (año % 100 == 0) {
            // 4, 100 y 400 > Sí Bisiesto
            if (año % 400 == 0) {
                return true;
            } 
            // 4 y 100 > No Bisiesto
            else {
                return false;
            }
        
        } 
        // sólo 4 > Sí Bisiesto
        else {
            return true;
        }
    }
    // No es divisible entre 4 > No Bisiesto
    else {
        return false;
    }
}

int Fecha::getMesCant(int mes, int año){
    int meses31[] = {1, 3, 5, 7, 8, 10, 12};
    int len_meses31 = sizeof(meses31) / sizeof(meses31[0]);
    if (mes==2 && esBisiesto(año))
        return 29;
    else if (mes==2 && !esBisiesto(año))
        return 28;
    for(int i=0; i < len_meses31; i++){
        if (mes==meses31[i])
            return 31;
    }
    return 30;
}

bool Fecha::resetAtributos(int diai, int mesi, int añoi){
    // No usamos set, porque esas fechas ya eran válidas en su momento
    // Si cambiamos día, mes y año uno a uno, puede ocasionarse un error de fecha
    dia = diai;
    mes = mesi;
    año = añoi;
    return false;
}

int Fecha::getDiaSemana(){
    int dias_transc = 0;
    int diai = dia;
    int mesi = mes;
    int añoi = año;

    while (true){
        if (incrementaDias(-1)){ // cuando devuelva False (ha llegado a menos de 1900)
            dias_transc++;
        }
        else{
            resetAtributos(diai, mesi, añoi);
            return dias_transc%7;
        }
    }
}

string Fecha::aCadena(bool larga, bool conDia) {
    string cadena;
    string dias_semana[] = {"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"};
    string meses[] = {"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                    "agosto", "septiembre", "octubre", "noviembre", "diciembre"};

    if (larga) {
        cadena = to_string(dia) + " de " + meses[mes-1] + " de " + to_string(año);
        if (conDia) {
            cadena = dias_semana[getDiaSemana()] + " " + cadena;
        }
    } 
    else {
        cadena = to_string(dia) + "/" + to_string(mes) + "/" + to_string(año);
        if (conDia){
            cadena = dias_semana[getDiaSemana()] + " " + cadena;
        } 
    }
    return cadena;
}