# EDA Unificada: Formação (INEP) × Demanda Profissional (CAGED)
## Análise Exploratória segundo Bussab & Moretin (2010) — integração das duas bases do MBA

**Autora:** Fernanda Carnevalle de Melo  
**Data:** 2026-10-30 · **Base:** Censo da Educação Superior INEP (2021–2024, anual/censitário) × Novo CAGED (2021–01 a 2026–08, mensal, anos 2021–2025 completos)  
**Tabelas:** `workspace.gold.fato_inep_educacao_brasil_anual` + `fato_inep_educacao_uf_anual` (v2) × `workspace.silver.novo_caged_movimentacoes` + `workspace.gold.fato_caged_semestral`  
**Objetivo:** fechar o ciclo analítico do MBA — validar, com coerência temporal total, as **features de formação (INEP)** que entram no modelo preditivo de **demanda profissional (CAGED)**, com justificativa bibliográfica consolidada para cada escolha.

---

## O Princípio da Coerência Temporal (mês↔mês, semestre↔semestre, ano↔ano)

Comparar grandezas de granularidades diferentes é o erro clássico que essa EDA elimina. As duas bases têm naturezas temporais distintas — o CAGED é **fluxo mensal declaratório** (toda movimentação vira registro) e o INEP é **censo anual** (fotografia do ano letivo). O alinhamento obedece a uma regra única:

> **Toda comparação entre as duas bases acontece no nível ANO. Mês e semestre são granularidades internas do CAGED, usadas para decompor (mês→semestre→ano). Nunca dividir o INEP ao meio, nunca comparar mês com ano.**

| Granularidade | Onde vive | Uso nesta EDA |
| --- | --- | --- |
| Mês | CAGED (68 meses) | decomposição interna: sazonalidade, share de janeiro, vales de dezembro |
| Semestre | CAGED (11 completos + 1 parcial) | agregação interna: S1+S2 = ano; contraprova 2026S2 aplicada |
| **Ano** | **CAGED × INEP** | **a única granularidade de cruzamento entre as bases (2021–2024)** |
| UF × Ano | ambas (27 UFs) | cross-sectional unificado (n=108) — a análise com poder estatístico real |

**Defasagem estrutural formação→mercado:** concluintes do Censo do ano Y-1 chegam ao mercado de trabalho a partir de janeiro de Y. Toda feature INEP entra no modelo com **lag mínimo de 1 ano** — nunca simultânea (risco de vazamento temporal, Seção 6).

---

## Metodologia

Esta EDA unifica as duas EDAs individuais (EDA_caged.md e EDA_Inep.md, mesmas pasta e metodologia) sob os princípios de **Bussab & Moretin (2010)**:

1. **Coerência temporal primeiro** — alinhamento mês→semestre→ano antes de qualquer cruzamento
2. **Painel anual pareado** — comparação ano com ano (2021–2024, janela comum às duas bases)
3. **Cross-sectional UF×ano** — onde n=108 dá poder às correlações (Pearson e Spearman, com e sem log)
4. **Razões contra efeito-tamanho** — correlações altas em cross-sectional refletem escala; o sinal está nas razões
5. **Feature engineering com justificativa bibliográfica** — cada feature citada com a literatura que a sustenta
6. **Validação e riscos** — o que o desenho não pode afirmar, fica escrito

---

# SEÇÃO 1: Painel Anual Pareado (ano com ano, 2021–2024)

## 1.1 As duas bases lado a lado

| Ano | CAGED: Admissões | CAGED: Desligam. | CAGED: Saldo | CAGED: Salário med. | INEP: Ingressantes | INEP: Matrículas | INEP: Concluintes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 19.703.604 | 16.851.191 | 2.852.413 | R$ 1.400 | 3.943.733 | 8.984.396 | 1.326.961 |
| 2022 | 22.243.441 | 20.232.075 | 2.011.366 | R$ 1.500 | 4.755.158 | 9.441.290 | 1.287.136 |
| 2023 | 22.982.161 | 21.503.821 | 1.478.340 | R$ 1.628 | 4.992.486 | 9.974.435 | 1.374.287 |
| 2024 | 25.336.277 | 23.659.763 | 1.676.514 | R$ 1.744 | 5.009.116 | 10.224.686 | 1.333.515 |

*(2025 CAGED completo: 26.321.557 adm / 25.064.560 desl / saldo 1.256.997 / salário R$ 1.854,60 — exibido à parte porque o INEP 2025 ainda não existe; ele entra no painel quando o Censo for publicado.)*

