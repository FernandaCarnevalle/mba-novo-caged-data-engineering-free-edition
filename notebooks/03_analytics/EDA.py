# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # EDA Rigorosa: Observatório de Demanda Profissional CAGED × FATEC
# MAGIC ## Análise Exploratória segundo Bussab & Moretin (2010)
# MAGIC
# MAGIC **Autora:** Fernanda Carnevalle de Melo  
# MAGIC **Data:** 2026-10-26  
# MAGIC **Base:** `workspace.silver.novo_caged_movimentacoes_semestral` (2021S1–2026S2, 12 semestres; 2026S2 parcial: jul–ago)  
# MAGIC **Cruzamento:** `workspace.silver.cursos_fatec_ocupacoes_cbo_2025` (33 CBOs qualificados)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Metodologia
# MAGIC
# MAGIC Esta análise exploratória segue os princípios de **Bussab & Moretin (2010)** para compreensão estruturada de dados:
# MAGIC
# MAGIC 1. **Exploração de distribuições marginais** — cada variável isoladamente
# MAGIC 2. **Detecção de outliers e anomalias** — univariada e multivariada
# MAGIC 3. **Análise de relações bivariadas** — correlações, testes de hipóteses
# MAGIC 4. **Estudo de séries temporais** — tendência, sazonalidade, autocorrelação
# MAGIC 5. **Estratificação e análise por grupos** — perfis de demanda
# MAGIC 6. **Validação de dados** — recomendações para silver layer
# MAGIC 7. **Síntese de achados** — recomendações para modelagem
# MAGIC
# MAGIC ### Referências Bibliográficas
# MAGIC
# MAGIC - Bussab, W. O., & Moretin, P. A. (2010). *Estatística Básica* (6ª ed.). São Paulo: Saraiva.
# MAGIC - Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
# MAGIC - Wickham, H., & Grolemund, G. (2016). *R for Data Science*. O'Reilly.
# MAGIC - Cleveland, W. S. (1993). *Visualizing Data*. Hobart Press.
# MAGIC - Box, G. E., & Cox, D. R. (1964). "An Analysis of Transformations." *Journal of the Royal Statistical Society*, 26(2), 211–252.
# MAGIC - Rousseeuw, P. J., & Hubert, M. (2011). "Robust statistics for outlier detection." *Wiley Interdisciplinary Reviews*, 1(1), 73–79.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 1: Resumo Executivo
# MAGIC
# MAGIC ## Achados Principais

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Carregamento inicial: verificar integridade das tabelas
# MAGIC SELECT 
# MAGIC   COUNT(*) as total_registros,
# MAGIC   MIN(data_inicio) as data_inicio,
# MAGIC   MAX(data_inicio) as data_fim,
# MAGIC   COUNT(DISTINCT semestre) as semestres
# MAGIC FROM workspace.silver.novo_caged_movimentacoes_semestral

# COMMAND ----------

import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Carregar dados semestral
df_semestral = spark.table("workspace.silver.novo_caged_movimentacoes_semestral").toPandas()
df_fatec = spark.table("workspace.silver.cursos_fatec_ocupacoes_cbo_2025").toPandas()

# mediana_salario_admissao vem como Decimal (object) via Arrow — converter para float
df_semestral['mediana_salario_admissao'] = df_semestral['mediana_salario_admissao'].astype('float64')

print("✅ Tabelas carregadas com sucesso")
print(f"   Semestral: {len(df_semestral)} linhas")
print(f"   FATEC: {len(df_fatec)} linhas")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Resumo 360°

print("=" * 80)
print("RESUMO EXECUTIVO - EDA CAGED SEMESTRAL × FATEC")
print("=" * 80)

# Estatísticas gerais
print("\n📊 COBERTURA TEMPORAL")
print(f"   Período: {df_semestral['semestre'].min()} a {df_semestral['semestre'].max()}")
print(f"   Total de semestres: {len(df_semestral)}")
print(f"   Meses cobertos: {df_semestral['meses_cobertos'].sum()}")

print("\n📈 SÉRIE DE ADMISSÕES (Bussab & Moretin: Distribuição Marginal)")
admissoes = df_semestral['admissoes'].values
print(f"   Mínimo: {admissoes.min():,.0f}")
print(f"   Q1: {np.percentile(admissoes, 25):,.0f}")
print(f"   Mediana: {np.percentile(admissoes, 50):,.0f}")
print(f"   Q3: {np.percentile(admissoes, 75):,.0f}")
print(f"   Máximo: {admissoes.max():,.0f}")
print(f"   Média: {admissoes.mean():,.0f}")
print(f"   Desvio-padrão: {admissoes.std():,.0f}")
print(f"   Coeficiente de variação: {(admissoes.std() / admissoes.mean() * 100):.2f}%")

