# EDA da Formação Profissional INEP (Censo da Educação Superior)
## Análise Exploratória segundo Bussab & Moretin (2010)

**Autora:** Fernanda Carnevalle de Melo  
**Data da EDA:** 2026-10-30 · **Base:** Censo da Educação Superior INEP, 2021–2024  
**Tabelas:** `workspace.gold.fato_inep_educacao_brasil_anual` + `workspace.gold.fato_inep_educacao_uf_anual` (v2, gravadas pelo notebook `031_silver_to_gold_inep`) + `workspace.silver.inep_superior_cursos` (2,41 mi linhas, granular por curso × município × IES)  
**Escopo:** formação educacional (oferta, ingresso, estoque e conclusão) — contraponto estrutural da EDA CAGED (demanda do mercado de trabalho)  
**Adaptação metodológica:** dado censitário **anual** com 4 pontos temporais (2021–2024). Séries com n=4 não sustentam STL, ADF ou ACF (poder estatístico insuficiente) — a EDA é **transversal** (distribuições por campo CINE, UF e modalidade) com evolução descritiva 2021→2024.

---

## Metodologia

Esta análise segue os princípios de **Bussab & Moretin (2010)**, adaptados à natureza censitária e transversal da base:

1. **Exploração de distribuições marginais** — cada variável isoladamente (campo CINE, UF, modalidade)
2. **Detecção de outliers e anomalias** — univariada (IQR e MAD)
3. **Análise de relações bivariadas** — correlações de Pearson e Spearman (oferta × demanda educacional)
4. **Evolução temporal descritiva** — 4 pontos anuais, variação 2021→2024 e participação da modalidade EaD
5. **Feature engineering para integração com o CAGED** — indicadores candidatos a exógenas do modelo de demanda
6. **Validação de dados** — checklist de qualidade das camadas silver/gold

### Referências Bibliográficas

- Bussab, W. O., & Moretin, P. A. (2010). *Estatística Básica* (6ª ed.). São Paulo: Saraiva.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- INEP (2024). *Dicionário de dados do Censo da Educação Superior*. Microdados.
- Rousseeuw, P. J., & Hubert, M. (2011). "Robust statistics for outlier detection." *Wiley Interdisciplinary Reviews*, 1(1), 73–79.

---

## Integridade da Base (verificação inicial)

| Métrica | Valor |
| --- | --- |
| Camadas | bronze + silver + gold (v2) |
| Cobertura | 4 Censos completos: 2021, 2022, 2023, 2024 |
| Registros na silver | 2.410.764 (curso × município × IES × CINE × modalidade) |
| UFs na gold | 27 (26 estados + DF) — completo |
| IES distintas | ~2.561 (2024) |
| Campos CINE (rótulo) | 353 (2024), hierarquia em 3 níveis + `gold.dim_cine_brasil` (372 rótulos) |

**As 4 dimensões territoriais da silver (`tipo_dimensao`)** — peça-chave para não somar errado:

| Dim | Conteúdo | UF | Vagas 2024 |
| --- | --- | --- | --- |
| 1 | Presencial localizado | 27 UFs | 5.075.146 |
| 2 | EaD territorializado | tem UF | ~7 mil |
| 3 | EaD nacional | sem UF (por design) | 18.583.348 |
| 4 | Sem localização | sem UF | 0 |

**Regras da Gold v2** (validadas no notebook 031, diferenças silver×gold = 0 em todas as medidas e anos):

- Estudantes (ingressantes, matrículas, concluintes): dimensões 1 + 2 (presencial + EaD territorializado)
- Oferta (cursos, vagas, inscritos): **somente dimensão 1** — oferta presencial. A oferta EaD nacional (18,6 mi de vagas em 2024) existe **apenas na silver**
- ⚠️ **Nunca somar `quantidade_vagas` da silver sem filtrar `tipo_dimensao`**
- Os 11.778 registros sem UF (2024) são estruturais (dim 3 + dim 4 + 9 exceções de EaD sem sede), não sujeira

