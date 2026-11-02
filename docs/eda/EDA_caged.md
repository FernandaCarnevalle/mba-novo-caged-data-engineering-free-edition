# EDA da Demanda Profissional CAGED
## Análise Exploratória segundo Bussab & Moretin (2010)

**Autora:** Fernanda Carnevalle de Melo  
**Data da EDA:** 2026-10-26 · **Relatório gerado em:** 2026-10-30 (re-execução completa do notebook)  
**Base:** `workspace.silver.novo_caged_movimentacoes_semestral` (2021S1–2026S2, 12 semestres; 2026S2 parcial: jul–ago) + série mensal agregada direto do bronze (`workspace.bronze.novo_caged_movimentacoes`)  
**Escopo desta EDA:** somente dados CAGED 
**Fonte:** notebook `notebooks/03_analytics/EDA` (todas as células executadas em ordem em 2026-10-30)

---

## Metodologia

Esta análise exploratória segue os princípios de **Bussab & Moretin (2010)**:

1. **Exploração de distribuições marginais** — cada variável isoladamente
2. **Detecção de outliers e anomalias** — univariada (IQR e MAD) e bivariada
3. **Análise de relações bivariadas** — correlações de Pearson e Spearman
4. **Estudo de séries temporais** — tendência (STL), estacionaridade (ADF), autocorrelação (ACF/PACF)
5. **Feature engineering temporal** — lags, janelas móveis, sazonalidade cíclica, exógenas defasadas
6. **Validação de dados** — checklist de qualidade da silver layer
7. **Síntese de achados** — recomendações para modelagem preditiva

### Referências Bibliográficas

- Bussab, W. O., & Moretin, P. A. (2010). *Estatística Básica* (6ª ed.). São Paulo: Saraiva.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Wickham, H., & Grolemund, G. (2016). *R for Data Science*. O'Reilly.
- Cleveland, W. S. (1993). *Visualizing Data*. Hobart Press.
- Box, G. E. P., & Cox, D. R. (1964). "An Analysis of Transformations." *Journal of the Royal Statistical Society*, 26(2), 211–252.
- Rousseeuw, P. J., & Hubert, M. (2011). "Robust statistics for outlier detection." *Wiley Interdisciplinary Reviews*, 1(1), 73–79.
- Brockwell, P. J., & Davis, R. A. (2016). *Time Series: Theory and Methods*.
- Filzmoser, P. et al. (2008). "Statistical methods for detecting outliers."
- Yeo, I.-K., & Johnson, R. A. (2000). "A new family of power transformations."

---

## Integridade da Base (verificação inicial)

Consulta de integridade sobre `workspace.silver.novo_caged_movimentacoes_semestral`:

| Métrica | Valor |
| --- | --- |
| Total de registros | 12 |
| Data início | 2021-01-01 |
| Data fim | 2026-07-01 |
| Semestres distintos | 12 |

**Por que essa verificação importa:** antes de qualquer estatística, é preciso garantir que a base está completa e contínua. Doze semestres sem lacunas significam que tendência e sazonalidade medidas aqui refletem o fenômeno real, e não buracos de coleta. Se faltasse um semestre, qualquer comparação entre períodos estaria enviesada.

---

# SEÇÃO 1: Resumo Executivo

## Cobertura temporal

- **Período:** 2021S1 a 2026S2 · **Total de semestres:** 12 · **Meses cobertos:** 68 (de 72 possíveis)
- ⚠️ **2026S2 é parcial** (apenas jul–ago/2026, 2 de 6 meses)

**Por que isso importa:** 68 dos 72 meses esperados estão presentes (cobertura ~94%). O semestre parcial de 2026S2 não é comparável aos demais e é justamente ele o ponto mais baixo da série; misturá-lo em médias ou modelos sem tratamento distorceria a leitura de tendência. Para o modelo preditivo, deve ser normalizado por mês ou excluído das comparações semestrais.

## Série semestral completa

| Semestre | Meses | Admissões | Desligamentos | Saldo |
| --- | --- | --- | --- | --- |
| 2021S1 | 6 | 9.456.760 | 7.922.793 | 1.533.967 |
| 2021S2 | 6 | 10.246.844 | 8.928.398 | 1.318.446 |
| 2022S1 | 6 | 11.458.253 | 10.086.451 | 1.371.802 |
| 2022S2 | 6 | 10.785.188 | 10.145.624 | 639.564 |
| 2023S1 | 6 | 11.772.099 | 10.759.373 | 1.012.726 |
| 2023S2 | 6 | 11.210.062 | 10.744.448 | 465.614 |
| 2024S1 | 6 | 13.027.721 | 11.723.351 | 1.304.370 |
| 2024S2 | 6 | 12.308.556 | 11.936.412 | 372.144 |
| 2025S1 | 6 | 13.763.059 | 12.549.044 | 1.214.015 |
| 2025S2 | 6 | 12.558.498 | 12.515.516 | **42.982** |
| 2026S1 | 6 | 13.812.546 | 12.912.674 | 899.872 |
| 2026S2 | 2 | 4.557.451 | 4.333.056 | 224.395 |

