# Databricks notebook source
# DBTITLE 1,Libs
import os
import pandas as pd
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# DBTITLE 1,Pip Install
pip install openpyxl -q

# COMMAND ----------

# Funcao para ler excel e criar tabela delta

def convert_excel_to_delta_table(
    caminho_excel = "/Workspace/Users/kevyn.zap@hotmail.com/mba-novo-caged-data-engineering-free-edition/docs/dicionario-dados-novo-caged-movimentacao.xlsx",
    sheet_name = None,
    catalogo = "workspace",
    schema = "silver",
    tabela_name = "default"
):
    '''
    caminho_excel: caminho da pasta do excel
    sheet_name: aba requerida para leitura
    catalogo: nome do catalogo no databricks para ser salvo
    schema: schema em que será salvo a tabela
    tabela_name: nome da tabela que será salvo
    carminho_regiao: local fisico onde será salvo os dados em ADLS Gen2
    '''

    if caminho_excel is None or sheet_name is None:
        print("Passe os parametros requisitados: caminho_excel e sheet_name")
        return 
    else:
        # Lendo aba do arquivo excel
        df_init = pd.read_excel(
            caminho_excel,
            sheet_name = sheet_name,
            dtype=str
        )

        # Padronização de colunas
        df_tratadas = (
            df_init
            .rename(columns={
                "Código":"codigo",
                "Descrição":"descricao"
            })
        )

        # Padronizar os valores como texto
        for coluna in ["codigo", "descricao"]:
            df_tratadas[coluna] = (
                df_tratadas[coluna]
                .astype("string")
                .str.strip()
            )

        # Definir o schema da referência 
        schema_default = StructType([
            StructField("codigo", StringType(), False),
            StructField("descricao", StringType(), False)
        ])

        # Converter Pandas para Spark
        df_regiao_spark = spark.createDataFrame(
            df_tratadas.astype(object),
            schema=schema_default
        )

        # Nome da tabela no Unity Catalog
        tabela_regiao = f"{catalogo}.{schema}.{tabela_name}"

        # Criar a tabela Delta externa
        (
            df_regiao_spark.write
            .format("delta")
            .saveAsTable(tabela_regiao)
        )

        print(f"Tabela criada com sucesso: {tabela_regiao}")

        return df_regiao_spark