**Por que essa verificação importa:** a mesma disciplina da EDA CAGED (2026S2 parcial) se aplica aqui em outra forma: o risco desta base não é mês incompleto, é **dupla contagem de dimensões** e **oferta que parece sumir**. Saber de antemão que "vagas" da gold é presencial evita a conclusão errada de que o Brasil oferta poucas vagas — a oferta EaD é 3,7× a presencial e mora na silver.

---

# SEÇÃO 1: Resumo Executivo

## Cobertura e evolução anual (gold Brasil v2)

| Ano | Ingressantes | Matrículas | Concluintes | Cursos pres. | Vagas pres. | Inscritos pres. |
| --- | --- | --- | --- | --- | --- | --- |
| 2021 | 3.943.733 | 8.984.396 | 1.326.961 | 35.482 | 5.942.212 | 8.644.865 |
| 2022 | 4.755.158 | 9.441.290 | 1.287.136 | 35.774 | 5.658.590 | 8.811.102 |
| 2023 | 4.992.486 | 9.974.435 | 1.374.287 | 35.410 | 5.440.999 | 8.627.123 |
| 2024 | 5.009.116 | 10.224.686 | 1.333.515 | 34.479 | 5.075.146 | 8.658.561 |

## Indicadores-síntese 2021 → 2024

| Indicador | 2021 | 2024 | Variação | Leitura |
| --- | --- | --- | --- | --- |
| Matrículas totais | 8.984.396 | 10.224.686 | **+13,8%** | expansão do estoque |
| Ingressantes | 3.943.733 | 5.009.116 | **+27,0%** | entrada acelerada |
| Concluintes | 1.326.961 | 1.333.515 | +0,5% | saída estagnada |
| Vagas presenciais | 5.942.212 | 5.075.146 | **−14,6%** | contração da oferta presencial |
| Inscritos presenciais | 8.644.865 | 8.658.561 | +0,2% | procura presencial estável |
| Inscritos por vaga presencial | 1,45 | **1,71** | +18% | disputa por vaga crescendo |
| Matrículas EaD (share) | 41,3% | **50,7%** | +9,4 p.p. | EaD ultrapassa presencial |
| Ingressantes EaD (share) | 62,8% | **66,8%** | +4,0 p.p. | 2 de cada 3 novos alunos são EaD |

**Por que isso importa:** o retrato estrutural é de **transição de modalidade com aperto de oferta presencial**: o estoque cresce (+13,8%), mas a oferta presencial contrai (vagas −14,6%) enquanto a procura por vaga sobe (1,45 → 1,71 inscritos/vaga). O motor do crescimento é o **EaD** — hoje mais da metade das matrículas e dois terços dos ingressantes. Para o modelo de demanda profissional (CAGED), isso significa: a formação de mão de obra está migrando de canal, e qualquer projeção de "concluintes entrando no mercado" precisa modelar as duas modalidades separadamente, porque o presencial encolhe e o EaD explode.

---

# SEÇÃO 2: Distribuições Marginais (Bussab & Moretin)

## 2.1 Matrículas por campo de formação (CINE rótulo, 2024)

**Distribuição marginal** — comportamento de uma variável isolada (conceito detalhado na EDA CAGED, Seção 1). Aqui: como as 10,2 milhões de matrículas se distribuem pelos 353 campos de formação, sozinhos, sem cruzamento.

| Estatística | Valor |
| --- | --- |
| n (campos CINE) | 353 |
| Mínimo | 1 |
| Q1 | 452 |
| Mediana | 2.327 |
| Q3 | 15.716 |
| Máximo | 887.502 (Pedagogia) |
| Média | 28.965 |
| Desvio-padrão | 88.314 |
| **Coeficiente de variação** | **304,9%** |
| Assimetria | +5,83 |
| Curtose excedente | +41,26 |

**Testes de normalidade:**

| Teste | Estatística | p-value | Conclusão |
| --- | --- | --- | --- |
| Shapiro-Wilk (bruto) | 0,3464 | 1,4e-33 | ⚠️ Rejeita normalidade |
| Shapiro-Wilk (log) | 0,9925 | 0,0734 | ✅ Compatível com normal |