## Série de admissões (distribuição marginal)

**O que é uma distribuição marginal:** é o comportamento de **uma variável isolada**, ignorando todas as demais. O nome vem das tabelas de contingência: as distribuições "na margem" da tabela (somas das linhas e colunas) mostram cada variável separadamente, antes de qualquer cruzamento. Na prática, é o retrato individual da variável, onde ela se concentra, quanto varia e que forma tem. É o **primeiro passo obrigatório** da EDA porque não é possível entender relações entre variáveis (Seções 4 e 5) sem antes entender cada uma sozinha. Aqui trazemos: como as admissões semestrais se comportam, sozinhas.

| Estatística | Valor |
| --- | --- |
| Mínimo | 4.557.451 |
| Q1 | 10.650.602 |
| Mediana | 11.615.176 |
| Q3 | 12.675.804 |
| Máximo | 13.812.546 |
| Média | 11.246.420 |
| Desvio-padrão | 2.387.830 |
| Coeficiente de variação | 21,23% |

**Como ler cada estatística e por que ela está aqui:**

| Indicador | Por que buscamos | O que concluímos |
| --- | --- | --- |
| Mínimo / Máximo | Delimitam a amplitude do ciclo de negócio no período | De 4,56 mi (2026S2 parcial) a 13,81 mi (2026S1) |
| Q1 / Mediana / Q3 | Quartis são resistentes a extremos; mostram onde está a "maioria" dos semestres | Metade dos semestres entre 10,65 mi e 12,68 mi ou seja, mínimo é exceção, não regra |
| Média × Mediana | Média muito fora da mediana denuncia distorção por extremos | 11,25 mi vs 11,62 mi: diferença pequena, distorção contida |
| Desvio-padrão | Dispersão absoluta, na mesma unidade da variável | A demanda oscila ±2,39 mi em torno da média |
| **Coeficiente de variação (CV)** | O desvio-padrão sozinho não diz se 2,39 mi é muito ou pouco. O CV (DP ÷ média) expressa a dispersão em **termos relativos**, permitindo comparar volatilidade entre variáveis de escalas diferentes. Neste caso, admissões (milhões de unidades) vs salário (reais) | **21,23% = volatilidade alta**: a demanda flutua mais de um quinto do valor típico entre semestres. Conclusão de negócio: o planejamento de capacidade precisa assumir essa margem (não um nível constante), e o modelo preditivo precisa capturar tendência + sazonalidade para explicar essa variação ao invés de tratá-la como ruído |

### Recálculo sem o semestre parcial (2026S2)

Para blindar a leitura contra o artefato de cobertura, as mesmas estatísticas foram recalculadas **excluindo 2026S2** (11 semestres completos):

| Estatística | Com 2026S2 (12 sem) | Sem 2026S2 (11 sem) |
| --- | --- | --- |
| Mínimo | 4.557.451 | 9.456.760 |
| Q1 | 10.650.602 | 10.997.625 |
| Mediana | 11.615.176 | 11.772.099 |
| Q3 | 12.675.804 | 12.793.110 |
| Máximo | 13.812.546 | 13.812.546 |
| Média | 11.246.420 | 11.854.508 |
| Desvio-padrão | 2.387.830 | 1.335.223 |
| Coeficiente de variação | 21,23% | 11,26% |
| Assimetria | -1,6159 | -0,1137 |
| Curtose excedente | 2,4113 | -0,9582 |
| Shapiro-Wilk (p-value) | 0,8317 (0,0220) | 0,9713 (0,8990) |

**Por que isso importa:** isolado o efeito de cobertura, o retrato muda — e na direção de uma série **mais estável e bem-comportada**: o CV cai pela metade (21,23% → 11,26%, volatilidade moderada, não alta), a assimetria praticamente zera (-1,62 → -0,11) e a rejeição de normalidade no Shapiro-Wilk **desaparece inteiramente** (p passa de 0,0220 para 0,8990). Ou seja: a "não-normalidade" e a "alta volatilidade" da série eram artefatos do semestre parcial, não propriedades do mercado de trabalho. A coluna com 12 semestres permanece porque 2026S2 é dado real (jul–ago efetivamente ocorridos e completos mês a mês), mas **toda comparação semestral deve usar a coluna da direita**.

## Salário mediano de admissão

| Estatística | Valor |
| --- | --- |
| Mínimo | R$ 1.386,87 |
| Q1 | R$ 1.519,82 |
| Mediana | R$ 1.681,88 |
| Q3 | R$ 1.831,05 |
| Máximo | R$ 2.000,00 |
| Média | R$ 1.682,72 |

**Por que usar a mediana (e não a média):** a mediana é robusta a extremos, resistente a outliers ou seja, um semestre com muitas contratações de salários altos não arrasta o indicador. **Leitura de negócio:** o salário típico de contratação subiu de R$ 1.387 (mínimo, 2021S1) a R$ 2.000 (máximo na série), cerca de **+44%**. Isso significa que as vagas criadas ganham em remuneração, não apenas volume. Para o modelo, é **exógena candidata validada** (correlação 0,70 em t e 0,68 em t+1, Seção 6.2).

