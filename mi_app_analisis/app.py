import streamlit as st
import pandas as pd
from database import conectar
from notificaciones import enviar_aviso_registro

# Configuración inicial de la página
st.set_page_config(page_title="App Privada Mamá", layout="wide")

# --- LÓGICA DE SESIÓN (Memoria de la App) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- FUNCIÓN DE LOGIN ---
def login():
    st.title("🔐 Acceso al Sistema")
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        boton_entrar = st.form_submit_button("Entrar")

        if boton_entrar:
            try:
                conn = conectar()
                cursor = conn.cursor(dictionary=True)
                # Verificamos que el usuario exista, la clave coincida y esté ACTIVADO
                sql = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND password_hash = %s AND estado = 'activo'"
                cursor.execute(sql, (usuario, clave))
                user = cursor.fetchone()
                
                if user:
                    st.session_state.autenticado = True
                    st.session_state.nombre_usuario = user['nombre_usuario']
                    st.session_state.rol = user['rol']
                    st.success(f"¡Bienvenido {user['nombre_usuario']}!")
                    st.rerun()
                else:
                    st.error("Acceso denegado: Usuario/Contraseña incorrectos o cuenta no activada aún.")
                conn.close()
            except Exception as e:
                st.error(f"Error de conexión a la base de datos: {e}")

# --- FLUJO PRINCIPAL DE LA APLICACIÓN ---
if not st.session_state.autenticado:
    # Menú para usuarios que no han iniciado sesión
    menu_publico = st.sidebar.radio("Navegación", ["Entrar", "Registrarse"])
    
    if menu_publico == "Entrar":
        login()
    else:
        st.title("📝 Solicitud de Acceso")
        st.write("Completa el formulario para solicitar tu acceso al sistema.")
        with st.form("registro_form"):
            nuevo_user = st.text_input("Nombre de Usuario")
            email_user = st.text_input("Tu Correo Electrónico")
            password = st.text_input("Crea una Contraseña", type="password")
            
            if st.form_submit_button("Enviar Solicitud"):
                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    sql = "INSERT INTO usuarios (nombre_usuario, email_contacto, password_hash, rol, estado) VALUES (%s, %s, %s, 'consultor', 'pendiente')"
                    cursor.execute(sql, (nuevo_user, email_user, password))
                    conn.commit()
                    
                    # Notificación automática al correo de administración
                    enviar_aviso_registro(nuevo_user, "consultor")
                    
                    st.success("✅ ¡Solicitud enviada con éxito! Te avisaremos cuando seas aprobado.")
                    conn.close()
                except Exception as e:
                    st.error(f"Error al procesar el registro: {e}")
else:
    # --- MENÚ PARA USUARIOS AUTENTICADOS ---
    st.sidebar.success(f"Usuario: {st.session_state.nombre_usuario}")
    st.sidebar.write(f"Rol: {st.session_state.rol.capitalize()}")
    
    opciones = ["Visualizar Datos"]
    # Solo el admin puede ver el panel de aprobación
    if st.session_state.rol == "admin":
        opciones.append("Aprobar Usuarios (Admin)")
    
    opcion = st.sidebar.radio("Ir a:", opciones)
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    # ==========================================
    # OPCIÓN: VISUALIZAR DATOS
    # ==========================================
    if opcion == "Visualizar Datos":
        st.title("📂 Sistema de Gestión de Datos")
        
        busqueda = st.text_input("🔍 Buscar por nombre de empresa o colegio...")
        
        # Filtros rápidos con botones
        c1, c2, c3 = st.columns(3)
        query = "SELECT * FROM vista_general WHERE 1=1"
        
        if c1.button("🏢 Ver Solo Empresas"): query += " AND tipo = 'empresa'"
        if c2.button("🎓 Ver Solo Colegios"): query += " AND tipo = 'colegio'"
        if c3.button("⚖️ Con Procesos Judiciales"): query += " AND url_proceso_judicial IS NOT NULL"

        if busqueda:
            query += f" AND nombre LIKE '%{busqueda}%'"

        try:
            conn = conectar()
            df = pd.read_sql(query, conn)
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # --- BOTÓN DE DESCARGA A EXCEL/CSV ---
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar esta lista en CSV",
                    data=csv,
                    file_name="reporte_datos.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No se encontraron resultados para tu búsqueda.")
            conn.close()
        except Exception as e:
            st.error(f"Error al cargar los datos: {e}")

    # ==========================================
    # OPCIÓN: APROBAR USUARIOS (SOLO ADMIN)
    # ==========================================
    elif opcion == "Aprobar Usuarios (Admin)":
        st.title("🛡️ Panel de Control de Usuarios")
        st.write("Gestiona las solicitudes de acceso pendientes.")
        
        try:
            conn = conectar()
            # Ajustado a 'id' según vimos en el error anterior
            query = "SELECT id, nombre_usuario, email_contacto, rol FROM usuarios WHERE estado = 'pendiente'"
            df_pendientes = pd.read_sql(query, conn)

            if not df_pendientes.empty:
                for idx, fila in df_pendientes.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"👤 {fila['nombre_usuario']} | 📧 {fila['email_contacto']} | 🔑 Rol: {fila['rol']}")
                    with col2:
                        # El ID asegura que el botón active al usuario correcto
                        if st.button(f"✅ Activar", key=f"btn_{fila['id']}"):
                            cursor = conn.cursor()
                            cursor.execute("UPDATE usuarios SET estado = 'activo' WHERE id = %s", (fila['id'],))
                            conn.commit()
                            st.success(f"Usuario {fila['nombre_usuario']} activado.")
                            st.rerun()
            else:
                st.write("✨ No hay nuevas solicitudes por aprobar.")
            conn.close()
        except Exception as e:
            st.error(f"Error en el panel administrativo: {e}")