- **A distribuição é log-normal:** a rejeição violenta no bruto (assimetria +5,83, curtose +41) **desaparece após log-transformação** — o mesmo diagnóstico que o CAGED exigiu contraprova para provar, aqui é direto: o tamanho dos campos de formação multiplica, não soma.
- **Como ler:** a mediana (2.327) é 12× menor que a média (28.965) — metade dos campos é minúscula, enquanto Pedagogia (887 mil), Direito (653 mil) e Administração (653 mil) concentram o mercado. O CV de 304,9% é esperado e **não é "volatilidade"**: é concentração estrutural da oferta educacional brasileira.

**Por que isso importa:** a lição metodológica é a mesma da idade mediana no CAGED (Seção 2.3): o teste estatístico aponta, o contexto decide. Aqui o contexto diz "campo educacional é escala livre" — então o correto é (i) resumir por **mediana e quartis**, nunca por média; (ii) **modelar em log** (a correlação de Pearson em bruto será dominada por Pedagogia/Direito/Administração); (iii) usar Spearman sempre como contraponto. É a mesma disciplina do "2026S2 parcial" — identificar o artefato antes de interpretar o número.

## 2.2 Concentração por área CINE geral (2024)

| Área CINE | Matrículas | Share matrículas | Share ingressantes | Var. 2021→2024 |
| --- | --- | --- | --- | --- |
| Negócios, administração e direito | 2.755.028 | 26,9% | 29,7% | +4,7% |
| Saúde e bem-estar | 2.345.570 | 22,9% | 20,7% | **+25,0%** |
| Educação | 1.758.118 | 17,2% | 16,8% | +5,9% |
| Engenharia, produção e construção | 887.402 | 8,7% | 7,1% | **−5,4%** |
| Computação e TIC | 799.800 | 7,8% | **9,8%** | +15,3% |
| Ciências sociais, comunicação e informação | 604.611 | 5,9% | 4,9% | +9,1% |
| Agricultura, silvicultura, pesca e veterinária | 356.018 | 3,5% | 2,5% | −2,4% |
| Serviços | 271.869 | 2,7% | 3,8% | +7,4% |
| Artes e humanidades | 256.838 | 2,5% | 2,9% | +5,2% |
| Ciências naturais, matemática e estatística | 128.420 | 1,3% | 0,9% | +2,2% |
| Programas básicos | 61.012 | 0,6% | 0,9% | +9,0% |

- **Top-3 áreas = 67% das matrículas** (Negócios + Saúde + Educação).
- **Saúde e bem-estar é a história do período (+25%)**; **Engenharia é a única grande área em queda (−5,4%)**.
- **Computação/TIC chama atenção:** share de ingressantes (9,8%) maior que o de estoque (7,8%) — a área está **acelerando entrada**, crescendo 15,3% no período.

**Por que isso importa:** este é o mapa da **oferta de formação** que encontrará a demanda do CAGED. Saúde cresce 25% enquanto Engenharia recua — se o cruzamento CINE×CBO confirmar demanda por saúde em alta, o sistema está alinhado; se houver demanda por engenharia/produção, há **risco de gargalo de formação**. E TIC com entrada acelerada é o candidato natural a "onde o futuro da demanda profissional aponta" — o contraponto direto das admissões do CAGED.

---

# SEÇÃO 3: Detecção Robusta de Outliers

**Por que detectar outliers:** mesmo objetivo da EDA CAGED — distinguir **erro de dado** (corrigir), **evento real** (manter e explicar) e **artefato** (excluir de comparações). Nas duas variáveis a seguir, os extremos são o **próprio fenômeno** (concentração educacional e demográfica brasileira), não erro — e classificá-los como anomalia a remover seria destruir o sinal.

## 3.1 Método IQR — campo CINE (2024)

| Unidade | Q1 | Q3 | IQR | Limite superior | Outliers |
| --- | --- | --- | --- | --- | --- |
| Campo CINE (matrículas) | 452 | 15.716 | 15.264 | 38.612 | 47 (13,3%) |

