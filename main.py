from rpg import *

# Creamos un personaje y un enemigo
jugador = Personaje("julius", 100, 50, 100, 50, 10,15)
enemigo = Enemigo("Ogro", 80, 30, 80, 30, 8,25)

# Aprendemos una habilidad
habilidad_1 = Habilidad("Habilidad de Fuego", 15, 10)
jugador.aprender_habilidad(habilidad_1)

# El personaje ataca al enemigo
jugador.atacar(enemigo)

# El enemigo contraataca
enemigo.atacar(jugador)

# El personaje descansa
jugador.descansar()

# El personaje sube de nivel
jugador.recibir_experiencia(enemigo.experiencia_otorgada)

# Creamos un objeto, una poción y una tienda
espada = Objeto("espada sin filo", "Una espada sin filo mejor usa los puños", 50)
pocion_vida = Pocion("Poción de Vida", "Recupera salud",35, "salud", 1)
tienda = tiendas([espada], [pocion_vida])

# El personaje compra un objeto en la tienda
jugador.comprar(tienda, espada)
jugador.comprar(tienda, pocion_vida)

# El personaje usa una poción
jugador.usar_pocion(pocion_vida)

jugador.listar_inventario()
