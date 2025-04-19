from datetime import datetime

from utils.agent_manager import AgentManager


class DetailReportService:

    @staticmethod
    def generate_consumption_and_turnover_report():
        """
        Genera un reporte en texto sobre tendencias de consumo y rotación de productos
        usando un prompt IA.
        """
        agent = AgentManager()

        prompt = (
            "You are a data analyst specialized in inventory management. Analyze the current database and write "
            "a clear, professional, and well-structured report in markdown format, including the following sections:\n\n"
            "## Inventory Status Summary\n"
            "- Briefly describe the current state of the inventory.\n"
            "- Mention if there are any products with unusual stock levels (very high or very low).\n\n"
            "## High and Low Turnover Products\n"
            "- List the products with the highest turnover and provide key data such as units sold or frequency of movement.\n"
            "- Do the same for the products with the lowest turnover.\n\n"
            "## Restocking Recommendations\n"
            "- Suggest which products should be restocked soon.\n"
            "- Justify each recommendation based on historical patterns.\n\n"
            "## Conclusion\n"
            "- Summarize the most important points and the suggested priority action in a few sentences.\n\n"
            "Make sure to use clear language, avoid unnecessary technical terms, and write the report as if presenting it to a non-technical general manager."
            "**Important:** The entire report must be written in English, with no translations or mixed languages. "
            "Assume your audience speaks only English."
        )

        result_text = agent.query_nlp_text_only(prompt)
        date = datetime.now()
        return {"report_text": result_text,
                "date": date}
