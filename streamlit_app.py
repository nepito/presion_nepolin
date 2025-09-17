import streamlit as st
import requests
import datetime

# Configuración de la PWA
st.set_page_config(
    page_title="Nombre de Tu App",
    page_icon="🎯", # Puedes usar un emoji o la ruta a tu icono
    layout="wide"
)

# Título de la aplicación
st.title('Registro de Presión Arterial 🩺')

# Subtítulo con una breve descripción
st.write('Ingresa tus mediciones de presión arterial y pulso para registrarlas en la base de datos.')

# Definir la URL de la API
API_URL = "http://localhost:6969/presiones"

# Obtener la fecha y hora actuales para sugerirlas en el formulario
fecha_actual = datetime.date.today()
hora_actual = datetime.datetime.now().time().strftime("%H:%M:%S")

# --- Formulario de entrada de datos ---
with st.form(key='presion_form'):
    st.header('Datos de la Medición')

    # Campo para la presión sistólica
    sistolica = st.number_input('Presión Sistólica (mmHg)', min_value=0, value=120, help='Valor superior (presión máxima)')

    # Campo para la presión diastólica
    diastolica = st.number_input('Presión Diastólica (mmHg)', min_value=0, value=80, help='Valor inferior (presión mínima)')

    # Campo para el pulso
    pulso = st.number_input('Pulso (latidos/min)', min_value=0, value=75, help='Número de pulsaciones por minuto')

    # Campo de notas
    notas = st.text_area('Notas Adicionales', help='Detalles sobre la medición (ej. en ayunas, después de ejercicio, etc.)')

    # Campo para las etiquetas
    etiquetas_input = st.text_input('Etiquetas (separadas por comas)', help='Ej: mañana, reposo, estrés')
    # Convertir el string de etiquetas a una lista
    etiquetas = [tag.strip() for tag in etiquetas_input.split(',') if tag.strip()]

    # Campos de fecha y hora, sugeridos automáticamente
    fecha_medicion = st.date_input('Fecha de la Medición', value=fecha_actual)
    hora_medicion = st.time_input('Hora de la Medición', value=datetime.datetime.now().time())

    # Botón para enviar el formulario
    submit_button = st.form_submit_button(label='Registrar Medición')

# --- Lógica para enviar los datos a la API ---
if submit_button:
    # Preparar los datos en el formato JSON que la API espera
    data = {
        "diastolica": int(diastolica),
        "etiquetas": etiquetas,
        "fecha_medicion": str(fecha_medicion),
        "hora_medicion": hora_medicion.strftime("%H:%M:%S"),
        "notas": notas,
        "pulso": int(pulso),
        "sistolica": int(sistolica)
    }

    try:
        # Enviar la petición POST a la API
        response = requests.post(API_URL, json=data)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            st.success('✅ ¡Medición registrada exitosamente!')
            st.json(response.json())  # Mostrar la respuesta de la API
        else:
            st.error(f'❌ Ocurrió un error al registrar la medición. Código de estado: {response.status_code}')
            st.json(response.json()) # Mostrar el error detallado de la API

    except requests.exceptions.RequestException as e:
        st.error(f"❌ No se pudo conectar a la API. Asegúrate de que está funcionando en {API_URL}")
        st.write(f"Error detallado: {e}")