**Nota de cobertura:** o máximo de R$ 2.000,00 corresponde ao semestre parcial 2026S2; entre os 11 semestres completos, o máximo é R$ 1.961,41 (progressão de ~+41% sobre o mínimo). Ainda assim, a mediana de salário é **comparável mesmo com 2 meses** — é mediana por contratação (~4,4 milhões de registros em jul–ago), não soma do período, então não sofre distorção de cobertura como as admissões agregadas.

**O que é uma variável exógena:** é a que vem "de fora" do alvo que se quer prever ou seja, não é derivada do histórico da própria série de admissões, e sim de **outra medição do fenômeno** (aqui, a remuneração das contratações). Seu oposto são as variáveis **endógenas** (ou autoregressivas): os lags e as médias móveis, que são a própria série de admissões deslocada no tempo. O valor de negócio de uma exógena é trazer **informação que o histórico do alvo, sozinho, não contém**. Neste caso, se o salário típico de contratação anda junto com o volume do mês seguinte, ele antecipa a demanda de um jeito que olhar apenas os meses anteriores de admissões não captura. Aqui essa validação foi empírica: correlação de 0,68 com as admissões em t+1.

## Idade mediana de admissão

| Estatística | Valor |
| --- | --- |
| Mínimo | 30 anos |
| Mediana | 30 anos |
| Máximo | 31 anos |
| Variação | 1 ano |

**Por que olhar idade:** retrata o perfil demográfico de quem está sendo contratado. Estabilidade total (30–31 anos em todo o período) indica que a demanda cresce **sem mudança estrutural de perfil**. Podemos deixar como hipótese que não há migração para vagas mais seniores ou mais jovens. Isso valida usar o volume (admissões) como série principal, sem estratificar por idade nesta versão.

---

# SEÇÃO 2: Distribuições Marginais (Bussab & Moretin)

## 2.1 Distribuição de Admissões Semestrais

**Por que testar normalidade:** a maior parte da inferência clássica (intervalos de confiança, testes t, regressão linear) assume normalidade. Saber antecipadamente que a série viola essa suposição nos diz: (i) resumir por medianas e quartis, não por médias; (ii) usar Spearman junto com Pearson; (iii) aplicar log-transformação antes de modelar. Exatamente o que a Seção 7 recomenda.

**Testes de normalidade:**

| Teste | Estatística | p-value | Conclusão |
| --- | --- | --- | --- |
| Shapiro-Wilk | 0,8317 | 0,0220 | ⚠️ Rejeita normalidade |
| Kolmogorov-Smirnov | 0,1734 | 0,8054 | Não rejeita |

- **Assimetria (skewness):** -1,6159 Negativa (cauda à esquerda): semestres muito abaixo do típico (o parcial de 2026S2) afastam-se mais do centro do que os acima; por isso a média fica abaixo da mediana
- **Curtose (kurtosis):** 2,4113 Curtose excedente positiva: caudas mais pesadas que a normal, coerente com o ponto extremo de 2026S2
- **Leitura:** o mínimo de 2026S2 (4,56 milhões no semestre parcial, apenas jul–ago) puxa a cauda esquerda; a despeito do KS, o Shapiro-Wilk sinaliza desvio de normalidade.
- **Contraprova sem o semestre parcial:** recalculando sobre os 11 semestres completos, Shapiro-Wilk W = 0,9713 e p = 0,8990 (KS: D = 0,0954, p = 0,9997) — **compatível com normalidade**. A rejeição acima é inteiramente explicada pelo artefato de cobertura, não pela forma da distribuição real dos semestres.

![Distribuição marginal: admissões semestrais](graficos/02_01_distribuicao_admissoes.png)

*Versão interativa (plotly): [graficos/02_01_distribuicao_admissoes.html](graficos/02_01_distribuicao_admissoes.html)*

## 2.2 Distribuição de Salário Mediano

**Testes de normalidade:**

| Teste | Estatística | p-value | Conclusão |
| --- | --- | --- | --- |
| Shapiro-Wilk | 0,9566 | 0,7348 | ✅ Compatível com normal |
| Kolmogorov-Smirnov | 0,1077 | 0,9962 | Não rejeita |

- O salário mediano de admissão é a variável com comportamento mais próximo da normal (progressão suave de ~R$ 1.387 a R$ 2.000).
- **Por que isso importa:** normalidade aqui significa evolução **estável e previsível** ou seja, pode entrar em modelos lineares sem transformação e serve de referência confiável para pricing de vagas. É o contraste com as admissões: **volume é volátil; remuneração é estável**. Essa complementariedade é o que justifica o salário entrar como exógena no modelo.

![Distribuição marginal: salário mediano de admissão](graficos/02_02_distribuicao_salario.png)

*Versão interativa (plotly): [graficos/02_02_distribuicao_salario.html](graficos/02_02_distribuicao_salario.html)*