## 1.2 Indicadores derivados do pareamento

| Indicador | 2021 | 2022 | 2023 | 2024 | Leitura |
| --- | --- | --- | --- | --- | --- |
| Admissões CAGED (Y) / Concluintes INEP (Y−1) | — | 16,76 | 17,86 | 18,44 | cada formado "sustenta" ~17–18 admissões no ano seguinte — a demanda gira muito além da formação |
| Admissões / Desligamentos | 1,169 | 1,099 | 1,069 | 1,071 | criação líquida desacelerando; rotatividade (giro) acelerando |
| Saldo anual CAGED | 2.852.413 | 2.011.366 | 1.478.340 | 1.676.514 | absorção líquida caindo enquanto ingresso INEP sobe +27% |
| Salário mediano CAGED | R$ 1.400 | R$ 1.500 | R$ 1.628 | R$ 1.744 | +24,6% no período — o preço do trabalho sobe |

**Por que isso importa (leitura de negócio unificada):** o sistema mostra **tensão de absorção** — a formação acelera (ingressantes +27%, matrículas +13,8%) enquanto a criação líquida de vagas cai (saldo −41% de 2021 a 2024) e a razão admissão/formado sobe (16,8 → 18,4). A rotatividade (Davis, Haltiwanger & Schuh, 1996: mercados giram muito mais do que criam) é o elo: as vagas não somem, elas **circulam** — e é exatamente por isso que o modelo precisa das duas famílias de features (curto prazo = giro; longo prazo = formação).

---

# SEÇÃO 2: Semestre com Semestre (agregação interna do CAGED)

O INEP é anual por natureza (Censo) — **não existe semestre INEP** e dividir o Censo ao meio seria fabricar dado. A coerência aqui é dupla: (i) internamente, comparar semestre com semestre do CAGED; (ii) na ponte com o INEP, **S1 + S2 = ano do Censo**, sem exceção.

| Ano | S1 (admissões) | S2 (admissões) | S1+S2 (= ano Censo) | S2/S1 |
| --- | --- | --- | --- | --- |
| 2021 | 9.456.760 | 10.246.844 | 19.703.604 | 1,08 |
| 2022 | 11.458.253 | 10.785.188 | 22.243.441 | 0,94 |
| 2023 | 11.772.099 | 11.210.062 | 22.982.161 | 0,95 |
| 2024 | 13.027.721 | 12.308.556 | 25.336.277 | 0,95 |

- **Padrão estável 2022–2024: S2 ≈ 0,95 × S1** — o vale de dezembro (Seção 3) derruba o 2º semestre de forma sistemática. 2021 é a exceção (recomposição pós-pico da pandemia).
- Os semestres somam **exatamente** ao anual do painel da Seção 1 — a verificação de coerência (mês→semestre→ano) foi fechada com diferença zero.
- A contraprova da EDA CAGED segue valendo: **2026S2 é parcial (jul–ago)** e não deve entrar em comparação semestral.

**Por que isso importa:** o modelo mensal CAGED não pode ser validado somando meses em qualquer janela — a sazonalidade (vale de dezembro, pico de fev–mar) quebra qualquer agregação ingênua. Agregar sempre em jan–dez ou fev–jan *após* diferenciar, nunca em janelas soltas (Hyndman & Athanasopoulos, 2018, cap. sobre agregação temporal).

---

# SEÇÃO 3: Mês com Mês (decomposição interna do CAGED + calendário de formação)

O detalhe mensal existe só no CAGED — mas é ele que revela **quando a formação encontrada no ano do Censo chega ao mercado**:

| Ano | Admissões de janeiro | Share de janeiro nas admissões do ano |
| --- | --- | --- |
| 2021 | 1.550.075 | 7,87% |
| 2022 | 1.777.646 | 7,99% |
| 2023 | 1.874.226 | 8,16% |
| 2024 | 2.067.817 | 8,16% |
| 2025 | 2.271.611 | **8,63%** |

- **O share de janeiro sobe sistematicamente** (7,87% → 8,63%) — coerente com a hipótese de calendário de formação: os concluintes do Censo (colação concentrada em dezembro) entram no mercado no raiar do ano seguinte. O Censo não tem mês, mas o CAGED mostra a assinatura mensal da entrada dos formandos.
- Vale de **dezembro** em todos os anos (saldos negativos 2021–2025) e picos em **fev–mar** — a sazonalidade dominante já identificada na EDA CAGED (STL) e que obriga dummies/harmônicos no modelo.