Top extremos superiores: **Pedagogia** (887.502), **Direito** (652.996), **Administração** (652.934), **Enfermagem** (478.008), Sistemas de informação (420.280), Psicologia (375.574), Contabilidade (322.781), Educação física (303.816).

## 3.2 Método MAD — campo CINE (2024)

| Unidade | Mediana | MAD | Outliers (\|z_MAD\| > 2,5) |
| --- | --- | --- | --- |
| Campo CINE (matrículas) | 2.327 | 2.088 | 100 (28,3%) |

- **Divergência IQR (13,3%) × MAD (28,3%)** — em distribuição fortemente assimétrica, o MAD (centrado na mediana) flagra muito mais pontos. Ambos apontam os **mesmos** extremos no topo; a diferença é a cauda dos "pequenos". **Leitura:** não são 100 anomalias — é a cauda longa da log-normal (Seção 2.1). O correto é rodar os métodos sobre o log e interpretar os outliers como "campos gigantes", estrutura do mercado, não erro.

## 3.3 Outliers territoriais — UF (2024)

| Unidade | Mediana | MAD | Média | CV | Outliers IQR | Outliers MAD |
| --- | --- | --- | --- | --- | --- |
| UF (matrículas) | 196.696 | 115.949 | 378.692 | 125,3% | SP, MG, RJ | SP, MG, RJ, PR |

Participação no estoque nacional de matrículas (2024, top 8 UFs):

| UF | Share das matrículas 2024 | Leitura |
| --- | --- | --- |
| **São Paulo** | **23,9%** (2.441.033 matrículas) | outlier — IQR e MAD concordam |
| Minas Gerais | 9,3% (950.761) | 2º maior estoque |
| Rio de Janeiro | 9,2% (944.813) | grande estoque, mas conversão baixa (1,76 adm/matrícula — EDA unificada, Seção 4.3) |
| Paraná | 7,0% (711.466) | — |
| Rio Grande do Sul | 5,7% | — |
| Bahia | 4,9% | — |
| Santa Catarina | 4,5% (459.509) | estoque médio, mas conversão alta (3,64 adm/matrícula) |
| Ceará | 3,7% | — |

- **SP concentra 23,9%** das matrículas; top-5 (SP+MG+RJ+PR+RS) = **55,0%**; do 6º colocado em diante nenhuma UF passa de 5% — a cauda territorial é longa, como a de campos (Seção 2.1).
- **Por que isso importa:** a distribuição territorial é tão desigual quanto a de campos — e pelos mesmos motivos (população, renda, sede de IES). Para o modelo integrado CAGED×INEP, é um alerta de **estratificação obrigatória**: prever formação nacional e aplicar por UF introduziria viés grave em favor de SP; o pipeline UF já existe na gold (`fato_inep_educacao_uf_anual`, 27 UFs) e é a base correta para o join com o CAGED por UF.

---

# SEÇÃO 4: Relações Bivariadas

**Por que medir Pearson E Spearman:** mesma razão da EDA CAGED — Pearson captura relação linear e é sensível a extremos; Spearman captura relação monotônica qualquer. Com distribuição log-normal (Seção 2.1), **toda divergência Pearson < Spearman é sintoma de não-linearidade multiplicativa** — e aqui a regra empírica se confirmou.

Correlações entre indicadores educacionais por campo CINE (2024, n=353; oferta = presencial):

| Par | Pearson | p-value | Spearman | p-value | Leitura |
| --- | --- | --- | --- | --- | --- |
| Matrículas × Ingressantes | 0,9755 | <0,001 | 0,9818 | <0,001 | estoque e entrada andam juntos |
| Matrículas × Concluintes | 0,9838 | <0,001 | 0,9459 | <0,001 | campos grandes formam mais |
| Ingressantes × Concluintes | 0,9617 | <0,001 | 0,9196 | <0,001 | fluxo contínuo |
| Vagas × Inscritos | 0,8038 | <0,001 | **0,9553** | <0,001 | **divergência forte: log** |
| Vagas × Ingressantes | 0,9357 | <0,001 | **0,9747** | <0,001 | divergência: log |
| Inscritos × Ingressantes | 0,8940 | <0,001 | **0,9772** | <0,001 | divergência: log |