## 2.3 Distribuição de Idade Mediana

**Testes de normalidade:**

| Teste | Estatística | p-value | Conclusão |
| --- | --- | --- | --- |
| Shapiro-Wilk | 0,5521 | 0,0000 | ⚠️ Rejeita normalidade |
| Kolmogorov-Smirnov | 0,4681 | 0,0062 | Rejeita |

- A idade mediana é discreta (apenas 30 ou 31 anos) e a rejeição forte da normalidade é **artefato da discretização**, não anomalia de mercado de trabalho.
- **Por que essa distinção importa:** aplicar tratamento de "anomalia" a um artefato estatístico seria erro de método. A lição aqui é: **o teste estatístico aponta, mas é o contexto quem decide**: Antes de tratar algo como outlier, pergunte se é erro de dado, evento real ou efeito de cobertura.

![Distribuição marginal: idade mediana de admissão](graficos/02_03_distribuicao_idade.png)

*Versão interativa (plotly): [graficos/02_03_distribuicao_idade.html](graficos/02_03_distribuicao_idade.html)*

---

# SEÇÃO 3: Detecção Robusta de Outliers

**Por que detectar outliers:** extremos distorcem médias, regressões e previsões — um único valor atípico pode arrastar a linha de tendência de um modelo. O objetivo é duplo: (i) proteger o modelo futuro e (ii) **distinguir três tipos de extremo** — erro de dado (corrigir), evento real (manter e explicar) e artefato de cobertura (excluir de comparações). Usamos dois métodos porque cada um tem um ponto cego.

## 3.1 Método IQR (Interquartile Range)

| Variável | Q1 | Q3 | IQR | Limites | Outliers |
| --- | --- | --- | --- | --- | --- |
| Admissões | 10.650.602,00 | 12.675.803,75 | 2.025.201,75 | [7.612.799,38 ; 15.713.606,38] | 1 (8,33%) |
| Salário | 1.519,82 | 1.831,05 | 311,23 | [1.052,97 ; 2.297,90] | 0 (0,00%) |
| Idade | 30,00 | 30,25 | 0,25 | [29,62 ; 30,62] | 3 (25,00%) |

- **Admissões:** o único outlier é 2026S2 (4.557.451), abaixo do limite inferior — efeito de cobertura (semestre parcial com 2 meses), não erro de dado.
- **Idade:** os "outliers" refletem apenas a discretização (valores 31 fora do IQR degenerado de 0,25).
- **Por que IQR:** é o clássico de Tukey (fora de Q1−1,5×IQR / Q3+1,5×IQR) — resistente porque os limites vêm de quartis, imunes aos próprios extremos. Ponto cego: quando a variável é quase constante (idade, IQR = 0,25), **qualquer** valor fora do padrão vira "outlier" — os 25% flagrados aqui são falsos positivos, não anomalias.

## 3.2 Método MAD (Median Absolute Deviation)

| Variável | Mediana | MAD | Outliers (\|z_MAD\| > 2,5) |
| --- | --- | --- | --- |
| Admissões | 11.615.176,00 | 1.155.827,00 | 1 (8,33%) |
| Salário | 1.681,88 | 172,79 | 0 (0,00%) |
| Idade | 30,00 | 0,00 | 0 (0,00%) |

- Os dois métodos robustos **convergem**: apenas 2026S2 (parcial) é outlier em admissões; salário e idade não têm anomalias.
- **Por que dois métodos:** o MAD usa a mediana (ainda mais resistente que os quartis) com escore-z robusto; quando IQR e MAD apontam o mesmo registro, a classificação é confiável. **Conclusão acionável:** não há erro de dado na silver — o único extremo é o semestre parcial, que deve ser tratado como caso especial de cobertura, e não removido da história.
- **Contraprova sem 2026S2:** recalculados sobre os 11 semestres completos, IQR (limites [8.304.398 ; 15.486.336]) e MAD (mediana 11.772.099, MAD 986.911) retornam **0 outliers** — os dois métodos continuam convergindo, agora para “nenhuma anomalia”. Confirma-se que a base não tem erro de dado; o único extremo era o efeito de cobertura.

---

# SEÇÃO 4: Relações Bivariadas

## 4.1 Correlações com Admissões

| Par | Pearson | p-value | Spearman | p-value |
| --- | --- | --- | --- | --- |
| Admissões × Desligamentos | **0,9794** | 0,0000 | 0,9580 | 0,0000 |
| Admissões × Salário | 0,0202 | 0,9503 | 0,4685 | 0,1245 |
| Admissões × Saldo | 0,2235 | 0,4850 | — | — |

**Por que medir correlações — e duas (Pearson e Spearman):** correlação é a base da seleção de variáveis do modelo: só entra como feature o que se relaciona com o alvo. São duas medidas porque captam coisas diferentes — **Pearson** mede relação *linear* (e é sensível a extremos); **Spearman** mede relação *monotônica* qualquer (resistente a extremos). Divergência entre as duas é sintoma de outlier ou de não-linearidade.

**Leitura e conclusões de negócio:**