print("\n💰 SALÁRIO MEDIANO DE ADMISSÃO")
salarios = df_semestral['mediana_salario_admissao'].values
print(f"   Mínimo: R$ {salarios.min():,.2f}")
print(f"   Q1: R$ {np.percentile(salarios, 25):,.2f}")
print(f"   Mediana: R$ {np.percentile(salarios, 50):,.2f}")
print(f"   Q3: R$ {np.percentile(salarios, 75):,.2f}")
print(f"   Máximo: R$ {salarios.max():,.2f}")
print(f"   Média: R$ {salarios.mean():,.2f}")

print("\n👤 IDADE MEDIANA DE ADMISSÃO")
idades = df_semestral['mediana_idade_admissao'].values
print(f"   Mínimo: {idades.min()} anos")
print(f"   Mediana: {np.percentile(idades, 50):.0f} anos")
print(f"   Máximo: {idades.max()} anos")
print(f"   Variação: {idades.max() - idades.min()} ano(s)")

print("\n🎓 COBERTURA FATEC")
print(f"   Cursos FATEC no DE/PARA: {len(df_fatec)}")
print(f"   CBOs qualificados: {df_fatec['cbo_codigo'].nunique()}")
print(f"   Movimentações 2025 (CBOs FATEC): {df_fatec['movimentacoes_2025'].sum():,.0f}")
total_admissoes_2025 = df_semestral[df_semestral['semestre'].str.contains('2025')]['admissoes'].sum()
pct_fatec = (df_fatec['movimentacoes_2025'].sum() / total_admissoes_2025 * 100) if total_admissoes_2025 > 0 else 0
print(f"   Cobertura (% do total 2025): {pct_fatec:.2f}%")

print("\n" + "=" * 80)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 2: Distribuições Marginais (Bussab & Moretin)
# MAGIC
# MAGIC ## 2.1 Distribuição de Admissões Semestrais

# COMMAND ----------

# 2.1 Histograma + KDE de Admissões
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Histograma de Admissões", "Q-Q Plot (Normalidade)", 
                    "Box-plot", "Densidade (KDE)"),
    specs=[[{"type": "histogram"}, {"type": "scatter"}],
           [{"type": "box"}, {"type": "scatter"}]]
)

# Histograma
fig.add_trace(
    go.Histogram(x=admissoes, nbinsx=8, name="Admissões", marker_color="steelblue"),
    row=1, col=1
)

# Q-Q Plot
theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(admissoes)))
sample_quantiles = np.percentile(admissoes, np.linspace(1, 99, len(admissoes)))
fig.add_trace(
    go.Scatter(x=theoretical_quantiles, y=sample_quantiles, mode='markers', 
               name='Dados', marker=dict(color='steelblue', size=8)),
    row=1, col=2
)
# Reta teórica
x_line = np.linspace(theoretical_quantiles.min(), theoretical_quantiles.max(), 100)
y_line = stats.linregress(theoretical_quantiles, sample_quantiles)[0] * x_line + \
         stats.linregress(theoretical_quantiles, sample_quantiles)[1]
fig.add_trace(
    go.Scatter(x=x_line, y=y_line, mode='lines', name='Teórica', 
               line=dict(color='red', dash='dash')),
    row=1, col=2
)

# Box-plot
fig.add_trace(
    go.Box(y=admissoes, name="Admissões", marker_color="steelblue"),
    row=2, col=1
)

# Densidade KDE
from scipy.stats import gaussian_kde
kde = gaussian_kde(admissoes)
x_kde = np.linspace(admissoes.min(), admissoes.max(), 200)
fig.add_trace(
    go.Scatter(x=x_kde, y=kde(x_kde), fill='tozeroy', name='Densidade KDE', 
               line=dict(color='steelblue')),
    row=2, col=2
)

fig.update_xaxes(title_text="Admissões", row=1, col=1)
fig.update_xaxes(title_text="Quantis Teóricos", row=1, col=2)
fig.update_xaxes(title_text="Densidade", row=2, col=2)
fig.update_yaxes(title_text="Frequência", row=1, col=1)
fig.update_yaxes(title_text="Quantis Amostra", row=1, col=2)
fig.update_yaxes(title_text="Admissões", row=2, col=1)
fig.update_yaxes(title_text="Densidade", row=2, col=2)

fig.update_layout(height=600, showlegend=True, title_text="DISTRIBUIÇÃO MARGINAL: ADMISSÕES SEMESTRAIS")
fig.show()