**Leitura e conclusões de negócio:**

- **Multicolinearidade estrutural (todas > 0,93):** matrículas, ingressantes e concluintes são quase a mesma variável em escalas diferentes — não entrar juntos em modelo linear. Na EDA CAGED o gêmeo disso era admissões × desligamentos (0,98); aqui a solução é a mesma: **escolher uma medida por conceito** (estoque: matrículas; fluxo: ingressantes) e derivar razões.
- **Vagas × Inscritos é o par mais informativo (Pearson 0,80 << Spearman 0,96):** a relação oferta×procura é **multiplicativa** — campos grandes recebem proporcionalmente mais inscritos. E é o par com menor correlação absoluta, ou seja, com **variância própria a explorar**: a razão inscritos/vaga (1,71 na média nacional) varia por campo e é exatamente a medida de **escassez relativa** que interessa ao cruzamento com demanda.
- **Divergência sistemática Pearson < Spearman nos pares com oferta:** confirmação independente da log-normalidade da Seção 2.1 — em escala log, espera-se que os pares convirjam.

---

# SEÇÃO 5: Evolução Temporal (4 pontos anuais)

**Adaptação metodológica:** com apenas 4 pontos (2021–2024), STL, ADF e ACF não têm poder estatístico — a seção correspondente da EDA CAGED é substituída por **evolução descritiva**. Recomendação registrada: quando o Censo 2025–2026 for ingerido, reavaliar métodos de série temporal.

## 5.1 Modalidade: a grande transição

| Ano | Ingressantes EaD | Share EaD ingressantes | Matrículas EaD | Share EaD matrículas |
| --- | --- | --- | --- | --- |
| 2021 | 2.476.016 | 62,8% | 3.713.646 | 41,3% |
| 2022 | 3.098.768 | 65,1% | 4.328.108 | 45,8% |
| 2023 | 3.312.696 | 66,3% | 4.910.499 | 49,2% |
| 2024 | 3.346.076 | **66,8%** | 5.186.811 | **50,7%** |

- Matrículas: presencial **−4,4%** (5,27 → 5,04 mi) vs EaD **+39,7%** (3,71 → 5,19 mi).
- Concluintes: presencial **−13,4%** (842 → 729 mil) vs EaD **+24,7%** (485 → 604 mil).

**Por que isso importa:** o share de ingressantes EaD (66,8%) muito acima do share de matrículas (50,7%) diz que a transição **acelera** — o fluxo de entrada já é majoritariamente digital, o estoque ainda não. Para o modelo de demanda profissional, os **concluintes que chegarão ao mercado de 2025 em diante são majoritariamente formados a distância**. Se a formação do EaD difere do presencial por ocupação, a oferta de mão de obra qualificada por área CINE mudará de composição antes de mudar de volume.

## 5.2 Oferta presencial em contração, conclusão relativa caindo

| Indicador | 2021 | 2024 | Variação |
| --- | --- | --- | --- |
| Vagas presenciais | 5.942.212 | 5.075.146 | −14,6% |
| Inscritos por vaga presencial | 1,45 | 1,71 | +18% |
| Ingressantes / vagas presenciais | 37,2% | 32,8% | −4,4 p.p. |
| Concluintes / ingressantes | 33,7% | 26,6% | −7,1 p.p. |

- **Concluintes/ingressantes com caveat de defasagem:** concluintes de 2024 majoritariamente ingressaram ~2020 (antes da base) — a queda de 33,7% → 26,6% reflete o boom de ingresso recente puxando o denominador, não necessariamente evasão crescente. Não interpretar como taxa de evasão.
- ⚠️ **Ingressantes/vagas presenciais = 32,8%** e caindo: a vaga ofertada presencial está **cada vez menos virando matrícula** — coerente com migração do aluno para o EaD.