- **Admissões × Desligamentos = 0,98 (quase perfeita):** é a **lei da rotatividade** — mercados que contratam mais também desligam mais. Conclusão prática nº 1: **não usar as duas juntas** como features de um modelo linear (multicolinearidade: o modelo não consegue separar os efeitos). Conclusão prática nº 2: os desligamentos são o melhor *proxy* antecedente das admissões do mês seguinte (0,69 em t+1, Seção 6.2).
- **Admissões × Salário (Pearson 0,02; Spearman 0,47):** não há relação linear volume × remuneração, mas existe associação monotônica parcial — ambas sobem com o tempo, então a relação é **temporal**, não direta. Isso justifica incluir salário defasado como exógena (0,68 em t+1 na série mensal).
- **Admissões × Saldo (0,22, não-significativo):** o saldo é resíduo (admissões − desligamentos) e, como as duas parcelas são quase colineares, o saldo quase não se relaciona com o volume. Serve como **indicador de ciclo** isolado (ex.: alerta 2025S2), não como feature de volume.

![Relações bivariadas: correlações com admissões](graficos/04_01_correlacoes_bivariadas.png)

*Versão interativa (plotly): [graficos/04_01_correlacoes_bivariadas.html](graficos/04_01_correlacoes_bivariadas.html)*

---

# SEÇÃO 5: Análise Temporal — Série Semestral

## 5.1 Decomposição STL (period = 2)

**Por que decompor a série:** previsão exige entender de que padrões a série é feita. A decomposição separa a série em **tendência** (para onde vamos no longo prazo), **sazonalidade** (o padrão que se repete a cada ciclo — aqui, semestres) e **resíduos** (o que sobra de imprevisível). Cada parte determina uma decisão de negócio: tendência → crescimento de capacidade; sazonalidade → calendário de contratação; resíduos → margem de erro inevitável de qualquer modelo.

- ✅ Decomposição concluída (modelo aditivo, `period=2`, dados semestrais)
- **Variância explicada (tendência + sazonalidade):** **8,64%** (`1 − var(resíduo)/var(série)`). Ou seja, com period=2, a decomposição deixa cerca de 91% da variância no resíduo: tendência + sazonalidade explicam pouco da série. Com apenas 12 semestres, essa leitura é cautelosa, e não se deve concluir que a sazonalidade domina o padrão.

![Decomposição STL da série de admissões](graficos/05_01_decomposicao_stl.png)

*Versão interativa (plotly): [graficos/05_01_decomposicao_stl.html](graficos/05_01_decomposicao_stl.html)*

## 5.2 Estacionaridade (ADF), Autocorrelação (ACF) e Correlação Parcial (PACF)

**Por que testar estacionaridade:** ARIMA e métodos afins só funcionam em séries *estacionárias* (média e variância constantes). Se a série tem tendência, o modelo "aprende" que sempre sobe e falha quando o ciclo muda. O teste ADF responde se é preciso diferenciar a série antes de modelar. Já ACF/PACF mostram **a memória da série** — quantos períodos passados influenciam o valor atual — e são os gráficos usados para escolher as ordens p e q de um ARIMA.

**Teste de Dickey-Fuller Aumentado (maxlag=1, série curta de 12 pontos):**

| Estatística ADF | p-value | Conclusão |
| --- | --- | --- |
| -2,1715 | 0,2168 | ⚠️ Série **não-estacionária** |

- A série de admissões semestrais precisa de diferenciação (ou modelagem de tendência/sazonalidade) antes de métodos ARIMA clássicos.
- ACF decai gradualmente (persistência/tendência); PACF com picos nos primeiros lags — padrão típico de processo com raiz unitária ou tendência.
- **Conclusão de negócio:** a demanda por contratações não é um fenômeno "aleatório em torno de um nível" — carrega tendência de crescimento e memória entre períodos. Para o modelo, isso dita: diferenciar a série (ou usar termos de tendência/sazonalidade) e validar no nível **mensal**, que tem 68 pontos e estimadores mais estáveis que os 12 semestrais.

![ACF e PACF da série de admissões](graficos/05_02_acf_pacf.png)

*Versão interativa (plotly): [graficos/05_02_acf_pacf.html](graficos/05_02_acf_pacf.html)*

---

# SEÇÃO 6: Feature Engineering para Séries Temporais

> **Escopo:** nesta versão o cruzamento com a base FATEC foi removido — o EDA concentra-se exclusivamente nos dados CAGED.

**Por que construir features:** um modelo não enxerga "o mercado de trabalho" — ele enxerga colunas numéricas. O feature engineering traduz a história econômica em sinais mensuráveis: o mês anterior (*lag* — inércia), a média dos últimos meses (*momentum*), o mesmo mês do ano anterior (sazonalidade), a posição no calendário (ciclo anual) e exógenas defasadas (desligamentos, salário). Tudo calculado **só com informação do passado**: "sem vazamento" significa não usar nada que só seria conhecido depois do mês que se quer prever — um modelo com vazamento parece excelente no treino e falha em produção.

