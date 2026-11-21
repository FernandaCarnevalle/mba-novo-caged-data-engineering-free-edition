# MBA Engenharia de Dados — Previsão de Demanda Profissional e Formação Educacional no Brasil

**Instituição:** Universidade Presbiteriana Mackenzie  
**Projeto:** Engenharia de Dados aplicada aos microdados do Novo Caged (MTE) e do Censo da Educação Superior (INEP)

**Organização do trabalho:** [Trello — MBA | Previsão da Demanda por Ocupações](https://trello.com/b/sts8EjN4)

**Status das entregas:** [arquitetura dos pipelines e evidências de CI/CD](docs/status_entregas/arquitetura-pipelines-inep-caged.md)

**Glossário de dados:** [glossário de dados](docs/dicionario_dados/glossario_de_dados.md)

**Dashboard do produto:** [Relatório Mensal — Formação × Mercado de Trabalho](docs/relatorios/Relatorio_Mensal_Formacao_Mercado.html) — mapa, previsões e diagnóstico de desalinhamento com glossário interativo

## Problema de negócio

Instituições de ensino, organizações de formação profissional e gestores públicos precisam planejar a oferta de cursos diante das mudanças no mercado de trabalho, mas os indicadores de emprego e educação estão distribuídos em fontes e metodologias diferentes e possuem frequências de atualização distintas.

**Pergunta central:** Como utilizar dados históricos do emprego formal e da educação profissional para prever a evolução das admissões por ocupação e região e apoiar decisões de planejamento da formação profissional no Brasil?

## Objetivos

Desenvolver uma solução de Engenharia de Dados e Machine Learning para analisar e prever tendências de admissões no mercado de trabalho formal brasileiro, relacionando os resultados à oferta de educação profissional.

### Objetivos específicos

- Ingerir e integrar dados públicos de emprego e educação.
- Implementar um Lakehouse com camadas de dados brutos, tratados e analíticos.
- Construir um modelo dimensional para análises históricas e uma tabela analítica para Machine Learning.
- Treinar e avaliar modelos de previsão de admissões por UF e grupo ocupacional, considerando a compatibilização temporal com os dados educacionais.
- Criar um dashboard para acompanhar previsões, tendências e indicadores educacionais.
- Demonstrar arquitetura Lambda, CI/CD, qualidade e versionamento, conforme os requisitos acadêmicos e as possibilidades dos ambientes utilizados.

## Escopo do estudo e limitação de abrangência

O estudo usa os microdados do **Novo Caged (MTE)** para analisar e prever admissões no emprego formal e os microdados do **Censo da Educação Superior (INEP)**, de 2021 a 2024, para caracterizar a formação na graduação.

A integração usa uma [ponte provisória CINE × CBO](notebooks/03_analytics/034_bridge_provisoria_cine_cbo.ipynb), curada pela equipe, que associa áreas específicas de formação a subgrupos ocupacionais. Uma área pode se relacionar a vários subgrupos e vice-versa. A ponte registra a confiança e a justificativa dos pares, e uma tabela de cobertura identifica as áreas sem correspondência.


## 📊 Explore os resultados

Acesse os principais produtos analíticos desenvolvidos durante o projeto.

| Dashboard Unificado | Modelo Preditivo | Formação × Mercado |
|:---:|:---:|:---:|
| Indicadores Caged e INEP | Previsões de admissões | Análise de formação e demanda |
| [Abrir dashboard](https://kevynzap.github.io/mba-novo-caged-data-engineering-free-edition/eda/dashboard_unificado_caged_inep.html?utm_source=chatgpt.com) | [Abrir previsões](https://kevynzap.github.io/mba-novo-caged-data-engineering-free-edition/relatorios/dashboard_modelo_admissoes.html) | [Abrir relatório](https://kevynzap.github.io/mba-novo-caged-data-engineering-free-edition/relatorios/Relatorio_Mensal_Formacao_Mercado.html) |
| <img width="90" height="90" alt="qrcode_dashboard_unificado_caged_inep" src="https://github.com/user-attachments/assets/642c2d8a-a281-499f-b676-9f07520afa2e" /> | <img width="90" height="90" alt="qrcode_dashboard_modelo_admissoes" src="https://github.com/user-attachments/assets/52dda829-0fe2-4a16-bbb8-54add5545f7d" /> | <img width="90" height="90" alt="qrcode_Relatorio_Mensal_Formacao_Mercado" src="https://github.com/user-attachments/assets/49b19c13-3a61-4999-a69c-73722f1af4ae" /> |

## Desenho inicial da arquitetura

O projeto adota uma arquitetura **Lakehouse baseada no padrão Medallion**, estruturando os dados em Landing, Bronze, Silver e Gold.

A solução utiliza atualmente **Databricks Free Edition**, Apache Spark, Unity Catalog e Delta Lake. O processamento desenvolvido até o momento é predominantemente **batch**, adequado à publicação periódica dos microdados do Novo Caged.

A arquitetura considera os requisitos de Lambda, Star Schema, Wide Table, CI/CD e Machine Learning, distinguindo os componentes já implementados daqueles previstos para as próximas etapas.

- **Landing:** recepção e preservação dos arquivos oficiais disponibilizados pelas fontes.
- **Bronze:** ingestão dos microdados e dicionários de referência, com preservação dos valores de origem e metadados de rastreabilidade.
- **Silver:** padronização de nomes e tipos, tratamento de formatos, enriquecimento com descrições e validações de qualidade.
- **Gold:** construção de fatos e indicadores analíticos destinados a consultas, visualizações e modelagem preditiva.
- **Batch:** processamento dos dados históricos e das novas competências publicadas.
- **Streaming / Lambda:** requisito arquitetural a ser avaliado e demonstrado posteriormente; não corresponde a um fluxo de streaming já implementado.

### Diagrama da arquitetura

<img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/1f376c30-fae9-4150-bc0f-22bad81c13d1" />

A validação autenticada do Bundle no CI depende das credenciais do workspace. O deploy usa o commit aprovado pelo CI. As [evidências de CI/CD e o status da homologação operacional](docs/status_entregas/arquitetura-pipelines-inep-caged.md#arquitetura-de-cicd) estão na documentação de entregas.

## Arquitetura técnica

| Componente | Tecnologia | Responsabilidade |
|---|---|---|
| Ambiente principal | Databricks Free Edition | Desenvolvimento e execução dos pipelines |
| Armazenamento de arquivos | Unity Catalog Volumes | Preservação dos arquivos originais e staging de extração |
| Processamento | Apache Spark / PySpark / Spark SQL | Ingestão, transformação e agregação distribuída |
| Armazenamento analítico | Delta Lake | Persistência transacional das tabelas |
| Catálogo | Unity Catalog | Organização dos schemas e das tabelas |
| Orquestração | Databricks Jobs | Encadeamento das atividades de ingestão e transformação |
| Machine Learning | Python / scikit-learn e bibliotecas compatíveis | Treinamento e avaliação dos modelos |
| BI | Power BI | Visualização dos indicadores e resultados |
| Versionamento | Git / GitHub | Histórico e colaboração no código |
| CI/CD | GitHub Actions e Databricks Declarative Automation Bundles | Validação do repositório e deploy em `dev` |
| IaC | Terraform — planejado | Definição versionada dos recursos suportados |
| Qualidade | Validações PySpark e pytest | Verificação da integridade dos dados e do código |
| Gestão | Trello | Organização das atividades e acompanhamento das entregas |

### Ambientes de desenvolvimento

O projeto foi inicialmente desenvolvido em um workspace do **Azure Databricks**, com armazenamento ADLS Gen2. Esse ambiente permitiu validar um piloto de ingestão e armazenamento no padrão Medallion.

Posteriormente, o desenvolvimento principal foi transferido para a **Databricks Free Edition**, facilitando a colaboração e reduzindo a dependência de infraestrutura paga.

O ambiente Azure permanece pausado, podendo ser reutilizado para testes ou homologações futuras.

Na Free Edition, o projeto utiliza o catálogo `workspace`, com schemas `bronze`, `silver` e `gold`. Os arquivos originais ficam em Volumes, enquanto as tabelas Delta são gerenciadas pelo ambiente Databricks, sem necessidade de configurar armazenamento externo ADLS Gen2.

## Estrutura do repositório

```text
mba-novo-caged-data-engineering-free-edition/
│
├── .github/
│   ├── workflows/
│   │   ├── cd_databricks_dev.yml
│   │   └── ci_validacao_aut_repo.yml
│
├── docs/
│   ├── dicionario_dados
│   │   ├── dicionario-dados-novo-caged-movimentacao.xlsx
│   │   └── glossario_de_dados.md
│   ├── eda/
│   │   └── dashboard_unificado_caged_inep.html
│   ├── relatorios/
│   │   └── Relatorio_Mensal_Formacao_Mercado.html
│   └── status_entregas/
│       └── arquitetura-pipelines-inep-caged.md
|
├── infrastructure/
|    └── terraform/
|
├── notebooks/
│   ├── 00_setup/
│   │   ├── 01_create_catolog_schema.ipynb
│   │   └── 02_commom_functions.py
│   │
│   ├── 01_ingestao/
│   │   ├── 010_verificar_novos_arquivos_caged.ipynb
│   │   ├── 011_landing_to_bronze_caged.ipynb
│   │   ├── 012_dicionarios_referencia_caged.ipynb
│   │   ├── 013_download_landing_inep.ipynb
│   │   └── 014_landing_to_bronze_inep.ipynb
│   │
│   ├── 02_transformacao/
│   │   ├── 020_bronze_to_silver_caged.ipynb
│   │   ├── 021_analise_qualidade_bronze_caged.ipynb
│   │   ├── 022_bronze_to_silver_ref_caged.ipynb
│   │   ├── 023_analise_qualidade_inep.ipynb
│   │   └── 024_bronze_to_silver_inep.ipynb
│   │
│   └── 03_analytics/
│       ├── 030_silver_to_gold_caged.ipynb
│       ├── 031_silver_to_gold_inep.ipynb
│       ├── 0311_silver_to_gold_inep_analise.ipynb
│       ├── 032_mapeamento_cine_cbo.ipynb
│       ├── 033_construcao_bridge_cine_cbo.ipynb
│       ├── 034_bridge_provisoria_cine_cbo.ipynb
│       ├── 035_gold_ml_features.ipynb
│       ├── 036_treino_backtest_admissoes.ipynb
│       ├── 037_previsoes_operacionais.ipynb
│       ├── 038_desalinhamento_formacao_mercado.ipynb
│       └── EDA.ipynb
│
├── resources/
│   └── job_caged.yml
│   └── job_inep.yml
│   └── job_ml.yml
│
├── src/
│   └── transformations/
│
├── tests/
│   └── test_bundle_resources.py
│   └── test_data_quality_rules.py
│   └── test_pipeline_contracts.py
│
├── README.md
├── databricks.yml
├── job-settings-novo-caged.json
```

`tests/` contém testes automatizados executados pelo CI, incluindo contratos do pipeline, regras de qualidade e recursos do bundle. `src/transformations/` e `infrastructure/terraform/` contêm arquivos iniciais de preparação.

## Desenvolvimento das camadas de dados

### Landing — Ingestão dos arquivos originais

A Landing utiliza um volume do Unity Catalog:

`/Volumes/workspace/bronze/raw_novo_caged`

Os arquivos oficiais do Novo Caged são recebidos no formato `.7z`, organizados por ano e competência.

O notebook `010_verificar_novos_arquivos_caged.ipynb` consulta o FTP público, identifica novas competências e registra as informações para o processamento posterior.

O fluxo desenvolvido contempla a identificação e o download de novas competências do ano vigente. Revisões retroativas de arquivos já ingeridos exigem uma estratégia complementar.

### Bronze — Preservação e rastreabilidade

A tabela principal é:

`workspace.bronze.novo_caged_movimentacoes`

O notebook `011_landing_to_bronze_caged.ipynb` realiza a extração dos arquivos, a leitura com Apache Spark, a inclusão de metadados de ingestão e a gravação em Delta Lake.

A estrutura permite processamento por competência e sobrescrita seletiva dos períodos processados.

Entre os metadados preservados estão:

- Competência de referência.
- Nome do arquivo de origem.
- Caminho do arquivo original.
- Data e horário de ingestão.

O notebook `012_dicionarios_referencia_caged.ipynb` também disponibiliza na Bronze os dicionários oficiais do Novo Caged, preservando os códigos e as descrições fornecidos pela fonte.

**Decisão arquitetural:** as referências são inicialmente armazenadas na Bronze porque suas descrições e representações podem exigir tratamento e padronização antes do uso em camadas analíticas.

### Silver — Padronização e qualidade

A Silver contempla a tabela:

`workspace.silver.novo_caged_movimentacoes`

O notebook `021_analise_qualidade_bronze_caged.ipynb` documenta análises de qualidade, incluindo valores ausentes, formatos numéricos, domínios categóricos, códigos sem correspondência, duplicidades e cobertura temporal.

O notebook `020_bronze_to_silver_caged.ipynb` implementa:

- Conversão de tipos numéricos e datas.
- Padronização dos nomes das colunas.
- Normalização de formatos numéricos.
- Enriquecimento com descrições de referências.
- Preservação dos metadados de rastreabilidade.
- Reprocessamento seletivo por competência.

O notebook `022_bronze_to_silver_ref_caged.ipynb` trata e disponibiliza dez tabelas de referência tipadas em `workspace.silver`.

#### Decisões de qualidade

**Preservação de duplicidades:** registros com atributos idênticos não são removidos automaticamente, pois a fonte não disponibiliza uma chave natural que permita distinguir com segurança duplicação indevida de movimentações legítimas.

**Códigos sem correspondência:** movimentações com códigos não encontrados nos dicionários são preservadas; suas descrições podem permanecer nulas.

**Valores ausentes:** campos numéricos são convertidos com tratamento explícito de formatos inválidos, evitando exclusões silenciosas.

**Granularidade:** os registros de movimentação permanecem individualizados na Silver; a agregação temporal é responsabilidade da Gold.

#### Cobertura histórica documentada

A análise registrada nos notebooks apresenta:

| Indicador | Resultado documentado |
|---|---|
| Primeiro período | Janeiro de 2021 |
| Último período | Agosto de 2026 |
| Competências | 68 |
| Movimentações | 259.514.177 |

Esses números são provenientes da análise registrada no repositório e deverão ser atualizados quando novas competências forem ingeridas ou houver reprocessamento das fontes.

### Gold — Indicadores semestrais

O notebook `030_silver_to_gold_caged.ipynb` implementa a construção da tabela:

`workspace.gold.fato_caged_semestral`

**Granularidade:** ano × semestre × UF × ocupação CBO 2002.

A fato é construída a partir dos movimentos tratados na Silver e apresenta:

- Total de admissões.
- Total de desligamentos.
- Total de movimentações.
- Saldo de empregos.
- Identificação temporal.
- Código e descrição da UF.
- Código e descrição da ocupação CBO.

As admissões são identificadas por `saldo_movimentacao = 1`, enquanto os desligamentos utilizam `saldo_movimentacao = -1`.

O processamento considera somente semestres com seis competências mensais disponíveis, verificadas globalmente na Silver.

O notebook também implementa validações de unicidade, consistência das métricas e reconciliação dos totais com a Silver, além de recomputação e substituição da tabela Delta para permitir reexecuções sem duplicar os resultados.

**Status:** notebook desenvolvido e versionado; validado em 31/10/2026 contra os dados do workspace — a fato cobre 2021S1–2026S1 com apenas semestres completos (2026S2, parcial com apenas jul–ago, permanece excluída).

#### Decisões metodológicas para a Gold

- A análise trabalhista será inicialmente semestral para permitir futura compatibilização com a base de educação formal.
- A fato Caged será construída independentemente da fonte educacional.
- Não serão utilizados indicadores salariais no escopo analítico atual.
- Semestres incompletos serão excluídos da fato definitiva.
- A Silver continuará disponível na granularidade original, permitindo estudos mensais posteriores.

## Camadas de dados — INEP (Censo da Educação Superior)

Os microdados do Censo da Educação Superior do INEP seguem o mesmo padrão Medallion:

**Landing/Bronze:** os notebooks `013_download_landing_inep.ipynb` e `014_landing_to_bronze_inep.ipynb` baixam e ingerem os microdados por curso na tabela `workspace.bronze.inep_superior_cursos`, preservando os nomes originais do dicionário INEP (cerca de 200 colunas, todas STRING) e metadados de ingestão (`arquivo_origem`, `ano_ingestao`, `hash_origem`, `dt_ingestao`).

**Silver:** o notebook `023_analise_qualidade_inep.ipynb` documenta as análises de qualidade da base educacional. O `024_bronze_to_silver_inep.ipynb` produz a tabela `workspace.silver.inep_superior_cursos`, tipada e enriquecida, com a classificação CINE Brasil em quatro níveis, características da IES e do curso, e métricas agregadas (vagas, inscritos, ingressantes, matrículas, concluintes).

**Gold:** o notebook `031_silver_to_gold_inep.ipynb` constrói as tabelas:

- `workspace.gold.dim_cine_brasil` — dimensão da classificação CINE Brasil em quatro níveis (área geral → específica → detalhada → rótulo).
- `workspace.gold.fato_inep_educacao_brasil_anual` — fato anual para o Brasil (grão: ano × rótulo CINE × modalidade de ensino).
- `workspace.gold.fato_inep_educacao_uf_anual` — fato anual por UF (mesmo grão acrescido da UF; métricas de vagas restritas a cursos presenciais).

O notebook `0311_silver_to_gold_inep_analise.ipynb` registra as validações da Gold educacional.

**Cobertura:** Censos de 2021 a 2024.

**Correspondência CINE × CBO:** os notebooks `032_mapeamento_cine_cbo.ipynb`, `033_construcao_bridge_cine_cbo.ipynb` e `034_bridge_provisoria_cine_cbo.ipynb` documentam e constroem a ponte entre as áreas de formação (CINE) e as ocupações do mercado formal (CBO 2002), materializada nas tabelas gold `bridge_cine_cbo_provisoria` (pares área específica × subgrupo CBO, com confiança e justificativa) e `bridge_cine_cbo_provisoria_cobertura` (diagnóstico de cobertura), viabilizando a integração com a fato do Caged.

A documentação detalhada de todas as tabelas está no [glossário de dados](docs/dicionario_dados/glossario_de_dados.md).

## Integração com educação formal

A proposta do projeto contempla relacionar os indicadores do mercado de trabalho à disponibilidade e à formação de profissionais no Brasil.

A base educacional utilizada é o **Censo da Educação Superior do INEP**, com periodicidade **anual** e cobertura de 2021 a 2024 nos microdados ingeridos. Campos, classificações (CINE Brasil em quatro níveis) e granularidade geográfica (Brasil e UF) estão documentados no [glossário de dados](docs/dicionario_dados/glossario_de_dados.md).

Um desafio metodológico é relacionar classificações de cursos ou áreas de formação às ocupações da **Classificação Brasileira de Ocupações (CBO)**.

Essa correspondência não deve ser presumida como direta: uma formação pode estar associada a várias ocupações, e uma ocupação pode reunir profissionais de diferentes formações.

A bridge provisória usada pelo ML relaciona áreas específicas CINE a subgrupos CBO. O notebook [034](notebooks/03_analytics/034_bridge_provisoria_cine_cbo.ipynb) materializa essa relação e registra a cobertura.

## Modelagem dimensional e Wide Table

A arquitetura Gold contempla dois produtos analíticos complementares.

**Modelo dimensional (Star Schema):** organização das fatos e dimensões para análise histórica de admissões, desligamentos, ocupações, regiões e indicadores educacionais. Já implementadas na Gold: `dim_cbo_ocupacao`, `dim_cine_brasil`, `fato_caged_semestral`, `fato_inep_educacao_brasil_anual`, `fato_inep_educacao_uf_anual`, `bridge_cine_cbo_provisoria` e `bridge_cine_cbo_provisoria_cobertura`.

**Wide Table para Machine Learning:** consolidação das variáveis necessárias à previsão, respeitando a compatibilidade entre granularidades e a disponibilidade temporal das fontes. Implementada na Gold como `ml_features_mensal_uf_cbo` (grão mensal: competência × UF × subgrupo CBO), com suporte a: triagem estatística de features (`ml_features_ols_screening`, OLS com efeitos fixos de UF e mês), backtest por cutoffs móveis (`ml_backtest_admissoes`) e previsões versionadas (`previsoes_admissoes`, horizonte set/2026–ago/2027).

As previsões operacionais têm horizonte de 12 meses. As variáveis são construídas com informações disponíveis na data de corte para evitar vazamento temporal.

## Resultados de EDA e Machine Learning

O [dashboard Inep × Caged](docs/eda/dashboard_unificado_caged_inep.html) registra os achados exploratórios do Novo Caged e do Censo da Educação Superior.

O [dashboard de ML de previsão de admissões](notebooks/03_analytics/EDA%20%281%29/00_EDA_CAGED/dashboard_modelo_admissoes.html) foi desenvolvido por Fernanda Carnevalle no Databricks e publicado no repositório por Kevyn Zap.

O [Relatório Mensal — Formação × Mercado de Trabalho](docs/relatorios/Relatorio_Mensal_Formacao_Mercado.html) é o dashboard de produto para instituições de ensino: mapa do Brasil com previsões de 12 meses, diagnóstico de desalinhamento formação × demanda e glossário interativo, com os dados das tabelas gold embutidos no próprio arquivo HTML.

- **Emprego e formação em 2024.** O Novo Caged registrou **25,3 milhões de admissões** e o INEP registrou **1,33 milhão de concluintes** da graduação. Entre 2021 e 2024, o saldo formal caiu **41%**. Em 2024, **66,8% dos ingressantes** estavam no EaD.
- **Relação entre as bases.** A correlação de Pearson entre admissões do Novo Caged e concluintes do INEP no mesmo ano foi de **0,98**, em **108 observações UF × ano** (27 UFs de 2021 a 2024). A associação reflete em grande parte diferenças de escala entre UFs. [Metodologia da EDA integrada](docs/eda/EDA_Unificada_Inep_Caged.md#41-correlações-n108).
- **Triagem de variáveis para previsão mensal.** Na série do Caged, as maiores correlações de Pearson com as admissões do mês seguinte foram tendência (**0,70**), desligamentos do mês anterior (**0,69**) e salário do mês anterior (**0,68**). A correlação das admissões defasadas em um mês foi **0,40**. Esses valores medem a associação exploratória de cada variável com o alvo.

O [notebook de backtest](notebooks/03_analytics/036_treino_backtest_admissoes.ipynb) e o [dashboard de avaliação do modelo](notebooks/03_analytics/EDA%20%281%29/00_EDA_CAGED/dashboard_modelo_admissoes.html) documentam a avaliação da previsão de admissões mensais do Novo Caged para um mês à frente, em **12 janelas expansivas de jan–dez/2025**. Nas **698 séries UF × subgrupo CBO**, o LightGBM teve **MAE de 21,5 admissões por série-mês** e **RMSE de 72,2**. O baseline sazonal teve MAE de **24,4** e RMSE de **75,9**. O MASE do LightGBM foi de **0,80** nas 20 séries de maior volume e de **1,36** no painel completo, onde o baseline sazonal obteve **1,11**.

## Autoria das contribuições de EDA e estatística

O repositório é um trabalho em equipe. A autoria de cada parte está registrada no histórico de commits. Os itens abaixo são de **Fernanda Carnevalle**:

- [`notebooks/03_analytics/EDA.py`](notebooks/03_analytics/EDA.py) e [`notebooks/03_analytics/04_eda_rigorosa_bussab_moretin.py`](notebooks/03_analytics/04_eda_rigorosa_bussab_moretin.py): EDA do Novo Caged, incluindo a EDA rigorosa semestral segundo Bussab & Moretin.
- [`docs/eda/EDA_caged.md`](docs/eda/EDA_caged.md), [`docs/eda/EDA_Inep.md`](docs/eda/EDA_Inep.md) e [`docs/eda/EDA_Unificada_Inep_Caged.md`](docs/eda/EDA_Unificada_Inep_Caged.md): documentação das análises exploratórias.
- [`docs/eda/dashboard_unificado_caged_inep.html`](docs/eda/dashboard_unificado_caged_inep.html): dashboard HTML da EDA unificada Caged × INEP.
- [`notebooks/03_analytics/034_bridge_provisoria_cine_cbo.ipynb`](notebooks/03_analytics/034_bridge_provisoria_cine_cbo.ipynb): bridge provisória CINE × CBO.
- Roteiro unificado de apresentação EDA/modelo/entregável.
- Notebooks [035](notebooks/03_analytics/035_gold_ml_features.ipynb), [036](notebooks/03_analytics/036_treino_backtest_admissoes.ipynb), [037](notebooks/03_analytics/037_previsoes_operacionais.ipynb) e [038](notebooks/03_analytics/038_desalinhamento_formacao_mercado.ipynb) (ML e previsão): desenvolvidos por Fernanda Carnevalle no Databricks e publicados no repositório por Kevyn Zap.

## Glossário de dados

A documentação das tabelas do Novo Caged e do INEP nas camadas bronze, silver e gold está consolidada em [docs/dicionario_dados/glossario_de_dados.md](docs/dicionario_dados/glossario_de_dados.md), incluindo:

- Propósito, grão e colunas das tabelas do projeto, entre elas as bridges CINE × CBO e as tabelas de Machine Learning.
- Contexto de negócios das fontes oficiais (Novo CAGED/MTE e Censo da Educação Superior/INEP).
- Verificação dos contextos contra os dados do workspace (executada em 31/10/2026).
- Chaves de junção recomendadas entre fatos, dimensões e dicionários de referência.

## Orquestração e automação

Os Databricks Jobs são definidos nos YAMLs de [`resources/`](resources/), incluídos pelo [`databricks.yml`](databricks.yml). O status das entregas, no início deste README, reúne as dependências dos Jobs e as evidências aprovadas.

### CI/CD

O GitHub Actions valida mudanças destinadas à `main`. Após um push à `main` com CI aprovado, o CD implanta o bundle em `dev` a partir do commit validado. A execução dos Databricks Jobs é uma operação separada.

## Limitações e próximos passos

1. Validar a execução ponta a ponta dos Jobs no workspace e registrar as evidências operacionais.
2. Revisar a estratégia incremental para identificar alterações em competências já ingeridas, inclusive quando suas contagens forem mantidas.
3. Avaliar a validação das Golds INEP contra as Sinopses Estatísticas oficiais e a cobertura da bridge provisória CINE × CBO.
4. Avaliar o escopo de Terraform e da demonstração de Lambda e streaming na Free Edition.

### Limitações metodológicas

O Novo Caged representa movimentações de vínculos formais de trabalho. Portanto, o volume de admissões não deve ser interpretado como a totalidade das vagas disponíveis nem como uma medida direta de demanda por competências específicas.

A relação entre formação educacional e ocupação profissional também requer interpretação cuidadosa, considerando classificações distintas, defasagens temporais e ausência de correspondência individual entre bases.

---

**Projeto acadêmico — MBA em Engenharia de Dados | Universidade Presbiteriana Mackenzie.**