**Por que isso importa:** juntando as duas tabelas — oferta presencial contraindo 14,6%, disputa por vaga subindo 18% e formação migrando para EaD — o sistema de formação superior brasileiro está em **reorganização de canal**, não em expansão uniforme. Para o cruzamento com a demanda CAGED, o volume total de concluintes (1,33 mi/ano) ainda é estável; **o que muda é onde e como essa formação acontece**.

---

# SEÇÃO 6: Features para o Modelo Integrado (INEP → CAGED)

**Por que construir features aqui:** o objetivo do MBA é prever a **demanda profissional** (admissões CAGED) usando a **formação** como sinal antecedente. Formação é a exógena estrutural de longo prazo do mercado de trabalho: concluintes de hoje são a oferta de mão de obra de 1–3 anos à frente. A EDA CAGED validou exógenas de curto prazo (desligamentos e salário, r ≈ 0,68–0,69 em t+1); a base INEP traz as de **longo prazo**.

**Features candidatas (todas defasadas, sem vazamento):**

| Feature | Fonte | Racional |
| --- | --- | --- |
| `concluintes_cine_lag1..3a` | gold Brasil/UF × CINE | oferta de mão de obra por área entrando no mercado com defasagem de formação |
| `ingressantes_cine_lag3..5a` | gold Brasil/UF × CINE | pipeline de formação — antecipa concluintes futuros |
| `share_ead_campo` | gold Brasil | composição EaD/presencial por área — proxy de custo e escala da formação |
| `inscritos_por_vaga` (presencial) | gold Brasil | escassez relativa de vagas por área — sinal de atratividade/pressão |
| `matriculas_cine_lag1a` | gold Brasil/UF | estoque de formação por área |

**Regras de integração com o CAGED:**

1. Chave de ponte: **CINE × CBO** — notebook `032_mapeamento_cine_cbo` + dimensões `gold.dim_cine_brasil` (372 rótulos) e `gold.dim_cbo_ocupacao` já existem no workspace
2. Defasagem mínima de 1 ano (formação → mercado) — testar lags de 1–3 anos no join com a série mensal CAGED
3. Estratificação por **UF** obrigatória (Seção 3.3: SP = 23,9% e outlier MAD) — usar `fato_inep_educacao_uf_anual` no mesmo nível do CAGED por UF
4. Trabalhar as medidas educacionais em **log** (Seção 2.1)

**Por que isso importa:** com o CAGED validando exógenas de curto prazo e o INEP fornecendo as de longo prazo, o modelo ganha os dois horizontes que explicam demanda: a **rotatividade do mês** (CAGED) e a **formação de ontem** (INEP). É a fechadura do argumento central do MBA — e a razão de as duas EDAs seguirem a mesma metodologia.

---

# SEÇÃO 7: Validação de Qualidade & Recomendações

## 7.1 Checklist

**1. Cobertura temporal**
- ✅ 4 Censos completos (2021–2024), sem parcialidade
- ✅ 27 UFs em todos os anos

**2. Integridade das chaves (validações do notebook 031)**
- ✅ Zero chaves duplicadas e zero nulas nas duas golds
- ✅ Diferenças silver×gold = 0 em todas as medidas e anos

**3. De-paras**
- ✅ CINE: totalmente decodificado (nomes embutidos + `dim_cine_brasil`)
- ✅ Modalidade: 1 = presencial, 2 = EaD (confirmado pelas colunas `*_presenciais`)
- ⚠️ **Sem de-para textual no pipeline** para `tipo_rede` (dicionário INEP: 1 = pública, 2 = privada), `tipo_grau_academico` (1 = bacharelado, 2 = licenciatura, 3 = tecnólogo) e `tipo_nivel_academico`. Referência 2024: rede privada ≈ 84% das matrículas; grau nulo em 61.446 matrículas (cursos sem grau aplicável)

**4. Riscos metodológicos mapeados**
- ⚠️ Oferta EaD nacional (dim 3, 18,6 mi de vagas) **fora da gold** — qualquer análise de oferta total deve buscá-la na silver
- ⚠️ Vagas/cursos/inscritos da gold = **presencial apenas** (filtro `nome_uf IS NOT NULL` exclui a dim 3)

