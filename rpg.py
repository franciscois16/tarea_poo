#%%
import random


class Entidad:
    def __init__(self, nombre, salud, energia,salud_maxima,energia_maxima,ataque_basico,prob_critico):
        self.nombre = nombre
        self.salud = salud
        self.energia = energia
        self.salud_maxima = salud
        self.energia_maxima = energia
        self.ataque_basico = ataque_basico   
        self.prob_critico = prob_critico
    def atacar(self, objetivo):
        critico = self.calcula_critico()
        if critico:
            objetivo.recibir_dano(self.ataque_basico*2)
            print(f"!!!CRITICO!!! {self.nombre} ha inflingido {self.ataque_basico} a {objetivo.nombre}")
        else:
            objetivo.recibir_dano(self.ataque_basico)
            print(f"{self.nombre} ha inflingido {self.ataque_basico} a {objetivo.nombre}")
        
        if objetivo.salud <= 0:
            print(f"{objetivo.nombre} ha sido derrotado.")
            self.recibir_experiencia(objetivo.experiencia_otorgada)
            if objetivo.objeto_otorgado is not None:
                self.recibir_objeto(objetivo.objeto_otorgado)
            if objetivo.dinero_otorgado is not None:
                self.recibir_dinero(objetivo)


    
    def recibir_dano(self,dano):
        self.salud -= dano

    def usar_habilidad(self, habilidad, objetivo):  #asumimos que el personaje si tiene la habilidad usada
        if self.energia >= habilidad.energia_requerida:
            self.energia -= habilidad.energia_requerida
            dano = habilidad.ataque
            objetivo.recibir_dano(dano)
        else:
            print(f"{self.nombre} no tiene suficiente energia para usar la habilidad '{habilidad.nombre}'.")

    def descansar(self):
        if self.salud <= 0 :
            print("el personaje esta muerto")
        else:
            self.salud += self.salud_maxima*0.15
            self.energia += self.energia_maxima*0.15
            #en caso de que la vida sobrepase el max uso min para que se quede en 100 (min devuelve el minimo entre valores entregados)
            self.salud = min(self.salud, self.salud_maxima)
            self.energia = min(self.energia, self.energia_maxima)
            print(f"{self.nombre} ha recuperado parte de su salud y de  su energia.")

    def recibir_experiencia(self, cantidad):
        pass  # Este metodo se usa en Personaje

    def calcula_critico(self):
        return random.randint(0,100) <= self.prob_critico


