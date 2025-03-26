from openai import OpenAI
from dotenv import load_dotenv
from transformers import pipeline
import os

# Inicializar el modelo de resumen de Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_rfp_bart(rfp_text, category, prompt):
    """
    Genera un análisis detallado basado en la categoría seleccionada sin límites de tamaño.
    La IA actúa como un experto en desarrollo, análisis y creación de RFPs.
    Devuelve el análisis y los pasos sugeridos.
    """
    print(f"Generando análisis para {category}...")
    try:
        chunk_size = 1024
        chunks = [rfp_text[i:i+chunk_size] for i in range(0, len(rfp_text), chunk_size)]

        summary_text = ""
        for chunk in chunks:
            if not chunk.strip():
                continue

            input_length = len(chunk.split())
            max_len = min(800, int(input_length * 0.8))
            min_len = max(50, int(input_length * 0.3))

            if min_len >= max_len:
                min_len = max(50, int(max_len * 0.5))

            try:
                response = summarizer(f"{category}: {chunk}", max_length=max_len, min_length=min_len, do_sample=False)
                if response and len(response) > 0:
                    summary_text += response[0]['summary_text'] + " "
            except Exception as inner_e:
                print(f"Error generando el resumen para un fragmento: {inner_e}")

        analysis = f"{category}: {summary_text.strip()}"
        return analysis
    except Exception as e:
        print(f"Error al procesar el análisis para {category}: {e}")
        return f"Error: {e}", ""
    
def generate_follow_up_steps_bart(summary_text, category):
    prompts = {
        "Análisis Rápido": "Proporciona un análisis completo de los puntos clave y los pasos necesarios para abordarlos.",
        "Alineación Estratégica": "Evalúa la alineación estratégica y sugiere pasos para mejorar el ajuste.",
        "Ventaja Competitiva": "Identifica ventajas competitivas clave y proporciona pasos para maximizar su impacto.",
        "Decisión de Participación": "Evalúa la viabilidad de participar y propone pasos concretos para preparar la propuesta.",
        "Entendimiento Detallado": "Desglosa los requisitos y sugiere pasos para cumplirlos eficientemente.",
        "Identificación de Problemas": "Identifica los desafíos y problemas clave y propone estrategias para abordarlos.",
        "Preguntas de Clarificación": "Genera preguntas aclaratorias sobre los requisitos y expectativas del cliente.",
        "Evaluación de Recursos": "Identifica recursos necesarios y sugiere estrategias para gestionarlos.",
        "Estructura del Índice": "Proporciona una estructura clara y organizada para la respuesta a la RFP.",
        "Resumen Ejecutivo": "Redacta un resumen que destaque los puntos clave y beneficios para el cliente.",
        "Solución Propuesta": "Describe cómo la solución aborda los requisitos del cliente y aporta valor.",
        "Valor Añadido": "Explica los beneficios específicos y ventajas competitivas de la propuesta.",
        "Experiencia y Credenciales": "Resume la experiencia relevante en proyectos similares y logros clave.",
        "Equipo de Proyecto": "Presenta el equipo con roles y responsabilidades relevantes.",
        "Cronograma y Presupuesto": "Proporciona un cronograma detallado y estimación de presupuesto.",
        "Cumplimiento de Requisitos": "Valida el cumplimiento de requisitos y sugiere áreas de ajuste."
    }
    prompt = prompts.get(category, "Genera pasos claros y accionables.")
    
    # Formato correcto de la cadena
    openai_prompt = f"""{prompt}

Resumen del análisis:
{summary_text.strip()}

Pasos sugeridos para abordar los puntos clave mencionados en el análisis:"""
    
    # En este punto, se podría integrar la llamada a OpenAI o simular los pasos sugeridos
    # Por ahora, regresamos unos pasos estáticos como ejemplo
    suggested_steps = f"""Pasos generados automáticamente: 
1. Analizar el resumen proporcionado.
2. Identificar los aspectos clave.
3. Desarrollar una estrategia de acción detallada."""
    
    return suggested_steps

def get_ai_summary_and_steps_bart(rfp_text):
    prompt = "Como experto en análisis de RFP, proporciona un resumen completo y profesional del siguiente documento. Resume los objetivos principales, el alcance y los requisitos clave. Luego, enumera los pasos sugeridos para abordar cada punto importante."
    return analyze_rfp_bart(rfp_text, "Análisis Rápido", prompt)


def get_ai_alignment_strategy_bart(rfp_text):
    prompt = "Como experto en análisis estratégico, evalúa la alineación del proyecto descrito en la RFP con la experiencia de la empresa. Destaca fortalezas y debilidades potenciales, y proporciona pasos claros para mejorar el ajuste estratégico."
    return analyze_rfp_bart(rfp_text, "Alineación Estratégica", prompt)


