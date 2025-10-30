# Logical Fallacy Detection Analysis

**Project**: Debate Fallacy Detector  
**Course**: Dartmouth COSC 072, Winter 2025  
**Author**: Javier Agustin Rodillas  
**Last Updated**: October 29, 2025

---

## Executive Summary

This project compares two approaches to detecting logical fallacies in text:
1. **Random Forest Classifier** with TF-IDF vectorization
2. **Large Language Model** (meta.llama-3-2-3b-instruct)

**Key Finding**: The Random Forest classifier significantly outperformed the small LLM, achieving 83.0% accuracy compared to 16.5% for the LLM on the same validation dataset.

---

## Dataset

**Source**: [tasksource/logical-fallacy](https://huggingface.co/datasets/tasksource/logical-fallacy) from Hugging Face

**Fallacy Types Analyzed** (10 categories):
- Ad Hominem
- Ad Populum
- Appeal to Emotion
- Circular Reasoning
- Fallacy of Credibility
- Fallacy of Extension
- Fallacy of Relevance
- False Causality
- False Dilemma
- Faulty Generalization

**Data Split**:
- Training: 2,807 samples (~70%)
- Validation: 401 samples (~10%)
- Testing: 802 samples (~20%)

**Preprocessing**:
- Filtered out less relevant fallacy types (intentional, equivocation, fallacy of logic)
- Applied upsampling to balance minority classes
- Text cleaning: lowercase conversion, special character removal, whitespace normalization

---

## Model 1: Random Forest Classifier

### Configuration
- **Algorithm**: Random Forest with TF-IDF Vectorization
- **Vectorizer**: TfidfVectorizer (max_features=5000, stop_words='english')
- **Classifier**: RandomForestClassifier (n_estimators=100, random_state=42)

### Performance on Validation Set

**Overall Accuracy**: 83.0%

| Fallacy Type              | Precision | Recall | F1-Score | Support |
|---------------------------|-----------|--------|----------|---------|
| Ad Hominem                | 0.81      | 0.81   | 0.81     | 42      |
| Ad Populum                | 0.83      | 0.89   | 0.86     | 44      |
| Appeal to Emotion         | 0.87      | 0.79   | 0.83     | 33      |
| Circular Reasoning        | 0.82      | 0.91   | 0.86     | 55      |
| Fallacy of Credibility    | 0.79      | 0.82   | 0.81     | 38      |
| Fallacy of Extension      | 0.92      | 0.83   | 0.87     | 29      |
| Fallacy of Relevance      | 0.87      | 0.90   | 0.89     | 30      |
| False Causality           | 0.79      | 0.77   | 0.78     | 43      |
| False Dilemma             | 0.85      | 0.91   | 0.88     | 45      |
| Faulty Generalization     | 0.80      | 0.67   | 0.73     | 42      |
| **Macro Average**         | **0.84**  | **0.83** | **0.83** | 401     |
| **Weighted Average**      | **0.83**  | **0.83** | **0.83** | 401     |

### Key Strengths
✅ **Balanced Performance**: All fallacy types achieve >67% recall  
✅ **High Precision**: Precision ranges from 79-92% across categories  
✅ **No Class Bias**: Model successfully identifies all 10 fallacy types  
✅ **Consistent Results**: Macro and weighted averages align closely at 83%

### Best Performing Categories
1. **Fallacy of Extension**: 92% precision, 87% F1-score
2. **Fallacy of Relevance**: 89% F1-score
3. **False Dilemma**: 88% F1-score

### Weakest Category
- **Faulty Generalization**: 67% recall (still respectable)

---

## Model 2: Large Language Model (3B Parameters)

### Configuration
- **Model**: meta.llama-3-2-3b-instruct (3 billion parameters)
- **API**: Dartmouth-hosted ChatDartmouth wrapper
- **Prompt Strategy**: Zero-shot classification with explicit instruction
- **Prompt**: 
  ```
  Instruction: Read the statement and classify it as one of the following:
  ["ad hominem", "ad populum", "appeal to emotion", "circular reasoning", 
   "fallacy of credibility", "fallacy of extension", "fallacy of relevance", 
   "false causality", "false dilemma", or "faulty generalization"].

  Return *ONLY* the fallacy label without explanation.

  Statement: "{statement}"

  Fallacy:
  ```

### Performance on Validation Set

**Overall Accuracy**: 16.5%

| Fallacy Type              | Precision | Recall | F1-Score | Support |
|---------------------------|-----------|--------|----------|---------|
| None                      | 0.00      | 0.00   | 0.00     | 0       |
| Ad Hominem                | 0.47      | 0.19   | 0.27     | 42      |
| Ad Populum                | 1.00      | 0.02   | 0.04     | 44      |
| Appeal to Emotion         | 0.33      | 0.12   | 0.18     | 33      |
| Circular Reasoning        | 0.00      | 0.00   | 0.00     | 55      |
| Fallacy of Credibility    | 0.50      | 0.03   | 0.05     | 38      |
| Fallacy of Extension      | 0.00      | 0.00   | 0.00     | 29      |
| Fallacy of Relevance      | 0.07      | 0.10   | 0.08     | 30      |
| False Causality           | 0.69      | 0.26   | 0.37     | 43      |
| False Dilemma             | 0.14      | 0.84   | 0.24     | 45      |
| Faulty Generalization     | 0.00      | 0.00   | 0.00     | 42      |
| **Macro Average**         | **0.29**  | **0.14** | **0.11** | 401     |
| **Weighted Average**      | **0.33**  | **0.16** | **0.13** | 401     |

### Critical Issues
❌ **Extreme Class Bias**: 84% of predictions are "false dilemma"  
❌ **Zero Recall on 3 Categories**: Circular Reasoning, Fallacy of Extension, Faulty Generalization  
❌ **Very Low Recall**: Most categories have <20% recall  
❌ **Precision-Recall Imbalance**: High precision (100%) on Ad Populum but only 2% recall

### Pattern Analysis
- **False Dilemma Bias**: The model incorrectly classifies most statements as false dilemma (84% recall but only 14% precision)
- **Overly Conservative**: Nearly perfect precision (100%) on Ad Populum indicates the model only predicts it when extremely confident, missing most actual cases
- **Best Performance**: False Causality (69% precision, 26% recall) - still far below Random Forest

---

## Comparative Analysis

### Performance Gap

| Metric                    | Random Forest | LLM (3B) | Difference |
|---------------------------|---------------|----------|------------|
| **Accuracy**              | 83.0%         | 16.5%    | **+66.5%** |
| **Macro Avg Precision**   | 84%           | 29%      | **+55%**   |
| **Macro Avg Recall**      | 83%           | 14%      | **+69%**   |
| **Macro Avg F1-Score**    | 83%           | 11%      | **+72%**   |

**Conclusion**: The Random Forest classifier outperforms the 3B LLM by a factor of **5x** in accuracy.

### Why Random Forest Wins

1. **Pattern Recognition**: TF-IDF effectively captures linguistic patterns and word associations specific to each fallacy type
2. **Training Data Efficiency**: RF leverages 2,807 labeled examples to learn statistical patterns
3. **Task-Specific Optimization**: The model is specifically trained for this exact classification task
4. **No Reasoning Required**: Fallacies often have telltale linguistic markers that don't require deep logical reasoning

### Why the LLM Struggles

1. **Model Size Limitation**: 3B parameters is insufficient for nuanced logical reasoning
2. **Zero-Shot Learning**: No examples provided in the prompt to guide classification
3. **Complex Task**: Fallacy detection requires understanding context, argument structure, and logical relationships
4. **Overconfidence in One Category**: Model latches onto "false dilemma" pattern and overapplies it

---

## Key Insights

### 1. Traditional ML Can Outperform Small LLMs
For specialized classification tasks with labeled training data, traditional machine learning approaches (Random Forest + TF-IDF) can significantly outperform smaller language models.

### 2. Feature Engineering Matters
TF-IDF vectorization with appropriate feature limits (5,000 features) provides excellent signal for fallacy detection, capturing word importance and frequency patterns.

### 3. Model Selection is Critical
- **Use Random Forest when**: You have labeled training data and need reliable, consistent classification
- **Consider larger LLMs when**: You need reasoning capabilities, have limited training data, or require zero-shot performance

### 4. Class Balance After Upsampling
Despite upsampling minority classes, the Random Forest maintained balanced performance across all categories, suggesting the model learned genuine patterns rather than overfitting.

### 5. Small LLM Limitations
3B parameter models lack the reasoning capacity for complex logical tasks. Larger models (70B+) or specialized fine-tuned models may be necessary for competitive LLM performance.

---

## Application to Presidential Debates

The Random Forest classifier was applied to 43 presidential debate transcripts (1960-2020), containing 8,139 individual statements from various candidates.

**Output**: `debate_fallacy_predictions_filtered.csv`
- Contains predicted fallacy types for each debate statement
- Includes confidence scores for each prediction
- Enables analysis of fallacy usage patterns across:
  - Different candidates
  - Time periods
  - Debate topics

**Key Analysis Capabilities**:
- Fallacy frequency by speaker
- Historical trends in debate argumentation
- Comparison across political eras
- Most common fallacy types in political discourse

---

## Recommendations

### For This Project
1. ✅ **Use Random Forest for debate analysis** - Proven 83% accuracy makes it the reliable choice
2. 🔄 **Optional**: Test larger LLMs (70B+ parameters) to see if model scale closes the performance gap
3. 📊 **Focus on RF results** for academic paper and final presentation

### For Future Work
1. **Fine-tune LLMs**: Train a smaller model specifically on fallacy detection data
2. **Few-shot Prompting**: Provide examples of each fallacy type in the LLM prompt
3. **Ensemble Methods**: Combine RF and LLM predictions for potentially better performance
4. **Expand Dataset**: Include more debate-specific training data to improve real-world performance

### Prompt Engineering for LLMs
If testing larger models, consider:
- Adding 1-2 examples per fallacy type (few-shot learning)
- Including definitions of each fallacy
- Requesting step-by-step reasoning before classification
- Using chain-of-thought prompting

---

## Technical Specifications

### Environment
- **Python**: 3.13
- **Key Libraries**: 
  - scikit-learn (Random Forest, TF-IDF)
  - pandas (data manipulation)
  - langchain-dartmouth (LLM integration)
  - datasets (Hugging Face integration)

### Reproducibility
- Random seed: 42 (for all train/test splits and RF initialization)
- All hyperparameters documented in notebook
- Dataset publicly available on Hugging Face

### Computational Requirements
- **Random Forest Training**: <1 minute on standard laptop
- **LLM Inference**: ~2-3 seconds per statement (API-dependent)
- **Debate Analysis**: ~10 minutes for 8,139 statements (RF)

---

## Conclusion

This analysis demonstrates that traditional machine learning methods remain highly competitive for specialized classification tasks, even in the era of large language models. The Random Forest classifier's 83% accuracy, balanced performance across all fallacy types, and efficient computational requirements make it the superior choice for this fallacy detection application.

The stark contrast with the 3B parameter LLM's 16.5% accuracy highlights the importance of:
1. Matching model capabilities to task requirements
2. Leveraging labeled training data when available
3. Understanding the limitations of smaller language models for complex reasoning tasks

For the presidential debate analysis, the Random Forest classifier provides reliable, interpretable results that can inform understanding of argumentation patterns in American political discourse from 1960 to 2020.

---

## References

- **Dataset**: [tasksource/logical-fallacy](https://huggingface.co/datasets/tasksource/logical-fallacy)
- **Course**: Dartmouth COSC 072 - Machine Learning & Statistical Data Analysis
- **Instructor**: Professor Sarah Masud Preum
- **Code Repository**: [RodillasJavier/debate-fallacy-detector](https://github.com/RodillasJavier/debate-fallacy-detector)
