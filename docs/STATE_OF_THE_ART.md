# Estado del Arte - Skill Gap Analysis

## 1. Introducción

Este documento presenta un análisis del estado del arte en sistemas de análisis de brechas de habilidades (skill gap analysis) y herramientas relacionadas. El proyecto SkillGap se posiciona en este contexto, utilizando técnicas de análisis de datos, procesamiento de lenguaje natural (NLP) y análisis de redes (network science) para identificar las habilidades faltantes en perfiles profesionales.

## 2. Soluciones Existentes

### 2.1 LinkedIn Skills Assessment

**Descripción**: LinkedIn ofrece evaluaciones de habilidades donde los usuarios pueden demostrar su competencia en diferentes áreas técnicas y profesionales.

**Características**:
- Evaluaciones estandarizadas por skill
- Certificaciones verificables
- Comparación con otros profesionales
- Recomendaciones de cursos

**Limitaciones**:
- Basado en auto-evaluación del usuario
- No analiza directamente las ofertas de empleo
- No calcula brechas específicas para roles objetivo
- No utiliza análisis de grafos para identificar relaciones entre skills

**Diferencia con SkillGap**: Nuestro proyecto analiza directamente las ofertas de empleo del mercado, extrae habilidades requeridas mediante NLP, y calcula brechas específicas comparando el perfil del usuario con las demandas reales del mercado.

### 2.2 Jobscan

**Descripción**: Herramienta que compara el CV de un usuario con descripciones de ofertas de trabajo para mejorar el match.

**Características**:
- Análisis de palabras clave
- Optimización de CV para ATS (Applicant Tracking Systems)
- Scoring de match con ofertas específicas

**Limitaciones**:
- Enfoque en optimización de CV, no en desarrollo de habilidades
- No proporciona análisis de tendencias del mercado
- No utiliza análisis de redes para identificar comunidades de skills
- Análisis superficial basado en keywords

**Diferencia con SkillGap**: Nuestro proyecto va más allá del matching simple, proporcionando análisis de grafos, clustering de ofertas, y recomendaciones priorizadas de skills a desarrollar basadas en la demanda del mercado.

### 2.3 Coursera / Udacity Skill Assessments

**Descripción**: Plataformas de educación online que ofrecen evaluaciones de habilidades y recomendaciones de cursos.

**Características**:
- Evaluaciones de habilidades
- Recomendaciones personalizadas de cursos
- Certificaciones profesionales

**Limitaciones**:
- No analizan ofertas de empleo reales
- Recomendaciones basadas en contenido educativo disponible
- No consideran la demanda real del mercado laboral
- Falta de análisis de tendencias y co-ocurrencias de skills

**Diferencia con SkillGap**: Nuestro proyecto se basa en datos reales del mercado laboral (ofertas de empleo), no en catálogos de cursos, proporcionando una visión más precisa de lo que realmente demandan los empleadores.

### 2.4 Burning Glass Technologies / Lightcast

**Descripción**: Plataformas de análisis de mercado laboral que analizan millones de ofertas de trabajo para identificar tendencias.

**Características**:
- Análisis de grandes volúmenes de ofertas
- Identificación de tendencias de habilidades
- Reportes de mercado laboral

**Limitaciones**:
- Soluciones empresariales costosas
- No proporcionan análisis personalizado para usuarios individuales
- No incluyen análisis de grafos de co-ocurrencia
- Interfaz compleja para usuarios finales

**Diferencia con SkillGap**: Nuestro proyecto es accesible para usuarios individuales, proporciona análisis personalizado basado en el perfil del usuario, e incluye visualizaciones interactivas y análisis de redes.

## 3. Técnicas Analíticas Utilizadas

### 3.1 Procesamiento de Lenguaje Natural (NLP)

**Técnica**: Extracción de habilidades mediante spaCy y PhraseMatcher

**Implementación**:
- Uso de modelo multilingüe (`xx_ent_wiki_sm`) para soportar español e inglés
- Taxonomía de habilidades con sinónimos y variantes
- Matching de frases con normalización (case-insensitive)
- Limpieza de HTML de descripciones de ofertas

**Ventajas**:
- Detección robusta de habilidades incluso con variantes
- Soporte multiidioma
- Extensible mediante taxonomía en CSV

**Limitaciones y mejoras futuras**:
- Matching basado en reglas (no semántico)
- Podría mejorarse con embeddings (Word2Vec, BERT) para detección semántica
- No detecta habilidades implícitas o contextuales

### 3.2 Análisis de Grafos (Network Science)

**Técnica**: Análisis de redes de co-ocurrencia de habilidades

**Implementación**:
- Grafo bipartito jobs-skills
- Proyección a grafo de co-ocurrencia skill-skill
- Cálculo de centralidades (degree, betweenness, closeness, eigenvector)
- Detección de comunidades mediante algoritmo de Louvain

**Aplicaciones**:
- Identificación de habilidades "puente" (high betweenness)
- Detección de comunidades temáticas (ej: "Data Engineering", "BI/Reporting")
- Visualización de relaciones entre habilidades