def get_ai_competitive_advantage_bart(rfp_text):
    prompt = "Como experto en análisis competitivo, identifica los diferenciadores clave y ventajas que la empresa puede aprovechar frente a los competidores. Proporciona un desglose de fortalezas y áreas de mejora, seguido de pasos accionables."
    return analyze_rfp_bart(rfp_text, "Ventaja Competitiva", prompt)


def get_ai_participation_decision_bart(rfp_text):
    prompt = "Como experto en análisis de decisiones, evalúa la viabilidad de participar en la RFP en función de los recursos y capacidades actuales. Proporciona una recomendación clara y los pasos necesarios para preparar una propuesta competitiva."
    return analyze_rfp_bart(rfp_text, "Decisión de Participación", prompt)


def get_ai_detailed_understanding_bart(rfp_text):
    prompt = "Como experto en análisis de RFP, desglosa los requisitos clave y las expectativas del cliente. Identifica restricciones y criterios de éxito."
    return analyze_rfp_bart(rfp_text, "Entendimiento Detallado", prompt)


def get_ai_pain_points_bart(rfp_text):
    prompt = "Como experto en análisis de problemas, identifica los desafíos y problemas que el cliente busca resolver en la RFP. Sugiere estrategias efectivas para abordar estos problemas."
    return analyze_rfp_bart(rfp_text, "Identificación de Problemas", prompt)


def get_ai_clarifying_questions_bart(rfp_text):
    prompt = "Como experto en análisis de requisitos, genera una lista de preguntas aclaratorias basadas en los requisitos y expectativas del cliente mencionados en la RFP. Asegúrate de que las preguntas sean relevantes y específicas."
    return analyze_rfp_bart(rfp_text, "Preguntas de Clarificación", prompt)


def get_ai_resource_evaluation_bart(rfp_text):
    prompt = "Como experto en evaluación de recursos, identifica los recursos necesarios para abordar la RFP, incluyendo personal, tecnología y presupuesto. Evalúa la disponibilidad de recursos y los posibles desafíos."
    return analyze_rfp_bart(rfp_text, "Evaluación de Recursos", prompt)


def get_ai_index_structure_bart(rfp_text):
    prompt = "Como experto en redacción de propuestas, genera una estructura de índice para la respuesta a la RFP, incluyendo secciones clave como introducción, solución propuesta, experiencia previa, cronograma y presupuesto."
    return analyze_rfp_bart(rfp_text, "Estructura del Índice", prompt)


def get_ai_executive_summary_bart(rfp_text):
    prompt = "Como experto en redacción ejecutiva, redacta un resumen que destaque los puntos clave de la propuesta, incluyendo objetivos, solución ofrecida y principales beneficios para el cliente."
    return analyze_rfp_bart(rfp_text, "Resumen Ejecutivo", prompt)


def get_ai_proposed_solution_bart(rfp_text):
    prompt = "Como experto en soluciones propuestas, describe cómo la solución propuesta aborda los requisitos del cliente, enfatizando el valor añadido y los beneficios específicos."
    return analyze_rfp_bart(rfp_text, "Solución Propuesta", prompt)


def get_ai_value_added_bart(rfp_text):
    prompt = "Como experto en análisis de valor añadido, explica de manera clara y convincente los beneficios específicos que aporta la solución propuesta, destacando ventajas competitivas."
    return analyze_rfp_bart(rfp_text, "Valor Añadido", prompt)


def get_ai_experience_credentials_bart(rfp_text):
    prompt = "Como experto en credenciales y experiencia, resume la experiencia relevante de la empresa en proyectos similares, destacando logros clave y referencias significativas."
    return analyze_rfp_bart(rfp_text, "Experiencia y Credenciales", prompt)


def get_ai_project_team_bart(rfp_text):
    prompt = "Como experto en gestión de proyectos, presenta el equipo de proyecto, incluyendo roles, responsabilidades y experiencia relevante de cada miembro."
    return analyze_rfp_bart(rfp_text, "Equipo de Proyecto", prompt)


def get_ai_timeline_budget_bart(rfp_text):
    prompt = "Como experto en planificación y presupuestación, proporciona un cronograma detallado con fechas clave y una estimación clara del presupuesto, considerando recursos y fases del proyecto."
    return analyze_rfp_bart(rfp_text, "Cronograma y Presupuesto", prompt)


def get_ai_requirements_compliance_bart(rfp_text):
    prompt = "Como experto en cumplimiento de requisitos, valida si la propuesta cumple con todos los requisitos descritos en la RFP. Indica posibles brechas o áreas que requieran ajustes o aclaraciones."
    return analyze_rfp_bart(rfp_text, "Cumplimiento de Requisitos", prompt)