# %%
class Personaje(Entidad):
    def __init__(self, nombre, salud, energia, salud_maxima, energia_maxima,prob_critico, ataque_basico,habilidades=[],nivel=1, experiencia=0,dinero=1000):
        super().__init__(nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico,prob_critico)
        self.habilidades = habilidades
        self.nivel = nivel
        self.experiencia = experiencia
        self.inventario = []
        self.dinero = dinero

    def aprender_habilidad(self, habilidad):
        if len(self.habilidades) < 3:  # Verificar si el personaje puede aprender mas habilidades
            self.habilidades.append(habilidad)
        else:
            print("El personaje ya tiene el maximo de habilidades (3).")

    def olvidar_habilidad(self, habilidad):
        if habilidad in self.habilidades:
            self.habilidades.remove(habilidad)
        else:
            print(f"El personaje no posee la habilidad '{habilidad.nombre}'.")

    def recibir_experiencia(self, cantidad):
        print(f"has obtenido {cantidad} de experiencia")
        self.experiencia += cantidad
        if self.experiencia >= 100:  #sube de nivel cada 100 puntos de xp
            self.nivel += 1
            self.experiencia -= 100  # disminuimos 100 ptos al subir de nivel
            self.actualizar_atributos()

    def actualizar_atributos(self):
        print(f"los atributos de {self.nombre} se han actualizado")
        self.salud_maxima += 10  # aumenta 10 puntos de salud maxima por nivel
        self.energia_maxima += 5  # aumenta 5 puntos de energia maxima por nivel
        self.ataque_basico += 2  # aumenta 2 puntos de ataque basico por nivel
        self.salud = self.salud_maxima  # Restaura la salud al maximo al subir de nivel
        self.energia = self.energia_maxima  # Restaura la energia al maximo al subir de nivel

    def recibir_objeto(self, objetivo):
        if len(self.inventario) < 10:
            self.inventario.append(objetivo.objeto_otorgado)
            print(f"Has recibido el objeto: {objetivo.objeto_otorgado.nombre}")
        else:
            print("El inventario esta lleno, no puedes recibir mas objetos.")

    def eliminar_objeto(self, objeto):
        if objeto in self.inventario:
            self.inventario.remove(objeto)
            print(f"Has eliminado el objeto: {objeto.nombre}")
        else:
            print(f"No tienes el objeto {objeto.nombre} en tu inventario.")
    
    def usar_pocion(self,pocion):
        if pocion in self.inventario:
            if pocion.tipo == 'salud':
                self.salud += self.salud_maxima*(0.20*pocion.nivel)
                self.salud = min(self.salud, self.salud_maxima)     
                print(f"{self.nombre} ha usado {pocion.nombre} y ha recuperado {pocion.tipo}")       
            elif pocion.tipo == 'energia':
                self.energia_maxima += self.energia_maxima*(0.20*pocion.nivel)
                self.energia = min(self.energia, self.energia_maxima)
                print(f"{self.nombre} ha usado {pocion.nombre} y ha recuperado {pocion.tipo}")    
            self.inventario.remove(pocion)
        else:
            print("no tienes esta pocion en tu inventario")

    def recibir_dinero(self,objetivo):
        self.dinero += objetivo.dinero_otorgado

    def comprar(self, tienda, objeto):
        if objeto in tienda.inventario_objetos or objeto in tienda.inventario_pociones:
            if self.dinero >= objeto.precio_tienda:
                if len(self.inventario) < 10:  # Verificar espacio en el inventario
                    self.dinero -= objeto.precio_tienda
                    self.inventario.append(objeto)
                    print(f"Has comprado {objeto.nombre} por {objeto.precio_tienda} monedas.")
                else:
                    print("El inventario esta lleno, no puedes recibir mas objetos.")
            else:
                print(f"No tienes suficiente dinero para comprar {objeto.nombre}.")
        else:
            print(f"{objeto.nombre} no esta disponible en la tienda.")

                
    def listar_inventario(self):
        if self.inventario:
            print(f"Inventario de {self.nombre}:")
            for objeto in self.inventario:
                print(f"- {objeto.nombre}: {objeto.descripcion}")
        else:
            print(f"{self.nombre} no tiene objetos en su inventario.")


    
 


class Enemigo(Entidad):
    def __init__(self, nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico,prob_critico, habilidades=[], experiencia_otorgada=100, objeto_otorgado=None,dinero_otorgado=None):
        super().__init__(nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico,prob_critico)
        self.habilidades = habilidades
        self.experiencia_otorgada = experiencia_otorgada
        self.objeto_otorgado = objeto_otorgado
        self.dinero_otorgado = dinero_otorgado
        

class Habilidad:
    def __init__(self,nombre, ataque,energia_requerida):
        self.nombre = nombre
        self.ataque = ataque
        self.energia_requerida = energia_requerida

class Objeto:
    def __init__(self, nombre, descripcion,precio_tienda):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_tienda = precio_tienda

class Pocion(Objeto):
    def __init__(self, nombre, descripcion,precio_tienda, tipo, nivel):
        super().__init__(nombre, descripcion,precio_tienda)
        self.tipo = tipo
        self.nivel = nivel

class tiendas():
    def __init__(self, inventario_objetos=[], inventario_pociones=[]):
        self.inventario_objetos = inventario_objetos
        self.inventario_pociones = inventario_pociones
    
# %%