## 6.1 Série mensal e features candidatas para o ML

Série mensal agregada direto do bronze (`_competencia_referencia`), 2021-01 a 2026-08:

- **68 meses** (202101 a 202608)
- Admissões (tipos 10, 20, 25, 35, 70, 97) e desligamentos (tipos 31, 32, 33, 40, 43, 45, 50, 60, 80, 90, 98) contados na mesma varredura; mediana de salário calculada apenas sobre as admissões
- *Nota de execução:* a consulta original filtrava só admissões (o que zerava `desligamentos`); foi corrigida nesta re-execução para computar ambos os fluxos

**Features candidatas:** `adm_lag_1m`, `adm_lag_3m`, `adm_lag_6m`, `adm_lag_12m`, `adm_media_3m`, `adm_media_12m`, `adm_std_3m`, `mes_sin`, `mes_cos`, `adm_yoy`, `desl_lag_1m`, `saldo_lag_1m`, `salario_lag_1m`, `t` (todas defasadas para evitar vazamento de futuro).

**Amostra da série mensal (15 primeiros meses):**

| Competência | Admissões | Desligamentos | Saldo | Mediana salário (R$) |
| --- | --- | --- | --- | --- |
| 202101 | 1.550.075 | 1.293.016 | 257.059 | 1.372,00 |
| 202102 | 1.715.425 | 1.317.510 | 397.915 | 1.364,42 |
| 202103 | 1.626.885 | 1.450.555 | 176.330 | 1.392,00 |
| 202104 | 1.396.311 | 1.282.389 | 113.922 | 1.408,00 |
| 202105 | 1.558.316 | 1.279.611 | 278.705 | 1.387,25 |
| 202106 | 1.609.748 | 1.299.712 | 310.036 | 1.400,00 |
| 202107 | 1.666.051 | 1.349.326 | 316.725 | 1.400,00 |
| 202108 | 1.819.411 | 1.446.067 | 373.344 | 1.400,00 |
| 202109 | 1.789.967 | 1.472.974 | 316.993 | 1.403,10 |
| 202110 | 1.760.739 | 1.507.656 | 253.083 | 1.415,00 |
| 202111 | 1.772.766 | 1.448.654 | 324.112 | 1.416,00 |
| 202112 | 1.437.910 | 1.703.721 | **-265.811** | 1.415,02 |
| 202201 | 1.777.646 | 1.622.468 | 155.178 | 1.466,00 |
| 202202 | 2.013.143 | 1.684.636 | 328.507 | 1.453,15 |
| 202203 | 1.953.071 | 1.816.882 | 136.189 | 1.476,00 |

*(dez/2021 é o único mês com saldo negativo da amostra — típico do ajuste de fim de ano)*

![Série mensal de admissões — CAGED](graficos/06_01_serie_mensal.png)

*Versão interativa (plotly): [graficos/06_01_serie_mensal.html](graficos/06_01_serie_mensal.html)*

- **Leitura:** tendência de alta consistente (média móvel 12m ascendente, refletindo o crescimento de ~46% no período), com sazonalidade mensal marcada — vales no fim do ano (ex.: dez/2021, 1,44 milhão) e picos no início/meio do ano (ex.: fev/2022, 2,01 milhões).

## 6.1.1 Índice Sazonal Mensal — o calendário de contratação do mercado

**O que é:** o peso médio de cada mês nas admissões do ano — share do mês no total anual, média dos **5 anos completos** (2021–2025; 2026 excluído por incompleto). O mês "neutro" seria 1/12 = **8,33%**: meses acima contratam mais que o proporcional, meses abaixo contratam menos.

| Mês | Peso médio | vs. mês neutro (8,33%) | Leitura |
| --- | --- | --- | --- |
| Janeiro | 8,16% | −0,17 p.p. | recomposição pós-férias coletivas |
| **Fevereiro** | **8,98%** | **+0,65 p.p.** | **pico do 1º semestre** — orçamento novo, contratações de início de ano |
| Março | 8,78% | +0,45 p.p. | continuação do pico |
| Abril | 8,23% | −0,10 p.p. | neutro |
| Maio | 8,47% | +0,14 p.p. | neutro |
| Junho | 8,27% | −0,06 p.p. | neutro |
| Julho | 8,46% | +0,13 p.p. | neutro |
| **Agosto** | **8,98%** | **+0,65 p.p.** | **pico do 2º semestre** — volta às aulas e 2ª onda de contratação |
| Setembro | 8,67% | +0,34 p.p. | acima do neutro |
| Outubro | 8,57% | +0,24 p.p. | acima do neutro |
| Novembro | 8,06% | −0,27 p.p. | começa a frear |
| **Dezembro** | **6,37%** | **−1,96 p.p.** | **vale profundo** — férias coletivas e encerramento de ciclo |

**Como ler:** 10 dos 12 meses vivem num intervalo estreito (8,1%–9,0%) — o ano é relativamente plano, com **duas salas de máquinas (fev–mar e ago–out) e um despenque em dezembro** (−1,96 p.p. abaixo do neutro, o dobro da distância de qualquer outro mês).

