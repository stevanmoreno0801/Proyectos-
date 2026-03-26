package service;

import modelo.*;
import java.util.*;

// Clase que maneja la cola de clientes y el historial (pila)
public class GestorAtencion {
    private Queue<Cliente> colaClientes;
    private Stack<Operacion> historial;
    private List<OrdenYServicio> ordenes;
    private int contadorOrdenes = 1;

    public GestorAtencion() {
        colaClientes = new LinkedList<>();
        historial = new Stack<>();
        ordenes = new ArrayList<>();
    }

    // Encolar cliente
    public void encolarCliente(Cliente c) {
        colaClientes.offer(c);
        System.out.println("Cliente encolado: " + c.getNombre());
    }

    // Ver siguiente
    public Cliente verSiguiente() {
        return colaClientes.peek();
    }

    // Atender cliente (crear orden)
    public void atenderCliente(String descripcionProblema) {
        if (colaClientes.isEmpty()) {
            System.out.println("No hay clientes en la cola ");
            return;
        }

        Cliente c = colaClientes.poll();
        if (descripcionProblema == null || descripcionProblema.trim().isEmpty()) {
            System.out.println("Descripción obligatoria ");
            colaClientes.offer(c); // lo devolvemos a la cola
            return;
        }

        OrdenYServicio orden = new OrdenYServicio(contadorOrdenes++, c, descripcionProblema);
        ordenes.add(orden);
        historial.push(new Operacion("ATENCION", orden));
        System.out.println("Cliente atendido  Se creó la " + orden);
    }

    // Deshacer última operación
    public void deshacerOperacion() {
        if (historial.isEmpty()) {
            System.out.println("No hay operaciones para deshacer ");
            return;
        }

        Operacion ultima = historial.pop();
        OrdenYServicio orden = ultima.getOrdenAfectada();
        ordenes.remove(orden);
        colaClientes.offer(orden.getCliente());
        System.out.println("Deshecha la operación: " + ultima.getTipo());
        System.out.println("El cliente regreso a la cola: " + orden.getCliente().getNombre());
    }

    // Mostrar cola
    public void mostrarCola() {
        System.out.println("\n--- COLA DE CLIENTES ---");
        if (colaClientes.isEmpty()) {
            System.out.println("Vacia.");
        } else {
            for (Cliente c : colaClientes) {
                System.out.println(c);
            }
        }
        System.out.println("Tamaño: " + colaClientes.size());
    }

    // Mostrar historial
    public void mostrarHistorial() {
        System.out.println("\n--- HISTORIAL DE OPERACIONES ---");
        if (historial.isEmpty()) {
            System.out.println("Vacio.");
        } else {
            for (Operacion op : historial) {
                System.out.println(op);
            }
        }
        System.out.println("Tamaño: " + historial.size());
    }
}