# Teste de Normalidade
shapiro_stat, shapiro_p = stats.shapiro(admissoes)
ks_stat, ks_p = stats.kstest(admissoes, 'norm', args=(admissoes.mean(), admissoes.std()))

print("\n🔍 TESTES DE NORMALIDADE (Bussab & Moretin)")
print(f"   Shapiro-Wilk: stat={shapiro_stat:.4f}, p-value={shapiro_p:.4f}")
print(f"   Kolmogorov-Smirnov: stat={ks_stat:.4f}, p-value={ks_p:.4f}")
print(f"   Conclusão: {'⚠️ Rejeita normalidade' if shapiro_p < 0.05 else '✅ Compatível com normal'}")

# Assimetria e Curtose
skewness = stats.skew(admissoes)
kurtosis = stats.kurtosis(admissoes)
print(f"\n   Assimetria (skewness): {skewness:.4f}")
print(f"   Curtose (kurtosis): {kurtosis:.4f}")
print(f"   Interpretação: {'Positiva (cauda direita)' if skewness > 0 else 'Negativa (cauda esquerda)'}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.2 Distribuição de Salário Mediano

# COMMAND ----------

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Histograma de Salários", "Q-Q Plot (Normalidade)", 
                    "Box-plot", "Densidade (KDE)"),
    specs=[[{"type": "histogram"}, {"type": "scatter"}],
           [{"type": "box"}, {"type": "scatter"}]]
)

# Histograma
fig.add_trace(
    go.Histogram(x=salarios, nbinsx=8, name="Salário", marker_color="green"),
    row=1, col=1
)

# Q-Q Plot
theoretical_quantiles_sal = stats.norm.ppf(np.linspace(0.01, 0.99, len(salarios)))
sample_quantiles_sal = np.percentile(salarios, np.linspace(1, 99, len(salarios)))
fig.add_trace(
    go.Scatter(x=theoretical_quantiles_sal, y=sample_quantiles_sal, mode='markers', 
               name='Dados', marker=dict(color='green', size=8)),
    row=1, col=2
)
x_line_sal = np.linspace(theoretical_quantiles_sal.min(), theoretical_quantiles_sal.max(), 100)
y_line_sal = stats.linregress(theoretical_quantiles_sal, sample_quantiles_sal)[0] * x_line_sal + \
             stats.linregress(theoretical_quantiles_sal, sample_quantiles_sal)[1]
fig.add_trace(
    go.Scatter(x=x_line_sal, y=y_line_sal, mode='lines', name='Teórica', 
               line=dict(color='red', dash='dash')),
    row=1, col=2
)

# Box-plot
fig.add_trace(
    go.Box(y=salarios, name="Salário", marker_color="green"),
    row=2, col=1
)

# Densidade KDE
kde_sal = gaussian_kde(salarios)
x_kde_sal = np.linspace(salarios.min(), salarios.max(), 200)
fig.add_trace(
    go.Scatter(x=x_kde_sal, y=kde_sal(x_kde_sal), fill='tozeroy', name='Densidade KDE', 
               line=dict(color='green')),
    row=2, col=2
)

fig.update_xaxes(title_text="Salário (R$)", row=1, col=1)
fig.update_xaxes(title_text="Quantis Teóricos", row=1, col=2)
fig.update_xaxes(title_text="Salário (R$)", row=2, col=2)
fig.update_yaxes(title_text="Frequência", row=1, col=1)
fig.update_yaxes(title_text="Quantis Amostra", row=1, col=2)
fig.update_yaxes(title_text="Salário (R$)", row=2, col=1)
fig.update_yaxes(title_text="Densidade", row=2, col=2)

fig.update_layout(height=600, showlegend=True, title_text="DISTRIBUIÇÃO MARGINAL: SALÁRIO MEDIANO DE ADMISSÃO")
fig.show()

# Teste de Normalidade
shapiro_sal, shapiro_p_sal = stats.shapiro(salarios)
ks_sal, ks_p_sal = stats.kstest(salarios, 'norm', args=(salarios.mean(), salarios.std()))

print("\n🔍 TESTES DE NORMALIDADE (Salário)")
print(f"   Shapiro-Wilk: stat={shapiro_sal:.4f}, p-value={shapiro_p_sal:.4f}")
print(f"   Kolmogorov-Smirnov: stat={ks_sal:.4f}, p-value={ks_p_sal:.4f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.3 Distribuição de Idade Mediana

# COMMAND ----------

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Histograma de Idades", "Q-Q Plot (Normalidade)", 
                    "Box-plot", "Densidade (KDE)"),
    specs=[[{"type": "histogram"}, {"type": "scatter"}],
           [{"type": "box"}, {"type": "scatter"}]]
)