# ==========================================
    # HERRAMIENTAS DE EDICIÓN (SUPERPODERES)
    # ==========================================
    st.divider()
    st.subheader("🛠️ Panel de Edición y Control")
    
    accion = st.selectbox("¿Qué quieres hacer?", ["--- Seleccionar ---", "Añadir Nueva Empresa/Colegio", "Editar Información Existente", "Eliminar un Registro"])

    # --- 1. AÑADIR (Ya lo tienes, pero aquí está unificado) ---
    if accion == "Añadir Nueva Empresa/Colegio":
        with st.form("form_nuevo"):
            nombre_n = st.text_input("Nombre")
            tipo_n = st.selectbox("Tipo", ["empresa", "colegio"])
            correos_n = st.text_input("Correos")
            telefonos_n = st.text_input("Teléfonos")
            url_n = st.text_input("URL Proceso Judicial")
            if st.form_submit_button("Guardar Nuevo"):
                conn = conectar(); cursor = conn.cursor()
                cursor.execute("INSERT INTO vista_general (nombre, tipo, lista_correos, lista_telefonos, url_proceso_judicial) VALUES (%s, %s, %s, %s, %s)", (nombre_n, tipo_n, correos_n, telefonos_n, url_n))
                conn.commit(); conn.close(); st.rerun()

    # --- 2. EDITAR (Lo que faltaba) ---
    elif accion == "Editar Información Existente":
        id_editar = st.number_input("Escribe el ID del registro a editar", min_value=1, step=1)
        
        # Primero buscamos los datos actuales para que ella no escriba desde cero
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vista_general WHERE id = %s", (id_editar,))
            datos_actuales = cursor.fetchone()
            conn.close()

            if datos_actuales:
                st.info(f"Editando: **{datos_actuales['nombre']}**")
                with st.form("form_editar"):
                    nuevo_nombre = st.text_input("Nombre", value=datos_actuales['nombre'])
                    nuevo_tipo = st.selectbox("Tipo", ["empresa", "colegio"], index=0 if datos_actuales['tipo'] == 'empresa' else 1)
                    nuevo_correos = st.text_input("Correos", value=datos_actuales['lista_correos'])
                    nuevo_telefonos = st.text_input("Teléfonos", value=datos_actuales['lista_telefonos'])
                    nuevo_url = st.text_input("URL Judicial", value=datos_actuales['url_proceso_judicial'])
                    
                    if st.form_submit_button("Actualizar Cambios"):
                        conn = conectar(); cursor = conn.cursor()
                        sql_upd = """UPDATE vista_general 
                                     SET nombre=%s, tipo=%s, lista_correos=%s, lista_telefonos=%s, url_proceso_judicial=%s 
                                     WHERE id=%s"""
                        cursor.execute(sql_upd, (nuevo_nombre, nuevo_tipo, nuevo_correos, nuevo_telefonos, nuevo_url, id_editar))
                        conn.commit(); conn.close()
                        st.success("✅ ¡Información actualizada!")
                        st.rerun()
            else:
                st.warning("No se encontró ningún registro con ese ID.")
        except Exception as e:
            st.error(f"Error: {e}")

    # --- 3. ELIMINAR ---
    elif accion == "Eliminar un Registro":
        id_borrar = st.number_input("ID a eliminar", min_value=1, step=1)
        if st.button("🗑️ Confirmar Eliminación"):
            conn = conectar(); cursor = conn.cursor()
            cursor.execute("DELETE FROM vista_general WHERE id = %s", (id_borrar,))
            conn.commit(); conn.close(); st.rerun()            