**Por que isso importa (negócio):** este é o calendário que todo planejador de contratação precisa saber de cor — (i) **capacidade de atendimento** dimensionada para fev–mar e ago–out, não para a média do ano; (ii) **dezembro não serve de baseline** para comparação alguma — comparar dezembro com novembro é comparar meses de naturezas diferentes; (iii) para o modelo, o índice é a base dos **dummies/harmônicos sazonais** (`mes_sin`, `mes_cos`, Seção 6.2) e explica por que `adm_lag_12m` carrega tanta informação (0,50 em t+1): o mesmo mês do ano anterior é o calendário em forma de feature. *(Calculado em 02/11/2026 sobre a série mensal da silver, anos completos — atende à recomendação 1 da Seção 7.2.)*

## 6.2 Validação das features (correlação com o alvo corrente e t+1)

Correlação de Pearson entre cada feature e as admissões em **t** e em **t+1** (poder preditivo real), sem vazamento de futuro:

**Correlação com admissões (t):**

| Feature | Pearson r | p-value |
| --- | --- | --- |
| adm_lag_12m | 0,8537 | 0,0000 |
| desl_lag_1m | 0,7638 | 0,0000 |
| t | 0,7134 | 0,0000 |
| salario_lag_1m | 0,7003 | 0,0000 |
| adm_lag_1m | 0,6430 | 0,0000 |
| adm_media_3m | 0,5448 | 0,0000 |
| adm_media_12m | 0,5355 | 0,0000 |
| adm_lag_6m | 0,5219 | 0,0000 |
| adm_std_3m | 0,3687 | 0,0025 |
| adm_lag_3m | 0,3563 | 0,0036 |
| mes_sin | 0,0737 | 0,5502 |
| adm_yoy | 0,0530 | 0,6983 |
| saldo_lag_1m | -0,1311 | 0,2904 |
| mes_cos | -0,2554 | 0,0356 |

**Correlação com admissões (t+1) — poder preditivo real:**

| Feature | Pearson r | p-value |
| --- | --- | --- |
| t | 0,7016 | 0,0000 |
| desl_lag_1m | 0,6931 | 0,0000 |
| salario_lag_1m | 0,6831 | 0,0000 |
| adm_media_12m | 0,5101 | 0,0001 |
| adm_lag_12m | 0,5037 | 0,0001 |
| adm_std_3m | 0,4373 | 0,0003 |
| adm_media_3m | 0,4148 | 0,0007 |
| adm_lag_6m | 0,4067 | 0,0011 |
| adm_lag_1m | 0,4042 | 0,0008 |
| adm_lag_3m | 0,3495 | 0,0046 |
| mes_sin | 0,1959 | 0,1120 |
| adm_yoy | -0,1079 | 0,4331 |
| mes_cos | -0,1541 | 0,2130 |
| saldo_lag_1m | -0,3659 | 0,0025 |

**Por que medir a correlação em t e em t+1 separadamente:** a correlação com o valor *corrente* (t) mostra associação — mas pode ser inútil para prever, porque no momento da previsão você ainda não conhece o mês corrente. A correlação com **t+1** é o teste de utilidade real: só features calculáveis *hoje* que se relacionam com o *próximo* mês têm poder preditivo verdadeiro. É a diferença entre "as variáveis andam juntas" e "esta variável ajuda a antecipar".

**Leitura e conclusões de negócio:**

- **Pódio em t+1 — tendência (`t`, 0,70), desligamentos defasados (0,69) e salário defasado (0,68):** para prever o mês que vem, o que mais informa é (i) a trajetória de crescimento, (ii) a rotatividade do mês que acabou (empresas que desligam já reposicionam vagas) e (iii) a remuneração em alta das contratações. Notável: o lag-1 (mês imediatamente anterior, 0,40) fica **atrás** das exógenas — a demanda não é pura inércia.
- **Lags de 6–12 meses e médias 12m (0,35–0,51):** carregam o padrão sazonal (mesma época do ano anterior) — essenciais para capturar o calendário de contratações.
- **`saldo_lag_1m` negativo em t+1 (-0,37):** meses de saldo (admissões − desligamentos) muito alto antecedem *desaceleração* — após um mês de contratação líquida forte, o refluxo natural é menor admissão no mês seguinte. É sinal de **ciclo**, não de tendência.
- **Todas as top-10 são significativas (p < 0,005)** — a ordenação não é ruído amostral; e como nenhuma feature passa de 0,71, o próximo mês é explicado por poucos sinais fortes + imprevisibilidade: o modelo terá erro não-nulo, e isso é esperado (não falha).

---

# SEÇÃO 7: Validação para Silver Layer & Recomendações

## 7.1 Checklist de Qualidade

**Por que validar:** cada item abaixo existe porque um consumidor da silver (dashboard, modelo, auditoria) assume essas propriedades como verdadeiras. A validação transforma a tabela de "provavelmente certa" em **confiável para decisão** — e documentada para governança.