**Por que isso importa:** é a validação empírica da **defasagem 1-ano** usada nas features INEP: o ano letivo termina, o formando cola grau em dez, e o CAGED registra o pico de entrada em jan–mar seguinte. Miron (1996) trata sazonalidade como estrutura econômica real (não ruído a remover) — aqui ela é o próprio canal de transmissão formação→mercado. No modelo mensal: features INEP anuais entram **em janeiro** (ou espalhadas com peso sazonal), nunca em dezembro.

---

# SEÇÃO 4: Cross-Sectional UF × Ano — a análise unificada com poder estatístico

Com só 4 anos, correlações ano a ano têm n=4 (sem valor inferencial). A solução metodológica é o **painel UF×ano**: 27 UFs × 4 anos = **108 observações pareadas** (mesma UF, mesmo ano, nas duas bases).

## 4.1 Correlações (n=108)

| Par (UF×ano) | Pearson | p-value | Spearman | p-value |
| --- | --- | --- | --- | --- |
| CAGED admissões × INEP matrículas (mesmo ano) | 0,9782 | 3e-74 | 0,9528 | 1e-56 |
| CAGED admissões × INEP ingressantes (mesmo ano) | 0,9865 | 4e-85 | 0,9710 | 1e-67 |
| CAGED admissões × INEP concluintes (mesmo ano) | 0,9821 | 1e-78 | 0,9533 | 6e-57 |
| **CAGED admissões (Y) × INEP concluintes (Y−1)** | **0,9878** | **1e-65** | 0,9594 | 4e-45 |
| CAGED desligamentos (Y) × INEP concluintes (Y−1) | 0,9857 | 8e-63 | 0,9554 | 1e-43 |
| log(admissões) × log(matrículas) | 0,9659 | 5e-64 | — | — |

## 4.2 Estabilidade ano a ano (coerência verificada)

| Ano (n=27 por ano) | Pearson r (adm × matrículas) | Spearman ρ |
| --- | --- | --- |
| 2021 | 0,9790 | 0,9585 |
| 2022 | 0,9793 | 0,9585 |
| 2023 | 0,9791 | 0,9499 |
| 2024 | 0,9791 | 0,9469 |

A relação é **estável em todos os 4 anos** (r ≈ 0,979) — a coerência ano com ano não é acidente de um ano, é estrutura.

## 4.3 O caveat do efeito-tamanho — e onde está o sinal real

⚠️ **r ≈ 0,98 em cross-sectional de UF é dominado por escala:** SP é grande em tudo (população, IES, vagas, contratações), então "quem é grande em formação é grande em demanda" é quase tautológico (o mesmo problema da multicolinearidade de escala da Seção 2.1 da EDA INEP). O que essa correlação **valida** não é que formação causa demanda — é que as duas bases **medem o mesmo tecido econômico de forma coerente e estável**, o que autoriza o join.

**O sinal informacional está na razão** (admissões CAGED / matrículas INEP, 2024):

| UF | Admissões 2024 | Matrículas INEP 2024 | Adm por matrícula |
| --- | --- | --- | --- |
| SC | 1.672.889 | 459.509 | **3,64** |
| SP | 8.016.921 | 2.441.033 | **3,28** |
| MG | 2.763.831 | 950.761 | 2,91 |
| PR | 1.977.453 | 711.466 | 2,78 |
| RJ | 1.664.481 | 944.813 | **1,76** |
| Brasil | 25.336.277 | 10.224.686 | 2,47 |

Estados com a **mesma escala relativa de formação geram demandas muito diferentes**: SC converte 3,64 admissões por matrícula e RJ apenas 1,76 — razão de 2×. Esse **resíduo** (economia dinâmica vs. economia estagnada, mercado formal vs. informal, setores) é exatamente o que o modelo deve capturar com as demais features — e o que a razão adm/matrícula **como feature composta** traz ao modelo além do tamanho.

**Por que isso importa:** metodologicamente, é a aplicação direta de Bussab & Moretin (2010) sobre correlação e de Wooldridge (2010) sobre o perigo de regressões dominadas por escala: correlação alta valida **consistência**, não **explicação**. Para o ML, a consequência prática são três regras: (i) features em **log**; (ii) features de razão (adm/matrícula, adm/concluinte) como compostas; (iii) validação com **janela expansiva** (Tashman, 2000) por UF — nunca embaralhada.

---

# SEÇÃO 5: Ocupação × Formação (CBO × CINE) — o estágio atual da ponte

