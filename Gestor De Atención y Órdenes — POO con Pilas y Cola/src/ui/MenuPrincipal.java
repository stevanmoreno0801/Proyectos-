package ui;

import java.util.Scanner;
import service.GestorAtencion;
import modelo.Cliente;

public class MenuPrincipal {
    public static void iniciar() {
        Scanner sc = new Scanner(System.in);
        GestorAtencion gestor = new GestorAtencion();
        int opcion;

        do {
            System.out.println("\n--- MENU PRINCIPAL ---");
            System.out.println("1. Encolar cliente");
            System.out.println("2. Ver siguiente en la cola");
            System.out.println("3. Atender cliente (crear orden)");
            System.out.println("4. Ver tamaño; lista de la cola");
            System.out.println("5. Deshacer última operación (pila)");
            System.out.println("6. Ver tope; tamaño; lista del historial");
            System.out.println("0. Salir");
            System.out.print("OpciOn: ");

            while (!sc.hasNextInt()) {
                System.out.print("Por favor, ingresa un número válido: ");
                sc.next();
            }

            opcion = sc.nextInt();
            sc.nextLine();

            switch (opcion) {
                case 1:
                    System.out.print("Nombre del cliente: ");
                    String nombre = sc.nextLine();
                    System.out.print("Documento: ");
                    String doc = sc.nextLine();
                    gestor.encolarCliente(new Cliente(nombre, doc));
                    break;

                case 2:
                    Cliente siguiente = gestor.verSiguiente();
                    if (siguiente != null) {
                        System.out.println("Siguiente en la cola: " + siguiente);
                    } else {
                        System.out.println("No hay nadie en la cola ");
                    }
                    break;

                case 3:
                    System.out.print("Descripción del problema: ");
                    String desc = sc.nextLine();
                    gestor.atenderCliente(desc);
                    break;

                case 4:
                    gestor.mostrarCola();
                    break;

                case 5:
                    gestor.deshacerOperacion();
                    break;

                case 6:
                    gestor.mostrarHistorial();
                    break;

                case 0:
                    System.out.println("Saliendo...");
                    break;

                default:
                    System.out.println("Opción inválida ❌");
            }
        } while (opcion != 0);

        sc.close();
    }
}
