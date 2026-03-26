package modelo;

// Cliente hereda de Persona
public class Cliente extends Persona {

    public Cliente(String nombre, String documento) {
        super(nombre, documento);
    }

    @Override
    public String descripcion() {
        return "Cliente: " + getNombre() + " (Doc: " + getDocumento() + ")";
    }

    @Override
    public String toString() {
        return descripcion();
    }
}