O cruzamento ocupacional (demanda por CBO × formação por campo CINE) é a análise final da integração. O workspace já tem a infraestrutura (notebook `032_mapeamento_cine_cbo`):

| Componente | Status |
| --- | --- |
| `gold.dim_cine_brasil` | ✅ 372 rótulos CINE, hierarquia em 3 níveis, nomenclatura da edição mais recente |
| `gold.dim_cbo_ocupacao` | ✅ 2.778 códigos CBO 2002 (6 dígitos, validados) |
| Cobertura CBO na gold do CAGED | ✅ 2.727 CBOs; **41 sem cobertura na dimensão** (documentados, não excluídos); 0 divergências de descrição |
| **Crosswalk CINE→CBO** | ⚠️ **pendente** — o mapeamento semântico (qual campo forma para qual ocupação) ainda não foi materializado como tabela gold |

**Por que isso importa:** o crosswalk é o que transforma as features agregadas (Brasil/UF) em features **por ocupação** — permitindo, por exemplo, antecipar demanda por enfermeiros a partir de concluintes de Enfermagem. A literatura de mismatch (Quintini, 2011, OECD) mostra que a qualidade do match formação-ocupação é o determinante central de produtividade e absorção — o crosswalk é, literalmente, a formalização do conceito. Enquanto o crosswalk não existe, as features INEP entram no modelo no **nível UF e área CINE geral** (já validado nesta EDA), e o nível ocupacional é a evolução natural.

## 5.1 Retratos Ocupacionais de 2024 — a ponte CBO×CINE antecipada em números

Mesmo com o crosswalk formal pendente, os códigos de ocupação do CAGED (família CBO, 4 dígitos) já permitem **retratos manuais campo×ocupação** — três casos de 2024 que antecipam o valor da ponte:

| Retrato | Formandos INEP 2024 | Contratações CAGED 2024 | Desligamentos 2024 | Conversão (contrat./formandos) |
| --- | --- | --- | --- | --- |
| Enfermagem → CBO 223 (saúde nível superior) | 54,5 mil | 208,9 mil | 184,7 mil | **3,8×** |
| Pedagogia → CBO 231–232 (professores) | 103,4 mil | 145,4 mil | 142,6 mil | 1,4× |
| Sistemas de Informação → CBO 212 (TIC) | 61,8 mil | 139,6 mil | 125,7 mil | 2,3× |

Para referência, os **5 maiores campos de concluintes em 2024**: Pedagogia (103,4 mil), Direito (98,3 mil), Administração (76,9 mil), Sistemas de Informação (61,8 mil) e Enfermagem (54,5 mil) — os retratos abaixo cobrem o 1º, o 4º e o 5º.

**Como ler os retratos:**

- **O formado novo é minoria do volume:** nos três retratos, os formandos do ano equivalem a ~20–40% das contratações do grupo — o mercado absorve os concluintes, mas **gira muito mais do que forma** (a mesma lei da Seção 1.2: 18,4 admissões por formado no agregado).
- **Rotatividade também nos grupos qualificados:** saúde superior desliga 184,7 mil (88% das contratações); professores praticamente empatam (142,6 mil desligamentos vs 145,4 mil contratações) — o "mercado de reposição" da Seção 1.2, agora visível por ocupação.
- **As conversões ordenam a pressão de demanda:** saúde 3,8×, TIC 2,3× e pedagogia 1,4× — quanto maior a razão, mais o grupo depende de mão de obra que não vem da graduação recente (requalificação, técnico, reposição de alto giro).

**Salário mediano de admissão por grupo (2024)** — o prêmio de qualificação:

| Grupo ocupacional | Salário mediano de contratação | vs. mercado formal |
| --- | --- | --- |
| TIC nível superior (CBO 212) | **R$ 5.200** | **3,0×** |
| Saúde nível superior (CBO 223) | R$ 3.950 | 2,3× |
| Advogados (CBO 241) | R$ 3.700 | 2,1× |
| Professores (CBO 231–232) | R$ 2.109 | 1,2× |
| Mercado formal (todas as contratações) | R$ 1.741 | 1,0× |

**Grupos CBO com maior saldo líquido de 2024** (admissões − desligamentos, em milhões):

| Grupo CBO | Admissões | Desligamentos | Saldo líquido |
| --- | --- | --- | --- |
| Varejo (521) | 3,05 mi | 2,83 mi | +0,22 mi |
| Limpeza (514) | 1,85 mi | 1,64 mi | +0,21 mi |
| Escritório (411) | 1,70 mi | 1,51 mi | +0,19 mi |
| Alimentação (513) | 1,60 mi | 1,48 mi | +0,12 mi |
| Produção (784) | 1,48 mi | 1,22 mi | **+0,26 mi** |

