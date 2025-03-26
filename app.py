import streamlit as st
import time
import io
from utils.pdf_extractor import extract_text_from_pdf
from fpdf import FPDF
from database.db_manager import init_db, registrar_usuario, verificar_credenciales, save_rfp_data, save_response_data
from utils.ai_client_gemini import (
    get_ai_summary_and_steps_gemini, get_ai_alignment_strategy_gemini, get_ai_competitive_advantage_gemini,
    get_ai_participation_decision_gemini, get_ai_detailed_understanding_gemini, get_ai_pain_points_gemini,
    get_ai_clarifying_questions_gemini, get_ai_resource_evaluation_gemini, get_ai_index_structure_gemini,
    get_ai_executive_summary_gemini, get_ai_proposed_solution_gemini, get_ai_value_added_gemini,
    get_ai_experience_credentials_gemini, get_ai_project_team_gemini, get_ai_timeline_budget_gemini,
    get_ai_requirements_compliance_gemini, generate_follow_up_steps_gemini
)
from utils.ai_client_bart import (
    get_ai_summary_and_steps_bart, get_ai_alignment_strategy_bart, get_ai_competitive_advantage_bart,
    get_ai_participation_decision_bart, get_ai_detailed_understanding_bart, get_ai_pain_points_bart,
    get_ai_clarifying_questions_bart, get_ai_resource_evaluation_bart, get_ai_index_structure_bart,
    get_ai_executive_summary_bart, get_ai_proposed_solution_bart, get_ai_value_added_bart,
    get_ai_experience_credentials_bart, get_ai_project_team_bart, get_ai_timeline_budget_bart,
    get_ai_requirements_compliance_bart, generate_follow_up_steps_bart
)

# Inicializar la base de datos
init_db()

# Definir las categorías y subcategorías del menú
menu_options = {
    "Carga y Configuración": ["Cargar RFP", "Configuración General"],
    "Evaluación Inicial": ["Análisis rápido", "Alineación estratégica", "Ventaja Competitiva", "Decisión de Participar"],
    "Análisis Profundo": ["Comprensión Detallada", "Identificación de 'dolores'", "Preguntas Aclaratorias", "Evaluación de Recursos"],
    "Desarrollo de la Propuesta": ["Estructura del Índice", "Resumen ejecutivo", "Solución Propuesta", "Beneficios y Valor Añadido", "Experiencia y Credenciales", "Equipo de Proyecto", "Cronograma y Presupuesto", "Cumplimiento de Requisitos"],
    "Revisión y Aprobación": ["Revisión Interna", "Aprobación Responsable"]
}

def get_ai_function(page):
    ia_seleccionada = st.session_state.get("selected_ia", "Gemini")  # Valor por defecto si no hay selección
    if ia_seleccionada == "Gemini":
        # Selección de las funciones de Gemini
        return {
            "Análisis rápido": get_ai_summary_and_steps_gemini,
            "Alineación estratégica": get_ai_alignment_strategy_gemini,
            "Ventaja Competitiva": get_ai_competitive_advantage_gemini,
            "Decisión de Participar": get_ai_participation_decision_gemini,
            "Comprensión Detallada": get_ai_detailed_understanding_gemini,
            "Identificación de 'dolores'": get_ai_pain_points_gemini,
            "Preguntas Aclaratorias": get_ai_clarifying_questions_gemini,
            "Evaluación de Recursos": get_ai_resource_evaluation_gemini,
            "Estructura del Índice": get_ai_index_structure_gemini,
            "Resumen ejecutivo": get_ai_executive_summary_gemini,
            "Solución Propuesta": get_ai_proposed_solution_gemini,
            "Beneficios y Valor Añadido": get_ai_value_added_gemini,
            "Experiencia y Credenciales": get_ai_experience_credentials_gemini,
            "Equipo de Proyecto": get_ai_project_team_gemini,
            "Cronograma y Presupuesto": get_ai_timeline_budget_gemini,
            "Cumplimiento de Requisitos": get_ai_requirements_compliance_gemini,
        }.get(page, None)
    elif ia_seleccionada == "facebook/bart":
        # Selección de las funciones de Bart
        return {
            "Análisis rápido": get_ai_summary_and_steps_bart,
            "Alineación estratégica": get_ai_alignment_strategy_bart,
            "Ventaja Competitiva": get_ai_competitive_advantage_bart,
            "Decisión de Participar": get_ai_participation_decision_bart,
            "Comprensión Detallada": get_ai_detailed_understanding_bart,
            "Identificación de 'dolores'": get_ai_pain_points_bart,
            "Preguntas Aclaratorias": get_ai_clarifying_questions_bart,
            "Evaluación de Recursos": get_ai_resource_evaluation_bart,
            "Estructura del Índice": get_ai_index_structure_bart,
            "Resumen ejecutivo": get_ai_executive_summary_bart,
            "Solución Propuesta": get_ai_proposed_solution_bart,
            "Beneficios y Valor Añadido": get_ai_value_added_bart,
            "Experiencia y Credenciales": get_ai_experience_credentials_bart,
            "Equipo de Proyecto": get_ai_project_team_bart,
            "Cronograma y Presupuesto": get_ai_timeline_budget_bart,
            "Cumplimiento de Requisitos": get_ai_requirements_compliance_bart,
        }.get(page, None)
    else:
        return None  # Si la IA seleccionada no es válida

