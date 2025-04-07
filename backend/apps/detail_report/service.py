from utils.db_manager import DBManager
import pdb
import pandas as pd


class DetailReportService:

    @staticmethod
    def get_data():
        db_manager = DBManager()
        data = db_manager.get_all_data_from_table("retail_store")
        df = pd.DataFrame(data)

        return df

    @staticmethod
    def get_inventory_summary():
        df = DetailReportService.get_data()
        summary = {
            "total_products": int(df["Product ID"].nunique()),
            "total_inventory": int(df["Inventory Level"].sum()),
            "average_inventory": round(df["Inventory Level"].mean(), 2),
        }

        return summary

    @staticmethod
    def get_top_and_bottom_products_by_store(region_df):
        stores_data = {}
        for store_id in region_df["Store ID"].unique():
            store_df = region_df[region_df["Store ID"] == store_id]

            top_products = (
                store_df.groupby("Product ID")["Units Sold"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
                .to_dict(orient="records")
            )

            bottom_products = (
                store_df.groupby("Product ID")["Units Sold"]
                .sum()
                .sort_values(ascending=True)
                .head(5)
                .reset_index()
                .to_dict(orient="records")
            )

            stores_data[store_id] = {
                "top_5_products": top_products,
                "bottom_5_products": bottom_products,
            }
        return stores_data

    @staticmethod
    def get_category_sales_by_store(region_df):
        category_data = {}
        for store_id in region_df["Store ID"].unique():
            store_df = region_df[region_df["Store ID"] == store_id]

            category_summary = (
                store_df.groupby("Category")["Units Sold"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
                .to_dict(orient="records")
            )

            category_data[store_id] = category_summary
        return category_data

    @staticmethod
    def get_turnover_analysis_by_region():
        df = DetailReportService.get_data()
        result = {}

        for region in df["Region"].unique():
            region_df = df[df["Region"] == region]

            # Llamar a los métodos auxiliares
            top_bottom = DetailReportService.get_top_and_bottom_products_by_store(region_df)
            category_sales = DetailReportService.get_category_sales_by_store(region_df)

            # Unir los datos por tienda
            stores = {}
            for store_id in region_df["Store ID"].unique():
                stores[store_id] = {
                    **top_bottom.get(store_id, {}),
                    "category_sales": category_sales.get(store_id, [])
                }

            result[region] = stores

        return result

    @staticmethod
    def get_restock_recommendations():
        df = DetailReportService.get_data()
        df["Restock Needed"] = df["Inventory Level"] < df["Demand Forecast"]

        # Crear una columna para saber cuánto falta
        df["Shortage"] = df["Demand Forecast"] - df["Inventory Level"]

        # Filtrar productos que necesitan reabastecimiento
        recommendations = df[df["Restock Needed"]][
            ["Product ID", "Inventory Level", "Demand Forecast", "Units Sold", "Shortage"]
        ]

        # Ordenar por mayor escasez y tomar los 10 primeros
        top_critical = recommendations.sort_values(by="Shortage", ascending=False).head(10)

        return top_critical.to_dict(orient="records")