**Descobertas e caveats metodológicos do retrato TIC (CBO 212):**

- TIC contratou 139,6 mil em 2024 — porém **−25% desde o pico de 2021** (≈187 mil): a demanda qualificada cresce menos que o total do mercado.
- O **salário 3× o mercado** (R$ 5.200 vs R$ 1.741) combinado com queda de volume é a assinatura clássica de **escassez + seletividade**: as vagas que restam são as mais caras.
- ⚠️ **CBO 213 (técnicos de TIC) ≠ programadores** — as famílias CBO não mapeiam 1:1 para profissões de nicho; usar a família 212 como proxy de "programadores" subestima e distorce. Descoberta registrada como alerta de desenho para o crosswalk formal.
- ⚠️ **Advogados (CBO 241): saldo negativo** — 23,2 mil contratações × 24,8 mil desligamentos em 2024. Direito forma 98,3 mil por ano (2º maior campo de concluintes) num mercado que **encolhe** — o mismatch formação×demanda em estado puro.

**Por que isso importa:** estes números são a prova de conceito do crosswalk: com apenas três pares mapeados à mão, já se vê **onde a formação encontra demanda (saúde 3,8×, TIC 2,3×) e onde ela a excede (direito, saldo negativo)** — a diferença entre os dois é a literatura de mismatch (Quintini, 2011) materializada em números brasileiros. Para o modelo: as features `concluintes_cine_lag` (Seção 6.2) ganharão poder preditivo adicional quando puderem entrar **por ocupação**, não só por UF × área CINE geral.

---

# SEÇÃO 6: O Conjunto Final de Features para o ML — e por quê (bibliografia)

Este é o entregável central da EDA unificada: o **feature set do modelo de demanda profissional** (alvo: admissões CAGED mensais), cada feature com a evidência desta EDA e a literatura consolidada que a sustenta.

## 6.1 Features de curto prazo — CAGED (validadas na EDA CAGED)

| Feature | Defasagem | Evidência nesta EDA | Fundamentação bibliográfica |
| --- | --- | --- | --- |
| `adm_lag_1m, 3m, 6m, 12m` + médias móveis 3m/12m | t−1 a t−12 | ACF decai gradualmente; lag-12 carrega o calendário (STL) | **Box & Jenkins (1970)**: processos autororregressivos capturam a memória da série; **Hyndman & Athanasopoulos (2018)**: lags e janelas móveis são o vocabulário padrão de previsão univariada |
| `desl_lag_1m` (rotatividade) | t−1 | r = 0,69 com adm em t+1; adm×desl = 0,98 (não usar juntas) | **Davis, Haltiwanger & Schuh (1996)**: fluxos brutos de criação e destruição de vagas são simultâneos e cointensos — a destruição de ontem antecede a criação de amanhã; **Mortensen & Pissarides (1994)**: na teoria da busca, desligar e contratar são faces do mesmo processo de realocação |
| `salario_lag_1m` (mediana de admissão) | t−1 | r = 0,68 com adm em t+1; +24,6% no período | **Hamermesh (1993)**: a demanda por trabalho é função do seu preço — salário de contratação em alta sinaliza escassez de mão de obra e antecipa movimentação |
| `saldo_lag_1m` (ciclo) | t−1 | r = −0,37 em t+1 (correção cíclica) | **Granger (1969)**: precedência temporal com sinal negativo indica correção — saldo alto hoje antecede desaceleração; a interpretação é de ciclo, não tendência |
| `mes_sin, mes_cos` (harmônicos) + dummies | t | Vale de dez, pico fev–mar todos os anos | **Miron (1996)**: sazonalidade é estrutura econômica previsível, não ruído — deve entrar no modelo explicitamente, não ser amortecida |

## 6.2 Features de longo prazo — INEP (validadas nesta EDA unificada)