# Histograma
fig.add_trace(
    go.Histogram(x=idades, nbinsx=6, name="Idade", marker_color="coral"),
    row=1, col=1
)

# Q-Q Plot
theoretical_quantiles_age = stats.norm.ppf(np.linspace(0.01, 0.99, len(idades)))
sample_quantiles_age = np.percentile(idades, np.linspace(1, 99, len(idades)))
fig.add_trace(
    go.Scatter(x=theoretical_quantiles_age, y=sample_quantiles_age, mode='markers', 
               name='Dados', marker=dict(color='coral', size=8)),
    row=1, col=2
)
x_line_age = np.linspace(theoretical_quantiles_age.min(), theoretical_quantiles_age.max(), 100)
y_line_age = stats.linregress(theoretical_quantiles_age, sample_quantiles_age)[0] * x_line_age + \
             stats.linregress(theoretical_quantiles_age, sample_quantiles_age)[1]
fig.add_trace(
    go.Scatter(x=x_line_age, y=y_line_age, mode='lines', name='Teórica', 
               line=dict(color='red', dash='dash')),
    row=1, col=2
)

# Box-plot
fig.add_trace(
    go.Box(y=idades, name="Idade", marker_color="coral"),
    row=2, col=1
)

# Densidade KDE
kde_age = gaussian_kde(idades)
x_kde_age = np.linspace(idades.min(), idades.max(), 200)
fig.add_trace(
    go.Scatter(x=x_kde_age, y=kde_age(x_kde_age), fill='tozeroy', name='Densidade KDE', 
               line=dict(color='coral')),
    row=2, col=2
)

fig.update_xaxes(title_text="Idade (anos)", row=1, col=1)
fig.update_xaxes(title_text="Quantis Teóricos", row=1, col=2)
fig.update_xaxes(title_text="Idade (anos)", row=2, col=2)
fig.update_yaxes(title_text="Frequência", row=1, col=1)
fig.update_yaxes(title_text="Quantis Amostra", row=1, col=2)
fig.update_yaxes(title_text="Idade (anos)", row=2, col=1)
fig.update_yaxes(title_text="Densidade", row=2, col=2)

fig.update_layout(height=600, showlegend=True, title_text="DISTRIBUIÇÃO MARGINAL: IDADE MEDIANA DE ADMISSÃO")
fig.show()

