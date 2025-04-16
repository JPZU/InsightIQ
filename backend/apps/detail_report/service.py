from utils.agent_manager import AgentManager
import pdb
import pandas as pd


class DetailReportService:

    @staticmethod
    def generate_consumption_and_turnover_report():
        """
        Genera un reporte en texto sobre tendencias de consumo y rotación de productos
        usando un prompt IA.
        """
        agent = AgentManager()

        prompt = (
            "Eres un analista de datos especializado en inventarios. Analiza la base de datos actual y redacta "
            "un informe claro, profesional y bien estructurado en formato Markdown, que incluya lo siguiente:\n\n"
            "## Resumen del Estado del Inventario\n"
            "- Describe brevemente la situación actual del inventario.\n"
            "- Menciona si hay productos con niveles de inventario inusuales (muy altos o bajos).\n\n"
            "## Productos con Mayor y Menor Rotación\n"
            "- Enumera los productos con mayor rotación y proporciona datos clave como unidades vendidas o frecuencia de salida.\n"
            "- Haz lo mismo con los productos con menor rotación.\n\n"
            "## Recomendaciones de Reabastecimiento\n"
            "- Sugiere productos que deberían reabastecerse pronto.\n"
            "- Justifica cada recomendación con base en patrones históricos.\n\n"
            "## Conclusión\n"
            "- Resume en pocas líneas los puntos más importantes y la acción prioritaria sugerida.\n\n"
            "Asegúrate de usar un lenguaje claro, evitar términos técnicos innecesarios y redactar como si el informe fuera presentado a un gerente general no técnico."
        )

        result_text = agent.query_nlp_text_only(prompt)
        return {"report_text": result_text}