| Feature | Defasagem | Evidência nesta EDA | Fundamentação bibliográfica |
| --- | --- | --- | --- |
| `concluintes_cine_lag1..3a` (por UF × área CINE) | Y−1 a Y−3 | **r = 0,9878** com adm em Y (UF×ano, n=108); share de janeiro subindo (7,9%→8,6%) | **Becker (1964)**: concluintes são o fluxo que renova o estoque de capital humano — a oferta qualificada de mão de obra de 1–3 anos à frente; **Mincer (1974)**: a produtividade associada à escolaridade se materializa no mercado ao concluir, não ao ingressar |
| `matriculas_cine_lag1a` (estoque) | Y−1 | r = 0,978 (mesmo ano); razão adm/matrícula varia 1,76–3,64 por UF | **Becker (1964)**: o estoque de matriculados é capital humano em formação — antecipa concluintes futuros e dimensiona a pressão de oferta no horizonte de 2–4 anos |
| `ingressantes_cine_lag3..5a` (pipeline) | Y−3 a Y−5 | r = 0,9865 (mesmo ano) — mas uso com lag longo | Pipeline de formação: sinal de longo prazo da oferta futura de mão de obra, defasado pela duração típica do curso (3–5 anos) |
| `share_ead_uf` (composição de canal) | Y−1 | EaD = 50,7% do estoque, 66,8% dos ingressantes (2024) | Transição de canal: EaD muda o custo e a escala da formação — proxy estrutural de como e onde a mão de obra será formada (evidência documentada na EDA INEP, Seção 5.1) |
| `adm_por_matricula` (razão composta CAGED×INEP) | t−1 (compõe ano anterior) | SC 3,64 vs RJ 1,76 — resíduo com 2× de amplitude | **Wooldridge (2010)**: razões neutralizam efeito-tamanho e expõem a dinâmica relativa — estados com mesma formação geram demandas distintas; a feature captura a eficiência de conversão formação→demanda do território |
| `inscritos_por_vaga` (escassez, presencial) | Y−1 | 1,45 → 1,71 (+18% de disputa) | Escassez relativa de vagas por área: pressão de demanda reprimida que antecipa movimentação de procura (microeconomia da educação — sinal de preço da escassez) |

## 6.3 Regras de modelagem (transversais a todas as features)

| Regra | Justificativa | Fonte |
| --- | --- | --- |
| **Log-transformação** nas medidas de volume (ambas as bases) | Distribuições log-normal (INEP: CV 304,9%) e heterocedasticidade por escala — log estabiliza variância e lineariza relações multiplicativas | Bussab & Moretin (2010); Wooldridge (2010) |
| **Uma medida por conceito** (sem adm+desl juntos; sem ingressantes+matrículas+concluintes juntos) | Multicolinearidade: 0,98 (CAGED) e 0,93–0,98 (INEP) — coeficientes instáveis e sinais invertidos | Belsley, Kuh & Welsch (1980); Wooldridge (2010) |
| **Sem vazamento**: features INEP sempre com lag ≥ 1 ano; features CAGED só defasadas | Dado do futuro no treino infla métrica e quebra em produção | Kaufman et al. (2012); Hyndman & Athanasopoulos (2018) |
| **Validação temporal por janela expansiva** (não embaralhada), erro reportado por estação do ano | Série com tendência+sazonalidade exige avaliação out-of-sample na ordem do tempo | Tashman (2000); Hyndman & Athanasopoulos (2018) |
| **Estratificação por UF** (não só Brasil) | SP = 23,9% (INEP) e outlier IQR/MAD (CAGED); razões variam 1,76–3,64 | Evidência das duas EDAs (Seção 4.3 desta EDA) |
| **Correlação = precedência, não causalidade** | Granger (1969): defasagem temporal valida antecedência preditiva, não mecanismo causal — linguagem do relatório e da defesa deve ser precisa | Granger (1969) |

**Por que esse conjunto fecha o argumento do MBA:** o modelo prevê **demanda** com features dos dois lados do mercado de trabalho — o **giro** (curto prazo: rotatividade, salário, sazonalidade — Davis & Haltiwanger; Mortensen & Pissarides; Hamermesh; Miron) e a **formação** (longo prazo: capital humano defasado — Becker; Mincer). Nenhuma feature entra sem evidência empírica nesta EDA e sem base em literatura consolidada.

---

# SEÇÃO 7: Validação, Limites e Riscos

## 7.1 O que esta EDA pode afirmar

- ✅ Coerência temporal total: mês→semestre→ano fecham com diferença zero no CAGED; cruzamento INEP×CAGED só no nível ano
- ✅ As duas bases medem o mesmo tecido econômico de forma **estável** (r ≈ 0,979 em todos os anos, UF×ano)
- ✅ A defasagem 1-ano formação→mercado tem assinatura mensal (share de janeiro subindo) e suporte cross-sectional (concluintes Y−1 é o par de maior correlação, 0,9878)
- ✅ O feature set da Seção 6 é completo, sem vazamento e justificado por literatura

## 7.2 O que esta EDA NÃO pode afirmar (limites)