**Ventajas**:
- Revela relaciones no obvias entre habilidades
- Identifica clusters de habilidades complementarias
- Proporciona insights sobre la estructura del mercado laboral

**Limitaciones y mejoras futuras**:
- Análisis estático (no temporal)
- Podría incluir análisis de evolución temporal de skills
- Podría usar grafos dirigidos para relaciones de dependencia

### 3.3 Clustering de Ofertas

**Técnica**: K-means clustering basado en vectores binarios de habilidades

**Implementación**:
- Representación de ofertas como vectores binarios (presencia/ausencia de skills)
- Normalización con StandardScaler
- K-means con k=4 (configurable)
- Interpretación de clusters como "tipologías de ofertas"

**Aplicaciones**:
- Segmentación de ofertas por perfil de habilidades
- Identificación de nichos de mercado
- Recomendación de ofertas similares

**Ventajas**:
- Agrupa ofertas con perfiles similares
- Facilita la exploración del mercado
- Identifica diferentes "tipos" de roles

**Limitaciones y mejoras futuras**:
- K-means puede no capturar relaciones no lineales
- Podría usar clustering jerárquico o DBSCAN
- Podría incorporar features adicionales (salario, ubicación, seniority)

### 3.4 Análisis de Skill Gap

**Técnica**: Cálculo de match ratio y priorización de habilidades faltantes

**Implementación**:
- Match ratio = (skills del usuario ∩ skills del job) / skills del job
- Priorización basada en frecuencia de aparición en ofertas
- Cálculo de perfil "ideal" basado en demanda del mercado

**Aplicaciones**:
- Identificación de habilidades críticas faltantes
- Recomendaciones priorizadas de desarrollo
- Comparación de perfil usuario vs. perfil ideal

**Ventajas**:
- Métrica clara y comprensible
- Priorización basada en datos reales
- Personalización por perfil del usuario

**Limitaciones y mejoras futuras**:
- No considera la dificultad de adquirir cada skill
- No incluye tiempo estimado de aprendizaje
- Podría incorporar análisis de ROI (retorno de inversión) por skill

## 4. Limitaciones del Proyecto Actual

### 4.1 Limitaciones Técnicas

1. **Taxonomía de habilidades limitada**: Aunque expandida a 47 skills, aún es finita y puede no cubrir todos los nichos
2. **Matching basado en reglas**: No captura variaciones semánticas o habilidades implícitas
3. **Datos de una sola fuente**: Solo JSearch API, podría beneficiarse de múltiples fuentes
4. **Análisis estático**: No considera evolución temporal de demandas

### 4.2 Limitaciones de Datos

1. **Cuota de API**: Limitación en número de requests (MAX_NUM_PAGES=1)
2. **Cobertura geográfica**: Principalmente España, limitado a países soportados por JSearch
3. **Frecuencia de actualización**: Datos cacheados, pueden no reflejar ofertas más recientes

### 4.3 Limitaciones de Análisis

1. **No considera salarios**: No analiza relación skills-salario
2. **No analiza crecimiento temporal**: No identifica skills emergentes o en declive
3. **Clustering simple**: K-means puede no capturar todas las relaciones complejas

## 5. Trabajo Futuro

### 5.1 Mejoras Técnicas

1. **NLP Semántico**: Integrar embeddings (BERT, Sentence-BERT) para detección semántica de skills
2. **Análisis Temporal**: Tracking de evolución de demandas de skills a lo largo del tiempo
3. **Múltiples Fuentes**: Integrar APIs adicionales (Indeed, LinkedIn, etc.)
4. **Modelos Predictivos**: ML para predecir demanda futura de skills

### 5.2 Mejoras de Análisis

1. **Análisis de Salarios**: Correlación skills-salario
2. **Recomendaciones de Cursos**: Integración con catálogos de cursos online
3. **Roadmaps de Aprendizaje**: Secuencias sugeridas de skills a desarrollar
4. **Análisis de Competencia**: Comparación con otros candidatos

### 5.3 Mejoras de UX

1. **Dashboard más interactivo**: Filtros avanzados, comparaciones side-by-side
2. **Exportación de reportes**: PDF/Excel con análisis completo
3. **Alertas**: Notificaciones cuando aparecen ofertas con alto match
4. **Integración con CV**: Análisis automático desde CV/LinkedIn

## 6. Conclusiones

El proyecto SkillGap combina técnicas avanzadas de análisis de datos (NLP, grafos, clustering) para proporcionar un análisis personalizado de brechas de habilidades basado en datos reales del mercado laboral. Aunque existen soluciones similares, nuestro enfoque se distingue por:

1. **Análisis basado en ofertas reales**: No en auto-evaluaciones o catálogos de cursos
2. **Análisis de redes**: Identificación de relaciones y comunidades de skills
3. **Personalización**: Análisis específico para el perfil del usuario
4. **Accesibilidad**: Dashboard interactivo accesible para usuarios individuales
5. **Visualizaciones avanzadas**: Grafos interactivos, radar charts, clustering

Las limitaciones actuales abren oportunidades para investigación y desarrollo futuro, especialmente en el área de NLP semántico, análisis temporal, y modelos predictivos.

