package modelo;

// Guarda información de una operación para el historial (pila)
public class Operacion {
    private String tipo;
    private OrdenYServicio ordenAfectada;

    public Operacion(String tipo, OrdenYServicio ordenAfectada) {
        this.tipo = tipo;
        this.ordenAfectada = ordenAfectada;
    }

    public String getTipo() {
        return tipo;
    }

    public OrdenYServicio getOrdenAfectada() {
        return ordenAfectada;
    }

    @Override
    public String toString() {
        return "Operacion: " + tipo + " sobre " + ordenAfectada;
    }
}