- ⚠️ **n=4 anos** impede inferência temporal entre as bases (correlações ano a ano não têm valor de teste) — o cross-sectional UF×ano é a única via com poder, e ainda assim sofre efeito-tamanho
- ⚠️ r ≈ 0,98 em UF×ano é **consistência de escala**, não causalidade formação→demanda (Seção 4.3)
- ⚠️ Oferta EaD nacional (18,6 mi de vagas, dim 3 do INEP) fora da gold — invisível ao feature set atual
- ⚠️ Crosswalk CINE×CBO pendente — features ocupacionais (por CBO) ainda não são possíveis; a camada atual é UF × área CINE geral
- ⚠️ 2026S2 CAGED é semestre parcial (jul–ago) — excluído de toda comparação semestral nesta EDA

## 7.3 Próximas etapas

1. **Materializar o crosswalk CINE→CBO** em gold (extensão do notebook 032) — destrava features por ocupação
2. **Modelo integrado**: SARIMA/log + dummies como baseline; challenger com features da Seção 6; seleção por MAE/MAPE com janela expansiva por UF
3. **Feature composta adm/matrícula por UF×CINE** como primeiro teste do resíduo de conversão
4. Ingerir Censo 2025 (quando publicado) e reexecutar esta EDA unificada com n=5

## 7.4 Escopo oficial do modelo, stack e métricas de avaliação

**Escopo de previsão (fechado com a orientação do projeto):** prever **admissões mensais** no grão **UF × grupo ocupacional (CBO)** — 27 UFs × 4 grupos = **108 séries mensais** a previsar, com **defasagem mínima de 1 ano** nas features INEP (regra da Seção 6.3) e **validação temporal por janela expansiva** (Tashman, 2000), nunca embaralhada. Baseline: **SARIMA/log + dummies sazonais** (Statsmodels); challengers: **LightGBM** com as features da Seção 6 e **Prophet** para sazonalidade múltipla — experimentos versionados e rastreados no **MLflow**.

**Métricas de avaliação:**

| Métrica | O que mede | Por que entra |
| --- | --- | --- |
| **MAE** | erro médio absoluto, na unidade do alvo (admissões) | direto para o negócio: "erro típico de ±X contratações" |
| **MAPE** | erro percentual médio | comparável entre séries de escalas diferentes (UFs e grupos heterogêneos) |
| **RMSE** | erro quadrático médio | penaliza grandes erros — no grão mensal, um mês catastrófico pesa mais que muitos erros pequenos |

**Métricas descartadas (e por quê):**

| Métrica | Por que ficou de fora |
| --- | --- |
| R² | com tendência forte, qualquer modelo ingênuo "explica" 90%+ — infla a avaliação sem informar qualidade de previsão |
| Acurácia direcional / hit rate | binariza o problema (acertou a direção?) e esconde a magnitude do erro |
| MSE | unidade quadrada (admissões²) sem leitura de negócio — o RMSE cobre o mesmo papel de forma interpretável |

**Por que isso importa:** métrica mal escolhida escolhe o modelo errado — otimizar R² premia o ingênuo que segue a tendência; otimizar hit rate premia o tímido que nunca erra grande mas também nunca antecipa. O trio MAE/MAPE/RMSE força o modelo a ser **bom no tamanho do erro, comparável entre UFs e responsivo a meses ruins** — exatamente o que uma decisão de capacidade de contratação exige (Hyndman & Athanasopoulos, 2018, cap. 3).

---

# Conclusão

**Em uma frase de negócio:** entre 2021 e 2024, a formação superior cresceu 13,8% (impulsionada pelo EaD, hoje 66,8% dos ingressantes) enquanto a criação líquida de vagas formais caía 41% — um mercado que gira 17–18 admissões por formado e absorve os concluintes com assinatura visível no janeiro do CAGED (share 7,9%→8,6%); as duas bases são coerentes e estáveis entre si (r ≈ 0,98 em todos os anos, UF×ano), e a razão admissões/matrícula — de 1,76 no RJ a 3,64 em SC — é onde mora o sinal que o modelo deve aprender.

A EDA unificada entregou:

- ✅ **Regra de coerência temporal** explícita (mês↔semestre internos do CAGED; ano como única ponte INEP×CAGED)
- ✅ **Painel anual pareado** com indicadores de absorção (adm/concluinte, saldo, salário)
- ✅ **Validação cross-sectional** (n=108) com estabilidade ano a ano e caveat de efeito-tamanho
- ✅ **Assinatura mensal da defasagem formação→mercado** (janeiro)
- ✅ **Feature set final para o ML** — 11 features em 2 horizontes, cada uma com evidência empírica e fundamentação bibliográfica (Becker, Mincer, Davis & Haltiwanger, Mortensen & Pissarides, Hamermesh, Miron, Granger)
- ✅ **Limites declarados** — n=4, efeito-tamanho, crosswalk pendente

---

# Referências Bibliográficas

- Becker, G. S. (1964). *Human Capital: A Theoretical and Empirical Analysis*. New York: Columbia University Press for NBER.
- Belsley, D. A., Kuh, E., & Welsch, R. E. (1980). *Regression Diagnostics: Identifying Influential Data and Sources of Collinearity*. New York: Wiley.
- Box, G. E. P., & Jenkins, G. M. (1970). *Time Series Analysis: Forecasting and Control*. San Francisco: Holden-Day.
- Bussab, W. O., & Moretin, P. A. (2010). *Estatística Básica* (6ª ed.). São Paulo: Saraiva.
- Davis, S. J., Haltiwanger, R., & Schuh, S. (1996). *Job Creation and Destruction*. Cambridge, MA: MIT Press.
- Granger, C. W. J. (1969). "Investigating causal relations by econometric models and cross-spectral methods." *Econometrica*, 37(3), 424–438.
- Hamermesh, D. S. (1993). *Labor Demand*. Princeton, NJ: Princeton University Press.
- Hyndman, R. J., & Athanasopoulos, G. (2018). *Forecasting: Principles and Practice* (2ª ed.). Melbourne: OTexts.
- INEP (2024). *Dicionário de Dados do Censo da Educação Superior*. Brasília: Microdados.
- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). "Leakage in data mining: Formulation, detection, and avoidance." *ACM Transactions on Knowledge Discovery from Data*, 6(4), 1–21.
- Mincer, J. (1974). *Schooling, Experience, and Earnings*. New York: NBER.
- Miron, J. A. (1996). *The Economics of Seasonal Cycles*. Cambridge, MA: MIT Press.
- Mortensen, D. T., & Pissarides, C. A. (1994). "Job creation and job destruction in the theory of unemployment." *The Review of Economic Studies*, 61(3), 397–415.
- Quintini, G. (2011). *Over-qualified or Under-skilled: A Review of Existing Literature*. OECD Social, Employment and Migration Working Papers, nº 121. Paris: OECD.
- Rousseeuw, P. J., & Hubert, M. (2011). "Robust statistics for outlier detection." *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery*, 1(1), 73–79.
- Tashman, L. J. (2000). "Out-of-sample tests of forecasting accuracy: An analysis and review." *International Journal of Forecasting*, 16(4), 437–450.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Reading, MA: Addison-Wesley.
- Wooldridge, J. M. (2010). *Introductory Econometrics: A Modern Approach* (4ª ed.). Mason, OH: South-Western Cengage Learning.

---

# Apêndice: Artefatos e Procedência

| Artefato | Caminho |
| --- | --- |
| EDA CAGED individual | `EDA_caged.md` (mesma pasta) |
| EDA INEP individual | `EDA_Inep.md` (mesma pasta) |
| Painel CAGED mensal | `workspace.silver.novo_caged_movimentacoes` (68 meses) |
| Painel CAGED semestral | `workspace.gold.fato_caged_semestral` (12 semestres) |
| Gold INEP Brasil / UF | `workspace.gold.fato_inep_educacao_brasil_anual` / `..._uf_anual` (v2) |
| Dimensões da ponte | `workspace.gold.dim_cine_brasil` (372) + `workspace.gold.dim_cbo_ocupacao` (2.778) |
| Notebooks da integração | `031_silver_to_gold_inep` · `0311_..._analise` · `032_mapeamento_cine_cbo` |

**Notas técnicas:** números calculados em 30/10/2026 via queries diretas às tabelas — exceto os retratos ocupacionais da Seção 5.1 e o escopo/métricas da 7.4, cujos números por CBO família (silver CAGED) foram calculados em 02/11/2026 (ano com ano: CAGED 2021–2024 completo; UF×ano: join por sigla após normalização de 27 UFs, n=108; correlações Pearson/Spearman scipy com e sem log). Regra de coerência aplicada em toda a análise: cruzamento INEP×CAGED apenas no nível ano; semestres e meses usados apenas como decomposição interna do CAGED.

**EDA unificada concluída em 2026-10-30** · Autora: Fernanda Carnevalle de Melo