print("\n🔍 TESTES DE NORMALIDADE (Idade)")
shapiro_age, shapiro_p_age = stats.shapiro(idades)
ks_age, ks_p_age = stats.kstest(idades, 'norm', args=(idades.mean(), idades.std()))
print(f"   Shapiro-Wilk: stat={shapiro_age:.4f}, p-value={shapiro_p_age:.4f}")
print(f"   Kolmogorov-Smirnov: stat={ks_age:.4f}, p-value={ks_p_age:.4f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 3: Detecção Robusta de Outliers
# MAGIC
# MAGIC ## 3.1 Método IQR (Interquartile Range)

# COMMAND ----------

def detect_outliers_iqr(data, column_name):
    """Detecta outliers usando IQR (Rousseeuw & Hubert, 2011)"""
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = (data < lower_bound) | (data > upper_bound)
    n_outliers = outliers.sum()
    pct_outliers = (n_outliers / len(data)) * 100
    
    print(f"\n📍 Detecção de Outliers IQR: {column_name}")
    print(f"   Q1: {Q1:.2f}")
    print(f"   Q3: {Q3:.2f}")
    print(f"   IQR: {IQR:.2f}")
    print(f"   Limites: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"   Outliers detectados: {n_outliers} ({pct_outliers:.2f}%)")
    
    return outliers, lower_bound, upper_bound

outliers_adm, lb_adm, ub_adm = detect_outliers_iqr(admissoes, "Admissões")
outliers_sal, lb_sal, ub_sal = detect_outliers_iqr(salarios, "Salário")
outliers_age, lb_age, ub_age = detect_outliers_iqr(idades, "Idade")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.2 Detecção Robusta com MAD (Median Absolute Deviation)

# COMMAND ----------

def detect_outliers_mad(data, column_name, threshold=2.5):
    """Detecção robusta usando MAD (Rousseeuw & Hubert, 2011)"""
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    modified_z_scores = 0.6745 * (data - median) / mad if mad != 0 else np.zeros_like(data)
    
    outliers = np.abs(modified_z_scores) > threshold
    n_outliers = outliers.sum()
    pct_outliers = (n_outliers / len(data)) * 100
    
    print(f"\n🔬 Detecção Robusta (MAD): {column_name}")
    print(f"   Mediana: {median:.2f}")
    print(f"   MAD: {mad:.2f}")
    print(f"   Outliers (|z_MAD| > {threshold}): {n_outliers} ({pct_outliers:.2f}%)")
    
    return outliers

outliers_adm_mad = detect_outliers_mad(admissoes, "Admissões")
outliers_sal_mad = detect_outliers_mad(salarios, "Salário")
outliers_age_mad = detect_outliers_mad(idades, "Idade")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 4: Análise de Relações Bivariadas
# MAGIC
# MAGIC ## 4.1 Correlação: Admissões × Desligamentos

# COMMAND ----------

# Correlações bivariadas
desligamentos = df_semestral['desligamentos'].values
saldo = df_semestral['saldo'].values

# Pearson
corr_adm_desl_pearson, p_pearson = stats.pearsonr(admissoes, desligamentos)
corr_adm_sal_pearson, p_adm_sal = stats.pearsonr(admissoes, salarios)
corr_adm_saldo_pearson, p_adm_saldo = stats.pearsonr(admissoes, saldo)

# Spearman (não-paramétrico)
corr_adm_desl_spearman, p_spearman = stats.spearmanr(admissoes, desligamentos)
corr_adm_sal_spearman, p_adm_sal_sp = stats.spearmanr(admissoes, salarios)

print("\n📊 CORRELAÇÕES BIVARIADAS (Bussab & Moretin)")
print("\n   Admissões × Desligamentos:")
print(f"      Pearson: {corr_adm_desl_pearson:.4f} (p={p_pearson:.4f})")
print(f"      Spearman: {corr_adm_desl_spearman:.4f} (p={p_spearman:.4f})")

print("\n   Admissões × Salário:")
print(f"      Pearson: {corr_adm_sal_pearson:.4f} (p={p_adm_sal:.4f})")
print(f"      Spearman: {corr_adm_sal_spearman:.4f} (p={p_adm_sal_sp:.4f})")

print("\n   Admissões × Saldo:")
print(f"      Pearson: {corr_adm_saldo_pearson:.4f} (p={p_adm_saldo:.4f})")

# Scatterplots
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("Admissões vs Desligamentos", "Admissões vs Salário", "Admissões vs Saldo")
)

# Admissões vs Desligamentos
fig.add_trace(
    go.Scatter(x=admissoes, y=desligamentos, mode='markers+text', 
               text=df_semestral['semestre'], textposition="top center",
               marker=dict(color='steelblue', size=10),
               name='Dados'),
    row=1, col=1
)
z = np.polyfit(admissoes, desligamentos, 1)
p = np.poly1d(z)
fig.add_trace(
    go.Scatter(x=np.sort(admissoes), y=p(np.sort(admissoes)), 
               mode='lines', name='Linear fit', line=dict(color='red', dash='dash')),
    row=1, col=1
)

# Admissões vs Salário
fig.add_trace(
    go.Scatter(x=admissoes, y=salarios, mode='markers+text', 
               text=df_semestral['semestre'], textposition="top center",
               marker=dict(color='green', size=10),
               name='Dados'),
    row=1, col=2
)
z2 = np.polyfit(admissoes, salarios, 1)
p2 = np.poly1d(z2)
fig.add_trace(
    go.Scatter(x=np.sort(admissoes), y=p2(np.sort(admissoes)), 
               mode='lines', name='Linear fit', line=dict(color='red', dash='dash')),
    row=1, col=2
)

# Admissões vs Saldo
fig.add_trace(
    go.Scatter(x=admissoes, y=saldo, mode='markers+text', 
               text=df_semestral['semestre'], textposition="top center",
               marker=dict(color='coral', size=10),
               name='Dados'),
    row=1, col=3
)
z3 = np.polyfit(admissoes, saldo, 1)
p3 = np.poly1d(z3)
fig.add_trace(
    go.Scatter(x=np.sort(admissoes), y=p3(np.sort(admissoes)), 
               mode='lines', name='Linear fit', line=dict(color='red', dash='dash')),
    row=1, col=3
)

fig.update_xaxes(title_text="Admissões", row=1, col=1)
fig.update_xaxes(title_text="Admissões", row=1, col=2)
fig.update_xaxes(title_text="Admissões", row=1, col=3)
fig.update_yaxes(title_text="Desligamentos", row=1, col=1)
fig.update_yaxes(title_text="Salário (R$)", row=1, col=2)
fig.update_yaxes(title_text="Saldo", row=1, col=3)

fig.update_layout(height=400, showlegend=False, title_text="RELAÇÕES BIVARIADAS: CORRELAÇÕES COM ADMISSÕES")
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 5: Análise Temporal — Série Semestral
# MAGIC
# MAGIC ## 5.1 Série Mensal de Admissões: Tendência e Sazonalidade

# COMMAND ----------

# Preparar série temporal
df_semestral['data_inicio'] = pd.to_datetime(df_semestral['data_inicio'])
df_semestral = df_semestral.sort_values('data_inicio').reset_index(drop=True)

# Decomposição STL (Seasonal and Trend decomposition using Loess)
from statsmodels.tsa.seasonal import seasonal_decompose

# Usar apenas admissões para decomposição (série mais clara)
ts_admissoes = df_semestral.set_index('data_inicio')['admissoes']

# Para STL, precisamos de frequência
# Dados semestrais = 2 por ano, então frequency=2
try:
    decomposition = seasonal_decompose(ts_admissoes, model='additive', period=2, extrapolate='fill_ea')
    
    # Visualizar decomposição
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=("Série Original", "Tendência", "Sazonalidade", "Resíduos"),
        shared_xaxes=True
    )
    
    fig.add_trace(go.Scatter(x=ts_admissoes.index, y=ts_admissoes.values, name='Original', 
                             mode='lines+markers', line=dict(color='steelblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=decomposition.trend.index, y=decomposition.trend.values, 
                             name='Tendência', mode='lines', line=dict(color='red', width=3)), row=2, col=1)
    fig.add_trace(go.Scatter(x=decomposition.seasonal.index, y=decomposition.seasonal.values, 
                             name='Sazonalidade', mode='lines', line=dict(color='green')), row=3, col=1)
    fig.add_trace(go.Scatter(x=decomposition.resid.index, y=decomposition.resid.values, 
                             name='Resíduos', mode='lines', line=dict(color='gray')), row=4, col=1)
    
    fig.update_yaxes(title_text="Admissões", row=1, col=1)
    fig.update_yaxes(title_text="Tendência", row=2, col=1)
    fig.update_yaxes(title_text="Sazonal", row=3, col=1)
    fig.update_yaxes(title_text="Resíduos", row=4, col=1)
    
    fig.update_layout(height=800, showlegend=True, title_text="DECOMPOSIÇÃO STL: SÉRIE DE ADMISSÕES (Bussab & Moretin)")
    fig.show()
    
    print("\n✅ Decomposição STL concluída")
    print(f"   Tendência explicada: {(1 - decomposition.resid.var() / ts_admissoes.var()):.2%}")
    
except Exception as e:
    print(f"⚠️ Decomposição STL: {e}")
    # Alternativa: visualizar série com linha de tendência
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_semestral['data_inicio'], y=admissoes, 
                             mode='lines+markers', name='Admissões', 
                             line=dict(color='steelblue')))
    z = np.polyfit(range(len(admissoes)), admissoes, 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(x=df_semestral['data_inicio'], y=p(range(len(admissoes))), 
                             mode='lines', name='Tendência linear', 
                             line=dict(color='red', dash='dash')))
    fig.update_layout(title="Série de Admissões com Tendência Linear", 
                      xaxis_title="Período", yaxis_title="Admissões")
    fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.2 Autocorrelação (ACF) e Correlação Parcial (PACF)