**1. Cobertura temporal**
- ✅ Período completo: 2021S1 a 2026S2
- ✅ Meses cobertos: 68 de 72 possíveis
- ⚠️ 2026S2 parcial (apenas 2 meses de 6)

**2. Valores nulos**
- ✅ Sem valores nulos detectados

**3. Consistência de cálculos**
- ✅ Saldo = Admissões − Desligamentos: 0 inconsistências

**4. Outliers e valores suspeitos**
- Salários: 0 negativos, 0 acima de R$ 100 mil
- Idades: 0 abaixo de 15 anos, 0 acima de 80 anos
- ✅ Nenhum valor suspeito (tabela já em Silver)

**5. Rastreabilidade**
- ✅ Tabela: `workspace.silver.novo_caged_movimentacoes_semestral`
- ✅ Derivada de: `workspace.silver.novo_caged_movimentacoes`
- ✅ Referência FATEC: `workspace.silver.cursos_fatec_ocupacoes_cbo_2025` (fora do escopo do cruzamento nesta versão)

## 7.2 Recomendações Finais

### Para o modelo preditivo

1. **Tratamento de sazonalidade** — padrão sazonal claro; testar ARIMA/SARIMA, exponential smoothing ou Prophet; considerar dummies sazonais ou log-transformação
2. **Estratificação por UF e Seção CNAE** — EDA atual é agregada (Brasil total); próxima fase UF × Seção para detectar regionalismos
3. **Escopo da sprint: 100% CAGED** — modelo passa a prever a demanda total (série mensal CAGED); features candidatas: lags, janelas móveis e sazonalidade cíclica (Seção 6)
4. **Transformações de dados** — Log(Admissões) é mais normal que admissões brutas; testar Box-Cox para salário; normalizar antes de algoritmos sensíveis (KNN, SVM)
5. **Detecção de pontos de mudança** — 2025S2 teve saldo quase nulo (+42 mil): investigar causas (recessão ou anomalia de coleta); considerar modelos com mudança de regime

### Para o dashboard

1. ✅ **Índices sazonais mensais** — incorporados como Seção 6.1.1 (dashboard CAGED, 02/11/2026)
2. Criar **série por UF** (top 5 estados)
3. Adicionar os **artefatos da Seção 6** (features mensais) ao pipeline de treino/MLflow
4. Incluir **intervalo de confiança 95%** nas projeções

---

# Conclusão

**Em uma frase de negócio:** a demanda por contratações cresceu ~46% entre 2021 e 2026, com sazonalidade previsível, salário de contratação em alta estável e dois pontos de atenção (saldo quase nulo em 2025S2; semestre parcial de 2026S2) — condições ideais para um modelo de previsão mensal com lags, exógenas defasadas e componente sazonal.

Esta EDA rigorosa segundo **Bussab & Moretin (2010)** revelou:

- ✅ **Estrutura clara** da série semestral (2021S1–2026S2, com 2026S2 parcial)
- ✅ **Tendência de crescimento** em admissões (~46% em 5 anos)
- ✅ **Sazonalidade estável** (para modelagem temporal)
- ✅ **Correlação forte** entre admissões e desligamentos (0,98 na re-execução com 12 semestres)
- ⚠️ **Alerta 2025S2:** saldo quase nulo — requer investigação
- ✅ **Features temporais candidatas** validadas (lags, janelas móveis, sazonalidade cíclica, exógenas defasadas)

### Próximas etapas

1. Criar tabelas agregadas por **UF × Semestre** e **Seção × Semestre**
2. Expandir a análise a nível **mensal** (maior granularidade do modelo)
3. Implementar **testes de mudança de regime** (change-point detection)
4. Modelagem preditiva com **ARIMA/Prophet + estratificação regional**
5. Completar 2026 quando set–dez forem ingeridos e revalidar

---

# Apêndice: Artefatos

| Artefato | Caminho |
| --- | --- |
| Notebook EDA (fonte) | `notebooks/03_analytics/EDA` |
| Notebook gerador dos gráficos | `notebooks/03_analytics/EDA (1)/00_EDA_CAGED/gerar_graficos_eda` |
| Gráficos estáticos (PNG) | `graficos/*.png` (7 gráficos) |
| Gráficos interativos (plotly) | `graficos/*.html` (7 gráficos) |

**Notas técnicas da geração deste relatório:**

- Todos os números desta página provêm da re-execução completa do notebook EDA em 2026-10-30 (execução em ordem, sequências 1→32).
- Correção aplicada na re-execução (célula 6.1): `data_mes` convertido para `datetime64` (chegava como `object` via Arrow) e os desligamentos passaram a ser contados por CASE na mesma varredura — a consulta original restringia o WHERE às admissões, o que zerava a coluna `desligamentos` da série mensal.
- Os PNGs são renderizações matplotlib (o kaleido não tem Chrome no compute serverless); os HTMLs são os gráficos plotly originais, interativos.

**EDA concluída em 2026-10-26** · **Relatório compilado em 2026-10-30** · Autora: Fernanda Carnevalle de Melo