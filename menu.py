"""Menú de consola de la aplicación."""

import logging
from gestion import Gestion
from models import Jugador
from models import CuerpoTecnico
import os

logger = logging.getLogger(__name__)


class Menu:
    def __init__(self, gestion: Gestion):
        self.gestion = gestion

    def mostrar(self) -> None:
        """Muestra el menú principal y procesa las opciones."""
        while True:
            print("==============================================\n"
                  "Selecciona la aplicación que deseas iniciar:\n"
                  "==============================================\n"
                  "1. Héroes y villanos\n"
                  "2. Plantillas de fútbol\n"
                  "3. Salir\n"
                  "==============================================\n"
            )
            try:
                decisionMenu= int(input())
                if decisionMenu == 1:
                    while True:
                        print("\n=== HÉROES Y VILLANOS DEL VIRGEN ===")
                        print("1. Crear héroe")
                        print("2. Crear villano")
                        print("3. Listar personajes")
                        print("4. Buscar por atributo")
                        print("5. Emparejar héroe y villano")
                        print("6. Eliminar personaje")
                        print("0. Salir")
                        try:
                            opcion = input("Elige una opción: ").strip()
                            if opcion == "1":
                                self._crear("heroe")
                            elif opcion == "2":
                                self._crear("villano")
                            elif opcion == "3":
                                self._listar()
                            elif opcion == "4":
                                self._buscar()
                            elif opcion == "5":
                                self._emparejar()
                            elif opcion == "6":
                                self._eliminar()
                            elif opcion == "0":
                                logger.info("Aplicación cerrada por el usuario.")
                                print("Hasta luego.")
                                break
                            else:
                                print("Opción no válida.")
                                logger.warning("Opción de menú no válida: %s", opcion)
                        except (ValueError, TypeError) as exc:
                            print(f"Error: {exc}")
                            logger.warning("Entrada no válida: %s", exc)
                        except (KeyboardInterrupt, EOFError):
                            logger.info("Salida solicitada desde teclado.")
                            print("\nAplicación finalizada.")
                            break
                        except Exception:
                            logger.exception("Error no controlado en el menú.")
                            print("Se ha producido un error. Consulta el archivo aplicacion.log.")

                elif decisionMenu == 2:
                    while True:
                        print("==============================================\n"
                              "              PLANTILLAS DE FÚTBOL            \n"
                              "==============================================\n"
                              "1. Agragar miembro\n"
                              "2. Listar plantilla\n"
                              "3. Crear plantilla\n"
                              "4. Salir\n"
                              "==============================================\n"
                              )
                        try:
                            decision = int(input())
                            plantilla = {}
                            if decision == 1:
                                print("¿Qué tipo de miembro quieres agregar?\n"
                                      "1. Jugador\n"
                                      "2. Cuerpo técnico\n")
                                eleccion = input()
                                identificador = int(input("Dime el identificador:"))
                                nombre = input("Dime el nombre:")
                                apellido1 = input("Dime el primer apellido:")
                                apellido2 = input("Dime el segundo apellido:")
                                if eleccion == "1":
                                    posicion = input("¿Cuál es su posición?")
                                    plantilla[identificador] = Jugador(identificador, nombre, apellido1, apellido2, posicion)
                                    self.guardarSentenciaJugador(plantilla[identificador])
                                elif eleccion == "2":
                                    rol = input("¿Cuál es su rol?")
                                    plantilla[identificador] = CuerpoTecnico(identificador, nombre, apellido1, apellido2,rol)
                            elif decision == 2:
                                self.mostrarPlantilla(plantilla)
                            elif decision == 3:
                                pass
                            elif decision == 4:
                                logger.info("Aplicación cerrada por el usuario.")
                                print("Hasta luego.")
                                break


                        except (ValueError, TypeError) as exc:
                            print(f"Error: {exc}")
                            logger.warning("Entrada no válida: %s", exc)
                        except (KeyboardInterrupt, EOFError):
                            logger.info("Salida solicitada desde teclado.")
                            print("\nAplicación finalizada.")
                            break
                        except Exception:
                            logger.exception("Error no controlado en el menú.")
                            print("Se ha producido un error. Consulta el archivo aplicacion.log.")
                elif decisionMenu == 3:
                    logger.info("Aplicación cerrada por el usuario.")
                    print("Hasta luego.")
                    break
            except (ValueError, TypeError) as exc:
                print(f"Error: {exc}")
                logger.warning("Entrada no válida: %s", exc)
            except (KeyboardInterrupt, EOFError):
                logger.info("Salida solicitada desde teclado.")
                print("\nAplicación finalizada.")
                break
            except Exception:
                logger.exception("Error no controlado en el menú.")
                print("Se ha producido un error. Consulta el archivo aplicacion.log.")


    def _crear(self, tipo: str) -> None:
        nombre = input("Nombre: ").strip()
        apellidos = input("Apellidos: ").strip()
        fecha = input("Fecha de nacimiento (AAAA-MM-DD): ").strip()
        personaje = self.gestion.crear_personaje(tipo, nombre, apellidos, fecha)
        print(f"Personaje creado: {personaje}")

    def _listar(self) -> None:
        tipo = input("¿Qué quieres listar? (heroe/villano/todos): ").strip()
        personajes = self.gestion.listar_personajes(tipo)
        if not personajes:
            print("No hay personajes para mostrar.")
            return
        for personaje in personajes:
            print(personaje)

    def _buscar(self) -> None:
        tipo = input("Tipo (heroe/villano): ").strip()
        print("Atributos: identificador, nombre, apellidos, fecha_nacimiento, edad,")
        print("          puntuacion_total y las cualidades propias de cada tipo.")
        atributo = input("Atributo: ").strip()
        operador = input("Operador (=, !=, >, >=, <, <=, contiene): ").strip()
        valor = input("Valor a buscar: ").strip()
        resultados = self.gestion.buscar_por_atributo(tipo, atributo, operador, valor)
        if not resultados:
            print("No se han encontrado coincidencias.")
        else:
            for personaje in resultados:
                print(personaje)

    def _emparejar(self) -> None:
        heroe, villano, diferencia, valoracion = self.gestion.emparejar_aleatoriamente()
        print(f"Héroe: {heroe}")
        print(f"Villano: {villano}")
        print(f"Diferencia de puntuación: {diferencia}")
        print(valoracion)

    def _eliminar(self) -> None:
        tipo = input("Tipo (heroe/villano): ").strip()
        identificador = int(input("Identificador: "))
        if self.gestion.eliminar_personaje(tipo, identificador):
            print("Personaje eliminado.")
        else:
            print("No existe un personaje con ese identificador.")


    def guardarSentenciaJugador(self, jugador):
        os.makedirs(f"sentencias/", exist_ok=True)
        sentencia = (f"INSERT INTO jugador (id, nombre, apellidos, posicion) VALUES ({jugador.getIdentif()},{jugador.getNombre()},{jugador.getApellidos()}, {jugador.getPosicion()});")

        with open(f"sentencias/jugador0{jugador.getIdentif()}.sql", "w") as f:
            f.write(sentencia)

    def guardarSentenciaMiembro(self, miembro):
        os.makedirs(f"sentencias/", exist_ok=True)
        sentencia = (f"INSERT INTO miembro (id, nombre, apellidos, rol) VALUES ({miembro.getIdentif()},{miembro.getNombre()},{miembro.getApellidos()}, {miembro.getRol()});")

        with open(f"sentencias/miembro0{miembro.getIdentif()}.sql", "w") as f:
            f.write(sentencia)


    def mostrarPlantilla(self, plantilla):
        if plantilla is None:
            print("===========================================")
            print("No hay plantillas para mostrar.")
            print("===========================================")
        else:
            print("=============PLANTILLA DE FÚTBOL===============")
            for i in plantilla:
                print(f"ID: {i.getIdentif()}\n"
                      f"Tipo: {i.getTipo()}\n"
                      f"Nombre: {i.getNombre()}\n"
                      f"Apellidos: {i.getApellidos()}\n"
                      f"Posicion: {i.getPosicion()}\n"
                      f"--------------------------------------------")


