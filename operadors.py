from typing import List


class Operator(object):
    pass

class Moure_casella(Operator):
    def __init__(self, current_position):
        self.current_position = current_position
        #print(id_furgoneta)
    def __repr__(self) -> str:
        return f"Assignem la estacio origen {self.id_est} a la furgoneta {self.id_furgoneta} i agafem {self.agafar_bicicletes} bicicletes."

class Estacio_desti(Operator):
    def __init__(self, id_desti: int, id_furgoneta: int):
        self.id_furgoneta = id_furgoneta
        self.id_desti = id_desti
        
    def __repr__(self) -> str:
        return f"Assignem la estacio desti {self.id_desti} a la furgoneta {self.id_furgoneta}."
    
class Afegir_estacio_desti(Operator):
    def __init__(self, id_desti: int, id_furgoneta: int):
        self.id_furgoneta = id_furgoneta
        self.id_desti = id_desti

    def __repr__(self) -> str:
        return f"Afegim la estacio desti {self.id_desti} a la furgoneta {self.id_furgoneta}."

class Intercanviar_destins(Operator):
    def __init__(self, id_furgoneta: int):
        self.id_furgoneta = id_furgoneta

    def __repr__(self) -> str:
        return f"Intercanviem les estacions destí."

class Eliminar_estacio(Operator):
    def __init__(self, id_furgoneta:int, destins: bool = False):
        self.id_furgoneta = id_furgoneta
        self.destins = destins
        
    def __repr__(self) -> str:
        return f"Elimina una estació."
       
class Pivotar_destins(Operator):
    def __init__(self, id_furgoneta: int, estacio_canvia: int, id_estacio: int) -> None:
        self.id_furgoneta = id_furgoneta
        self.estacio_canvia = estacio_canvia
        self.id_estacio = id_estacio
        
    def __repr__(self) -> str:
        return f"Intercanviem totes les estacions desti"