## 7.2 Recomendações Finais

### Para o modelo integrado
1. **Criar o join CINE×CBO** (notebook 032) como tabela gold — é a ponte que falta entre as duas EDAs
2. **Features INEP defasadas 1–3 anos** como exógenas de longo prazo do modelo CAGED (Seção 6)
3. **Estratificar por UF×CINE** — ambas as golds já têm a granularidade
4. **Log-transformação** obrigatória nas medidas educacionais (log-normal, Seção 2.1)

### Para o pipeline
1. **Criar de-paras textuais** de `tipo_rede`/`tipo_grau_academico`/`tipo_nivel_academico` na silver
2. **Tabela gold da oferta EaD nacional** (dim 3) — hoje 18,6 mi de vagas invisíveis à gold
3. Ingerir o **Censo 2025** quando publicado para habilitar métodos de série temporal

---

# Conclusão

**Em uma frase de negócio:** a formação superior brasileira cresceu 13,8% em matrículas entre 2021 e 2024 movida pelo EaD (hoje 50,7% do estoque e 66,8% dos ingressantes), com oferta presencial contraindo 14,6% e disputa por vaga subindo — um sistema em reorganização de canal, concentrado em Negócios+Saúde+Educação (67% das matrículas), com Saúde em alta (+25%), Engenharia em queda (−5,4%) e TIC acelerando entrada.

Esta EDA, gêmea metodológica da EDA CAGED, revelou:

- ✅ **Base íntegra e validada** (4 censos, 27 UFs, diferenças silver×gold = 0)
- ✅ **Distribuição log-normal por campo CINE** — mediana/quartis e log obrigatórios (contraparte do "2026S2 parcial" no CAGED: identificar o artefato antes de interpretar)
- ✅ **Concentração estrutural** — top-3 áreas = 67%; SP = 23,9% (outlier em IQR e MAD)
- ✅ **Multicolinearidade** entre medidas educacionais (0,93–0,98) — escolher uma por conceito
- ⚠️ **Oferta EaD invisível na gold** — 18,6 mi de vagas só na silver (dim 3)
- ✅ **Features de longo prazo** prontas para o join CINE×CBO com o modelo de demanda

### Próximas etapas

1. **Join CINE×CBO** em gold (notebook 032) — a ponte das duas EDAs
2. **Modelo integrado**: série mensal CAGED + exógenas curtas (desligamentos, salário) + exógenas longas (concluintes/ingressantes CINE defasados)
3. De-paras textuais na silver + gold da oferta EaD nacional
4. Ingerir Censo 2025 e reavaliar métodos de série temporal

---

# Apêndice: Artefatos

| Artefato | Caminho |
| --- | --- |
| Gold nacional | `workspace.gold.fato_inep_educacao_brasil_anual` (v2) |
| Gold por UF | `workspace.gold.fato_inep_educacao_uf_anual` (v2) |
| Silver granular | `workspace.silver.inep_superior_cursos` (2,41 mi linhas) |
| Dimensão CINE | `workspace.gold.dim_cine_brasil` (372 rótulos) |
| Notebook gold v2 | `notebooks/03_analytics/031_silver_to_gold_inep` |
| Notebook análise dims | `notebooks/03_analytics/0311_silver_to_gold_inep_analise` |
| Ponte CINE×CBO | `notebooks/03_analytics/032_mapeamento_cine_cbo` |
| EDA CAGED (contraparte) | `EDA_caged.md` (mesma pasta) |

**Notas técnicas da geração deste relatório:**

- Todos os números provêm de queries executadas em 2026-10-30 contra a gold v2 (gravada 29/10) e a silver.
- "Vagas/inscritos/cursos" referem-se sempre à **oferta presencial** (dim 1); oferta EaD nacional (dim 3) indicada explicitamente quando citada.
- Correlações calculadas sobre os 353 campos CINE de 2024 (Pearson e Spearman, scipy); normalidade por Shapiro-Wilk bruto e log.

**EDA concluída em 2026-10-30** · Autora: Fernanda Carnevalle de Melo
