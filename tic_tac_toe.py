import copy
from sys import stdin


def sucesores(ej):
    """ Conocer todas las posibles siguientes jugadas 
        Parameters:
        ej: TEstado

        Returns:
        secuencia de estados."""
    return ej.hijos


class Busqueda:
    def inicial(self):
        """ Conocer el estado del tablero inicial 
            Returns:
            e: TEstado"""
        return  TEstado([['_','_','_'],['_','_','_'],['_','_','_']],Jugador('X'))

    def jugador(self, ej):
        """ Conocer la identificación del jugador en turno.
            Parameters:
            ej: TEstado
            
            Returns:
            j: TJugador"""
        j = ej.get_jugador()
        return j

    def utilidad(self, e, j):
        """Conocer el valor estático de un tablero para un jugador
            
            Parameters:
            e: TEstado
            j: Tjugador
            
            Returns:
            int: valor del tablero para j """
        return e.valor

    
    def max_value(self,t):
        """     
            Parameters:
            t: TEstado

            Returns:
            Retorna la jugada con la maxima funcion de utilidad de un etsado t
        """
        if t.esFinal:
          return self.utilidad(t,t.jugador)
        else:
            maximo=-float("inf")
            for fila in range(3):
                for columna in range(3):
                    if t.tablero[fila][columna] == '_':
                        t.tablero[fila][columna] = t.jugador.get_id()
                        proximo = Jugador("X") if t.jugador.get_id()=="O" else Jugador("O")
                        maximo=max(maximo,self.min_value(TEstado(t.tablero,proximo)))
                        t.tablero[fila][columna] = '_'
            t.valor = maximo     
            t.esFinal=True
            return t.valor
    
    def min_value(self,t):
        """     
            Parameters:
            t: TEstado

            Returns:
            Retorna la jugada con la minima funcion de utilidad de un etsado t
        """
        if t.esFinal:
          return self.utilidad(t,t.jugador)
        else:
            minimo=float("inf")
            for fila in range(3):
                for columna in range(3):
                    if t.tablero[fila][columna] == '_':
                        t.tablero[fila][columna] = t.jugador.get_id()
                        proximo = Jugador("X") if t.jugador.get_id()=="O" else Jugador("O")
                        minimo=min(minimo,self.max_value(TEstado(t.tablero,proximo)))
                        t.tablero[fila][columna] = '_'
            t.valor = minimo
            t.esFinal=True
            return t.valor

                
            
        
    def minMax (self,ej, j):
        """ Conocer el valor dinámico de un estado de juego para un jugado

          Parameters:

          ej: TEstado
          j: TJugador
          m: int

          Returns:

           v: int
        """
        #J1 -> Max
        #J2 -> Min
        
        if j.get_id()=="X":
          return self.max_value(ej)
        if j.get_id()=="O":
          return self.min_value(ej)

class Jugador:
  def __init__(self, id):
    self.id=id
  def __str__(self):
    return self.id
  def get_id(self):
    return self.id

  def set_id(self, id):
    self.id = id





#Estado de un tablero de triqui
class TEstado:
    def __init__(self,tablero, jugador,utilidad={"X":1,"E":0,"O":-1}):
        self.utilidad=utilidad
        self.tablero=tablero
        self.esFinal = False
        self.ganador = None
        self.valor = None
        self.jugador = jugador
        self.valor_tablero()

  
    def __iter__(self):
        return self
    
  
    def __next__(self):
      if self.__index == len(self.hijos)-1:
        raise StopIteration
      self.__index = self.__index + 1
      return self.hijos[self.__index]


    def __str__(self):
      return 'E' + str(self.id)

                    
    def valor_tablero(self):
        """
            Asigna el valor de un tablero
        """
        for i in range(3):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != '_':
                self.esFinal=True
                self.ganador=self.tablero[i][0]
                self.valor=self.utilidad[self.ganador]
                break
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != '_':
                self.esFinal=True
                self.ganador=self.tablero[0][i]
                self.valor=self.utilidad[self.ganador]
                break
        if self.tablero[0][0]==self.tablero[1][1]==self.tablero[2][2]!='_' or self.tablero[0][2]==self.tablero[1][1]==self.tablero[2][0] != '_':
            self.esFinal=True
            self.ganador=self.tablero[1][1] 
            self.valor=self.utilidad[self.ganador]
    
                   

def main():
    jugador=stdin.readline().strip()
    tablero=[]
    b=Busqueda()
    for i in range(3):
        linea=[_ for _ in stdin.readline().strip()]
        tablero.append(linea)
    maximo=-float("inf")
    #Iteramos sobre todos los posibles siguientes estados y elegimos el que tenga el mayor valor
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == '_':
                tablero[fila][columna] = jugador
                proximo = Jugador("X") if jugador=="O" else Jugador("O")
                posible_maximo=b.minMax(TEstado(tablero,proximo),proximo)
                if posible_maximo>maximo:
                    maximo=posible_maximo
                    nextF,nextC=fila,columna                            
                tablero[fila][columna] = '_'
    tablero[nextF][nextC]=jugador
    print(nextF,nextC)
main()