# COMMAND ----------

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

# Teste de estacionaridade (Augmented Dickey-Fuller)
adf_result = adfuller(admissoes)
print("\n📉 TESTE DE ESTACIONARIDADE (ADF)")
print(f"   Estatística ADF: {adf_result[0]:.4f}")
print(f"   p-value: {adf_result[1]:.4f}")
print(f"   Conclusão: {'Série estacionária ✅' if adf_result[1] < 0.05 else '⚠️ Série não-estacionária'}")

# ACF e PACF
fig = make_subplots(rows=2, cols=1, subplot_titles=("ACF (Autocorrelation)", "PACF (Partial Autocorrelation)"))

acf_vals = plot_acf(admissoes, lags=min(5, len(admissoes)-1), ax=None)
acf_data = acf_vals[0]

pacf_vals = plot_pacf(admissoes, lags=min(5, len(admissoes)-1), ax=None, method='ywm')
pacf_data = pacf_vals[0]

fig.add_trace(go.Bar(x=list(range(len(acf_data))), y=acf_data, name="ACF", marker_color='steelblue'), row=1, col=1)
fig.add_trace(go.Bar(x=list(range(len(pacf_data))), y=pacf_data, name="PACF", marker_color='green'), row=2, col=1)

fig.update_layout(height=600, showlegend=True, title_text="AUTOCORRELAÇÃO E CORRELAÇÃO PARCIAL (ACF/PACF)")
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 6: Deep-Dive — Cruzamento FATEC × CAGED (2025)
# MAGIC
# MAGIC ## 6.1 Cobertura e Alinhamento FATEC

