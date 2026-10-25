# DE/PARA: Cursos FATEC × Ocupações CBO 2025

## Resumo Executivo

Tabela de correspondência entre **116 cursos da FATEC** e **33 ocupações CBO** selecionadas, mapeadas por similaridade semântica com base nas movimentações formais do CAGED 2025.

**Localização:** `workspace.silver.cursos_fatec_ocupacoes_cbo_2025`  
**Linhas:** 116 (um curso por linha)  
**Colunas:** 8  
**Tipo:** Delta Lake (Managed Table)  
**Última atualização:** Outubro 2026  

---

## Objetivo e Contexto

Este DE/PARA é uma etapa analítica dentro de um projeto maior de previsão de demanda de trabalho e formação profissional. Ele não busca mapear todas as profissões do mercado brasileiro, mas oferecer um mecanismo controlado de correspondência entre ofertas de cursos técnicos (FATEC) e demanda de ocupações (CAGED).

Para entender melhor o escopo e as limitações deste estudo, consulte a seção **"Escopo do estudo e limitação de abrangência"** no [README.md](../../README.md#escopo-do-estudo-e-limitação-de-abrangência).

---

## Estrutura da Tabela

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `curso` | string | Nome do curso FATEC (limpo e normalizado) |
| `eixo_tecnologico` | string | Eixo tecnológico FATEC associado ao curso |
| `ocupacao_cbo` | string | Descrição da ocupação CBO selecionada |
| `cbo_codigo` | string | Código numérico da ocupação CBO (CBO 2002) |
| `movimentacoes_2025` | bigint | Número total de admissões dessa ocupação no CAGED 2025 |
| `similaridade` | float | Score de similaridade semântica (0 a 1, arredondado a 3 casas decimais) |
| `forca_match` | string | Classificação: `'forte'` (≥ 0.7) ou `'fraco'` (< 0.7) |

---

## Metodologia

### 1. Identificação dos Candidatos (60 Ocupações CBO)

A tabela começa com as **60 ocupações CBO mais frequentes** nas movimentações do CAGED 2025, filtradas por descritores técnicos/profissionais:

- `analista`, `programador`, `administrador`, `designer`, `desenhista`, `tecnólogo`, `técnico`, `engenheiro`, `cientista`, `agrônomo`, `logístico`, `marketing`, `publicidade`, `jornalista`, `moda`

**Critério:** Ocupações com alta frequência de admissões e perfil alinhado com formação técnica.

### 2. Cruzamento Semântico

Para cada um dos **116 cursos FATEC**, calcula-se a similaridade semântica com cada uma das 60 ocupações usando:

```
ai_similarity(
  concat(curso, " - ", eixo_tecnologico), 
  descricao_ocupacao_cbo
)
```

**Função:** `ai_similarity()` do Databricks (baseado em embeddings semânticos)  
**Score:** Varia de 0 a 1 (não é probabilidade; scores são relativos para ranking)

### 3. Seleção do Melhor Match

Para cada curso, seleciona-se a ocupação com **maior score de similaridade** (ROW_NUMBER PARTITION BY curso ORDER BY similaridade DESC).

**Resultado:** 116 linhas, uma por curso, sempre com match (o ranking nunca deixa nenhum curso sem ocupação).

### 4. Arredondamento e Classificação

- Score de similaridade é **arredondado a 3 casas decimais** para evitar contradições visuais
- Classificação de força de match:
  - **`'forte'`** → similaridade ≥ 0.7 (alinhamento natural)
  - **`'fraco'`** → similaridade < 0.7 (alinhamento por aproximação)

---

## Distribuição de Qualidade

### Força de Match

| Classificação | Quantidade | % | Faixa de Similaridade |
|---------------|-----------:|---|----------------------|
| **Forte** | 64 | 55% | 0.701 – 0.93 |
| **Fraco** | 52 | 45% | 0.599 – 0.70 |
| **Total** | **116** | **100%** | 0.599 – 0.93 |

**Média de similaridade:** 0.714  
**Mediana:** ~0.71  

### Exemplos de Matches

#### Forte (≥ 0.7)
- `Engenharia Civil` → `Engenheiro Civil` (0.93)
- `Análise e Desenvolvimento de Sistemas` → `Analista de Sistemas` (0.87)
- `Gestão de Recursos Humanos` → `Analista de Recursos Humanos` (0.82)

#### Fraco (< 0.7)
- `Ciência de Dados` → `Analista de Redes` (0.75) — *ainda acima, mas próximo do corte*
- `Marketing Digital` → `Agente de Atendimento ao Cliente` (0.65)
- Cursos sem ocupação clara nos 60 candidatos

---

## Limitações Intencionais

### Pelo lado das ocupações

Das **2.656 ocupações CBO distintas** no CAGED 2025:
- **33 (1.2%)** aparecem no DE/PARA
- **2.623 (98.8%)** não aparecem

**Por quê?** É esperado por desenho, não por defeito:
- Ocupações como faxineiro, vendedor, motorista, auxiliar administrativo não têm correspondência com cursos FATEC técnicos
- Mesmo entre os 60 candidatos qualificados, 27 nunca foram selecionados como melhor match para nenhum curso
- O DE/PARA mapeia cursos para ocupações, não o inverso

### Pelo lado dos cursos

**100% dos 116 cursos** receberam um match (o algoritmo sempre escolhe um):
- 64 com boa qualidade (forte)
- 52 com qualidade questionável (fraco)

A questão real de atenção é a presença de **52 cursos com match fraco**, que reflete:
- **CBO 2002 não retrata ocupações modernas de dados/tecnologia** (desalinhamento estrutural)
- **Recorte de 60 candidatos pode ser restritivo** para cursos interdisciplinares

---

## Como Reproduzir

Veja o notebook [02_de_para_fatec_ocupacoes_cbo.ipynb](../02_transformacao/02_de_para_fatec_ocupacoes_cbo.ipynb) para:
1. Identificação dos 60 candidatos
2. Cruzamento semântico completo
3. Validação e exploração dos resultados

**Comando SQL direto:**
```sql
SELECT * FROM workspace.silver.cursos_fatec_ocupacoes_cbo_2025
ORDER BY similaridade DESC;
```

---

## Considerações para Uso

### Quando usar este DE/PARA

✅ Análise de alinhamento entre oferta de cursos FATEC e demanda de ocupações  
✅ Contexto do projeto maior de previsão de demanda de trabalho  
✅ Agregações por eixo tecnológico ou força de match  
✅ Validação qualitativa de ocupações por especialista  

### Quando NÃO usar

❌ Como catálogo oficial de correspondências cursos-ocupações  
❌ Para extrapolação além do contexto FATEC-CAGED 2025  
❌ Como verdade absoluta sobre mercado de trabalho (é um recorte)  
❌ Para decisões de política pública sem revisão especializada  

---

## Parâmetros Metodológicos Documentados

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| **Ocupações candidatas** | 60 | Mais frequentes no CAGED 2025 + filtro técnico |
| **Filtro descritivo** | RLIKE (analista\|programador\|...) | Foco em ocupações técnicas/profissionais |
| **Função semântica** | `ai_similarity()` | Embeddings do Databricks |
| **Ranking** | ROW_NUMBER / ORDER BY similaridade DESC | Melhor match por curso |
| **Corte de força** | 0.7 | Aproximadamente na média (0.714) da distribuição real |
| **Arredondamento** | 3 casas decimais | Consistência visual com dados reportados |

---

## Histórico e Versionamento

| Data | Versão | Evento |
|------|--------|--------|
| Out 2026 | 1.0 | Criação inicial em Bronze, migração para Silver |
| Out 2026 | 1.1 | Adição de coluna `forca_match` |

**Próximas atualizações:** Condicionadas a revisão dos dados CAGED e eventuais ajustes de metodologia.

---

## Contato e Dúvidas

- **Responsável:** Fernanda Carnevalle
- **Projeto:** MBA Engenharia de Dados — Observatório de Demanda Profissional e Formação Técnica
- **Fonte dos dados:** CAGED (MTPS), FATEC, CBO 2002 (MTE)

Para dúvidas sobre escopo, limitações ou metodologia, consulte o documento [DE_PARA.txt](../../DE_PARA.txt) ou a seção de escopo no README.