# Estado de sesión
def get_button_text(page):
    return f"Generar {page} con IA"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "current_category" not in st.session_state:
    st.session_state["current_category"] = "Carga y Configuración"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Cargar RFP"
if "rfp_text" not in st.session_state:
    st.session_state["rfp_text"] = ""
if "show_steps_button" not in st.session_state:
    st.session_state["show_steps_button"] = False
if "analysis_cache" not in st.session_state:
    st.session_state["analysis_cache"] = {}
if "respuesta_guardada" not in st.session_state:
    st.session_state["respuesta_guardada"] = False

# Función de inicio de sesión
def login(username, password):
    if verificar_credenciales(username, password):
        st.session_state["logged_in"] = True
        st.session_state["user"] = username
        st.success(f"Inicio de sesión exitoso. Bienvenido, {username}.")
    else:
        st.error("Nombre de usuario o contraseña incorrectos.")

# Función para cerrar sesión
def logout():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.session_state["current_category"] = "Carga y Configuración"
    st.session_state["current_page"] = "Cargar RFP"

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)

    # Guardar el PDF en un buffer en memoria
    pdf_buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')  
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)
    return pdf_buffer

# Función para restablecer análisis al cambiar de categoría o subcategoría
def reset_analysis():
    current_page = st.session_state.get("current_page", "")
    if current_page and "analysis" in st.session_state:
        st.session_state["analysis_cache"][current_page] = ""