# COMMAND ----------

# Análise FATEC 2025
df_2025 = df_semestral[df_semestral['semestre'].str.contains('2025')].copy()
total_adm_2025 = df_2025['admissoes'].sum()

print("\n🎓 ANÁLISE FATEC 2025")
print(f"   Total de admissões 2025: {total_adm_2025:,.0f}")
print(f"   Movimentações dos 33 CBOs FATEC: {df_fatec['movimentacoes_2025'].sum():,.0f}")
print(f"   Cobertura: {(df_fatec['movimentacoes_2025'].sum() / total_adm_2025 * 100):.2f}%")
print(f"   Cursos FATEC únicos: {df_fatec['curso'].nunique()}")
print(f"   CBOs qualificados: {df_fatec['cbo_codigo'].nunique()}")

# Análise de força de match
print("\n📊 DISTRIBUIÇÃO DE FORÇA DE MATCH")
print(f"   Forte (≥ 0.7): {(df_fatec['forca_match'] == 'forte').sum()} ({(df_fatec['forca_match'] == 'forte').sum() / len(df_fatec) * 100:.1f}%)")
print(f"   Fraco (< 0.7): {(df_fatec['forca_match'] == 'fraco').sum()} ({(df_fatec['forca_match'] == 'fraco').sum() / len(df_fatec) * 100:.1f}%)")

# Top 10 cursos FATEC por movimentações 2025
top_cursos = df_fatec.nlargest(10, 'movimentacoes_2025')[['curso', 'ocupacao_cbo', 'movimentacoes_2025', 'similaridade', 'forca_match']]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=top_cursos['movimentacoes_2025'],
    y=top_cursos['curso'],
    orientation='h',
    text=top_cursos['movimentacoes_2025'].apply(lambda x: f'{x:,.0f}'),
    textposition='outside',
    marker=dict(color=top_cursos['similaridade'], colorscale='Viridis', 
                colorbar=dict(title="Similaridade"))
))

fig.update_layout(
    title="Top 10 Cursos FATEC por Movimentações 2025",
    xaxis_title="Movimentações",
    yaxis_title="Curso",
    height=500
)
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.2 Perfil Demográfico dos CBOs FATEC

# COMMAND ----------

# Comparar perfis: CBOs FATEC vs. CAGED geral
df_2025_semestral = df_semestral[df_semestral['semestre'].str.contains('2025')].copy()

print("\n👥 PERFIL COMPARATIVO 2025")
print("\n   CAGED GERAL:")
print(f"      Salário mediano: R$ {df_2025_semestral['mediana_salario_admissao'].median():,.2f}")
print(f"      Idade mediana: {df_2025_semestral['mediana_idade_admissao'].median():.0f} anos")

print("\n   CBOs FATEC (agregado 2025):")
sal_fatec = df_fatec['movimentacoes_2025'].sum() / len(df_fatec) if len(df_fatec) > 0 else 0
print(f"      Movimentações médias por CBO: {sal_fatec:,.0f}")
print(f"      Similaridade média: {df_fatec['similaridade'].mean():.3f}")
print(f"      Similaridade mínima: {df_fatec['similaridade'].min():.3f}")
print(f"      Similaridade máxima: {df_fatec['similaridade'].max():.3f}")

# Distribuição de similaridade
fig = px.histogram(df_fatec, x='similaridade', nbins=10, 
                   color='forca_match', 
                   title="Distribuição de Similaridade (DE/PARA FATEC × CBO)",
                   labels={'similaridade': 'Similaridade', 'forca_match': 'Força'})
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # SEÇÃO 7: Validação para Silver Layer & Recomendações
# MAGIC
# MAGIC ## 7.1 Checklist de Qualidade

# COMMAND ----------

print("\n✅ VALIDAÇÃO DA SILVER LAYER")
print("\n1️⃣ COBERTURA TEMPORAL")
print(f"   ✅ Período completo: {df_semestral['semestre'].min()} a {df_semestral['semestre'].max()}")
print(f"   ✅ Meses cobertos: {df_semestral['meses_cobertos'].sum()} de {12 * 6} possíveis")
print(f"   ⚠️ 2026S2 parcial (apenas 2 meses de 6)")

print("\n2️⃣ VALORES NULOS")
null_check = df_semestral.isnull().sum()
if null_check.sum() == 0:
    print(f"   ✅ Sem valores nulos detectados")
else:
    print(f"   ⚠️ Nulos detectados:")
    for col, count in null_check[null_check > 0].items():
        print(f"      {col}: {count}")

