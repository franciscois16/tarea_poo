#%%
class Entidad:
    def __init__(self, nombre, salud, energia,salud_maxima,energia_maxima,ataque_basico):
        self.nombre = nombre
        self.salud = salud
        self.energia = energia
        self.salud_maxima = salud_maxima
        self.energia_maxima = energia_maxima
        self.ataque_basico = ataque_basico   
    def atacar(self, objetivo):
        objetivo.recibir_dano(self.ataque_basico)
        if objetivo.salud <= 0:
            print(f"{objetivo.nombre} ha sido derrotado.")
            self.recibir_experiencia(objetivo.experiencia_otorgada)

    
    def recibir_dano(self,dano):
        self.salud -= dano

    def usar_habilidad(self, habilidad, objetivo):  #asumimos que el personaje si tiene la habilidad usada
        if self.energia >= habilidad.energia_requerida:
            self.energia -= habilidad.energia_requerida
            dano = habilidad.ataque
            objetivo.recibir_dano(dano)
        else:
            print(f"{self.nombre} no tiene suficiente energía para usar la habilidad '{habilidad.nombre}'.")

    def descansar(self):
        if self.salud <= 0 :
            print("el personaje esta muerto")
        else:
            self.salud += self.salud_maxima*0.15
            self.energia += self.energia_maxima*0.15
            #en caso de que la vida sobrepase el max uso min para que se quede en 100 (min devuelve el minimo entre valores entregados)
            self.salud = min(self.salud, self.salud_maxima)
            self.energia = min(self.energia, self.energia_maxima)

    def recibir_experiencia(self, cantidad):
        pass  # Este método se usa en Personaje


# %%
class Personaje(Entidad):
    def __init__(self, nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico,habilidades=[],nivel=1, experiencia=0,invetario=[10]):
        super().__init__(nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico)
        self.habilidades = habilidades
        self.nivel = nivel
        self.experiencia = experiencia
        self.inventario = invetario

    def aprender_habilidad(self, habilidad):
        if len(self.habilidades) < 3:  # Verificar si el personaje puede aprender más habilidades
            self.habilidades.append(habilidad)
        else:
            print("El personaje ya tiene el máximo de habilidades (3).")

    def olvidar_habilidad(self, habilidad):
        if habilidad in self.habilidades:
            self.habilidades.remove(habilidad)
        else:
            print(f"El personaje no posee la habilidad '{habilidad.nombre}'.")

    def recibir_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= 100:  #sube de nivel cada 100 puntos de xp
            self.nivel += 1
            self.experiencia -= 100  # disminuimos 100 ptos al subir de nivel
            self.actualizar_atributos()

    def actualizar_atributos(self):
        self.salud_maxima += 10  # aumenta 10 puntos de salud máxima por nivel
        self.energia_maxima += 5  # aumenta 5 puntos de energía máxima por nivel
        self.ataque_basico += 2  # aumenta 2 puntos de ataque básico por nivel
        self.salud = self.salud_maxima  # Restaura la salud al máximo al subir de nivel
        self.energia = self.energia_maxima  # Restaura la energía al máximo al subir de nivel


    
    


class Enemigo(Entidad):
    def __init__(self, nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico,habilidades=[],experiencia_otorgada=25):
        super().__init__(nombre, salud, energia, salud_maxima, energia_maxima, ataque_basico)
        self.habilidades = habilidades
        self.experiencia_otorgada = experiencia_otorgada


class Habilidad:
    def __init__(self,nombre, ataque,energia_requerida):
        self.nombre = nombre
        self.ataque = ataque
        self.energia_requerida = energia_requerida
# %%