# Layout principal
if st.session_state["logged_in"]:
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("BID_AI_Logotype.png", use_container_width=True)
    with col2:
        st.title("Análisis de RFPs con IA")
    
    # Menú lateral
    with st.sidebar:
        st.sidebar.success(f"Usuario: {st.session_state['user']}")
        for category in menu_options.keys():
            if st.button(category):
                st.session_state["current_category"] = category
                st.session_state["current_page"] = menu_options[category][0]
        st.button("Cerrar Sesión", on_click=logout)

    # CSS para uniformizar el tamaño de los botones del submenú y el botón de descarga
    st.markdown("""
        <style>
        .stButton button, .stDownloadButton button {
            height: 60px; /* Ajusta la altura según sea necesario */
            width: 100%;  /* Para que ocupen el ancho completo de la columna */
            margin: 5px 0; /* Espaciado entre botones */
            font-size: 16px; /* Tamaño de letra uniforme */
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Submenú con cajitas
    st.subheader(f"{st.session_state['current_category']}")
    sub_categories = menu_options[st.session_state["current_category"]]
    col1, col2, col3, col4 = st.columns(4)
    for i, subcategory in enumerate(sub_categories):
        col = [col1, col2, col3, col4][i % 4]
        if col.button(subcategory, key=subcategory):
            st.session_state["current_page"] = subcategory

    # Resaltar la página actual
    if "selected_ia" in st.session_state:
        ia_seleccionada = st.session_state["selected_ia"]
        st.markdown(f"**Página actual:** {st.session_state['current_page']} | IA seleccionada: {ia_seleccionada}")
    else:
        st.markdown(f"**Página actual:** {st.session_state['current_page']} | IA no seleccionada")
    
    # Contenido de la página actual
    if st.session_state["current_page"] == "Cargar RFP":
        st.subheader("Subir y Analizar RFP")
        uploaded_file = st.file_uploader("Sube un archivo RFP", type="pdf")
        
        if uploaded_file is not None:
            with open("uploaded.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            text = extract_text_from_pdf("uploaded.pdf")
            st.session_state["rfp_text"] = text
            st.text_area("Contenido del RFP", text, height=200)
            save_rfp_data(uploaded_file.name, text, "", "")
            st.success("Datos almacenados correctamente.")

    reset_analysis()

    if st.session_state["current_page"] == "Configuración General":
        st.subheader("Configuración General")
        
        # Mostrar opciones de IA
        ia_option = st.radio("Seleccione el modelo de IA", ["Gemini", "facebook/bart"])

        # Guardar la selección de IA en el estado de sesión
        st.session_state["selected_ia"] = ia_option

        # Mostrar la selección
        st.write(f"Has seleccionado: {st.session_state['selected_ia']}")

        # Agregar más configuraciones si es necesario
        if st.session_state["selected_ia"] == "IA con Gemini":
            st.write("Estás utilizando Gemini para el análisis.")
        elif st.session_state["selected_ia"] == "IA con Bart":
            st.write("Estás utilizando Bart para el análisis.")
    
    # Dentro de la parte donde generas el resumen con IA
    current_page = st.session_state.get("current_page", "")
    ai_function = get_ai_function(current_page)

    if ai_function:
        st.subheader(current_page)
        st.text_area("Contenido extraído de la RFP", st.session_state["rfp_text"], height=200)

        button_text = f"Generar {current_page} con IA"
        if st.button(button_text):
            if st.session_state["rfp_text"]:
                ai_function = get_ai_function(st.session_state["current_page"])

                if ai_function:
                    summary = ai_function(st.session_state["rfp_text"])
                    st.session_state["analysis_cache"][current_page] = summary  # Guarda por categoría
                    st.session_state["show_steps_button"] = True  # Activa el botón de pasos

                    # Mostrar análisis si existe para la categoría actual
                    if "analysis_cache" in st.session_state and st.session_state.get("current_page", "") in st.session_state["analysis_cache"]:
                        resumen_editable = st.text_area("Resumen Generado por IA", st.session_state["analysis_cache"][st.session_state["current_page"]], height=300)
                        
                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button("Guardar en la Base de Datos"):
                                rfp_id = st.session_state.get("rfp_id", "ID_desconocido")
                                pasos_sugeridos = generate_follow_up_steps_gemini(st.session_state["rfp_text"], "Análisis")
                                save_response_data(rfp_id, resumen_editable, pasos_sugeridos)
                                st.session_state["respuesta_guardada"] = True

                        if st.session_state.get("respuesta_guardada"):
                            success_message = st.empty()
                            success_message.success("Respuesta guardada correctamente en la base de datos.")
                            time.sleep(3)
                            success_message.empty()
                            st.session_state["respuesta_guardada"] = False

                        with col2:
                            pdf_buffer = generate_pdf(resumen_editable) 

                            st.download_button(
                                label="Descargar como PDF",
                                data=pdf_buffer.getvalue(),
                                file_name="resumen_ia.pdf",
                                mime="application/pdf"
                            )

        if st.session_state.get("show_steps_button", False):
            if st.button("Generar pasos con IA"):
                ia_seleccionada = st.session_state.get("selected_ia", "Gemini")
                
                if ia_seleccionada == "Gemini":
                    steps = generate_follow_up_steps_gemini(st.session_state["rfp_text"], "Análisis")
                    st.write("### Pasos Sugeridos")
                    st.write(steps)
                elif ia_seleccionada == "facebook/bart":
                    steps = generate_follow_up_steps_bart(st.session_state["rfp_text"], "Análisis")
                    st.write("### Pasos Sugeridos")
                    st.write(steps)
                else:
                    steps = "No se ha seleccionado una IA válida."

else:
    menu = st.sidebar.selectbox("Menú", ["Inicio de Sesión", "Registro"])
    if menu == "Registro":
        st.subheader("Registro de Usuario")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Registrar"):
            registrar_usuario(username, password)
    elif menu == "Inicio de Sesión":
        st.subheader("Inicio de Sesión")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión"):
            login(username, password)