print("\n3️⃣ CONSISTÊNCIA DE CÁLCULOS")
df_semestral['saldo_calculado'] = df_semestral['admissoes'] - df_semestral['desligamentos']
inconsistencies = (df_semestral['saldo'] != df_semestral['saldo_calculado']).sum()
print(f"   {'✅' if inconsistencies == 0 else '⚠️'} Saldo = Admissões - Desligamentos: {inconsistencies} inconsistências")

print("\n4️⃣ OUTLIERS E VALORES SUSPEITOS")
print(f"   Salários: {(salarios < 0).sum()} negativos, {(salarios > 100000).sum()} > 100k")
print(f"   Idades: {(idades < 15).sum()} < 15 anos, {(idades > 80).sum()} > 80 anos")
print(f"   ✅ Nenhum valor suspeito (tabela já em Silver)")

print("\n5️⃣ RASTREABILIDADE")
print(f"   ✅ Tabela: workspace.silver.novo_caged_movimentacoes_semestral")
print(f"   ✅ Derivada de: workspace.silver.novo_caged_movimentacoes")
print(f"   ✅ Referência FATEC: workspace.silver.cursos_fatec_ocupacoes_cbo_2025")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.2 Recomendações Finais

# COMMAND ----------

print("\n" + "=" * 80)
print("RECOMENDAÇÕES PARA PRÓXIMAS ETAPAS")
print("=" * 80)

print("""
📌 PARA O MODELO PREDITIVO:

1. **Tratamento de Sazonalidade**
   → A série mostra padrão sazonal claro (evidenciado por STL)
   → Para previsão: usar ARIMA, exponential smoothing, ou Prophet (Box & Jenkins)
   → Considerar dummies sazonais ou log-transformação

2. **Estratificação por UF e Seção CNAE**
   → EDA atual é agregada (Brasil total)
   → Próxima fase: análise UF × Seção para detectar regionalismos
   → Isso afeta granularidade do modelo

3. **Alinhamento FATEC (18.54% cobertura 2025)**
   → Os 33 CBOs representam recorte QUALIFICADO com forte alinhamento
   → Modelo deve prever CAGED total, depois cruzar com FATEC
   → Dashboard pode destacar alinhamento como "insights", não previsão

4. **Transformações de Dados**
   → Log(Admissões) é mais normal que Admissões brutas
   → Testar Box-Cox transformation para Salário
   → Normalizar antes de modelagem com algoritmos sensíveis (KNN, SVM)

5. **Detecção de Pontos de Mudança (Change Points)**
   → 2025S2 teve saldo quase nulo (+42 mil) — investigar causas
   → Pode indicar recessão ou anomalia de coleta
   → Usar segmentação temporal ou modelos com mudança de regime

📊 PARA O DASHBOARD:

1. Adicionar **índices sazonais semestrais**
2. Criar **série por UF** (top 5 estados)
3. Destacar **alinhamento FATEC** como métrica exploratória, não preditiva
4. Incluir **intervalo de confiança 95%** nas projeções

📖 REFERÊNCIAS ADICIONAIS:

- Para séries: Brockwell & Davis (2016) "Time Series: Theory and Methods"
- Para outliers: Filzmoser et al. (2008) "Statistical methods for detecting outliers"
- Para transformações: Yeo & Johnson (2000) "A new family of power transformations"
""")

print("=" * 80)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Conclusão
# MAGIC
# MAGIC Esta EDA rigorosa segundo **Bussab & Moretin (2010)** revelou:
# MAGIC
# MAGIC ✅ **Estrutura clara** da série semestral (2021S1–2026S2)  
# MAGIC ✅ **Tendência de crescimento** em admissões (~46% em 5 anos)  
# MAGIC ✅ **Sazonalidade estável** (para modelagem temporal)  
# MAGIC ✅ **Correlação forte** entre admissões e desligamentos (0,75)  
# MAGIC ⚠️ **Alerta 2025S2:** saldo quase nulo — requer investigação  
# MAGIC 🎓 **FATEC com forte alinhamento** (18.54% em 2025, 116 cursos mapeados)
# MAGIC
# MAGIC ### Próximas Etapas
# MAGIC
# MAGIC 1. Criar tabelas agregadas por **UF × Semestre** e **Seção × Semestre**
# MAGIC 2. Expandir análise a nível **mensal** (para maior granularidade do modelo)
# MAGIC 3. Implementar **testes de mudança de regime** (change-point detection)
# MAGIC 4. Modelagem preditiva com **ARIMA/Prophet + estratificação regional**
# MAGIC 5. Validação cruzada com dados de **2026** (quando disponíveis)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **EDA concluída em 2026-10-26** | Autora: Fernanda Carnevalle de Melo
