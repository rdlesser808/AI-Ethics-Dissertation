# MSC in AI and Ethics Dissertation
A Machine Learning Approach for Detecting Propaganda in News Articles with Case Study on Israel-Palestine Coverage

## Project Overview

This repository contains the code and analysis for my Master's dissertation: **"A Machine Learning Approach for Detecting Propaganda in News Articles with Case Study on Israel-Palestine Coverage"** - completed as part of my MS in Artificial Intelligence and Ethics at Northeastern University London.

## Project Goals

- Develop automated propaganda detection models for news articles using machine learning
- Compare CNN and CRF architectures for propaganda classification
- Deploy models on real-world news coverage to analyze propaganda patterns
- Create accessible tools for media literacy and critical news consumption

## Methodology

### Models Developed
- **Convolutional Neural Network (CNN)** for sentence-level propaganda detection
- **Conditional Random Field (CRF)** for both sentence-level and fragment-level classification
- Two-step classification: identify propaganda sentences → extract specific propaganda techniques

### Technical Stack
- **Languages**: Python
- **ML Libraries**: TensorFlow, Scikit-learn, NLTK
- **NLP Tools**: BERT tokenization, RoBERTa embeddings
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: Custom scrapers using BeautifulSoup for BBC and The Guardian

### Dataset
- SemEval-2020 Task 11 corpus (536 articles, 13 propaganda techniques)
- Real-world deployment on 2,000+ articles about Israel-Palestine conflict
- Professional annotations with techniques like "Loaded Language," "Name Calling," "Appeal to Fear"
- Data sourced from https://github.com/marcogdepinto/PropagandaDetection

## Key Results

### Model Performance

- **CRF Model**: 98% accuracy on sentence-level classification after k-fold validation
- **Fragment Detection**: 86% accuracy identifying specific propaganda techniques
- **Real-time Processing**: Real-time Processing: Low computational cost suitable for browser extensions

### Performance Analysis & Validation
- The sentence-level accuracy of 98% significantly exceeds the original SemEval-2020 competition baseline (best F1-score: 51.54%), warranting further investigation to ensure model generalizability. This discrepancy suggests potential overfitting to the specific dataset characteristics. The fragment-level performance (86% accuracy) aligns more closely with expected benchmarks for this task complexity.

Key takeaways for production deployment:

- Fragment-level detection shows robust, validated performance
- Sentence-level classification requires additional testing on diverse datasets
- Model demonstrates strong potential with further refinement needed

### Model Performance
- **CRF Model**: 98% accuracy on sentence-level classification after k-fold validation
- **Fragment Detection**: 86% accuracy identifying specific propaganda techniques
- **Real-time Processing**: Low computational cost suitable for browser extensions

### News Analysis Findings
- **27% of sentences** contained propaganda techniques across BBC and Guardian articles
- **Loaded Language** was most prevalent technique (69% of identified instances)
- **Minimal difference** between Israel-Palestine relevant vs. irrelevant articles (26.9% vs 24.9%)
- **Consistent propaganda levels** across time periods and topics

## Repository Structure

```
AI-Ethics-Dissertation/
├── Article-web-scraping/
│   ├── bbc_articles.py/
│   └── guardian_articles.py/
├── Notebooks/
│   ├── CRF/BERT FINAL MODEL.ipynb
│   ├── data exploration correct.ipynb
├── Report-and-Presentation/
│   ├── RLesser Dissertation Final.pdf
│   └── RLesser Dissertation Viva.pdf
```

## Business Applications

This research has practical applications for:
- **Media literacy tools** - Browser extensions for real-time propaganda detection
- **Journalism** - Automated content analysis for editorial review
- **Social media platforms** - Content moderation and fact-checking systems
- **Academic research** - Studying media bias and information campaigns

## Skills Demonstration

This project demonstrates:
- **Technical problem-solving**: Translating complex NLP challenges into scalable ML solutions
- **Business value creation**: Potential monetary value through automated content analysis
- **Cross-functional communication**: Presenting technical findings to non-technical stakeholders
- **Real-world deployment**: Moving from research models to practical applications

## Academic Context

This work builds upon the SemEval-2020 Task 11 competition results, achieving performance comparable to top-performing systems while maintaining computational efficiency for real-world deployment.

## Ethical Considerations

- Models designed for media literacy, not censorship
- Transparent limitations and potential biases acknowledged
- Focus on empowering critical thinking rather than definitive judgments
- Careful consideration of sensitive topics like Israel-Palestine coverage

## Skills Demonstrated

- **Machine Learning**: CNN, CRF, BERT, cross-validation, hyperparameter tuning
- **Data Science**: Large-scale data processing, statistical analysis, visualization
- **Software Engineering**: Python, Git, modular code architecture
- **Research**: Literature review, experimental design, academic writing
- **Communication**: Technical documentation, stakeholder presentations

---

*This project represents the intersection of AI ethics, media literacy, and practical machine learning - demonstrating how technical solutions can address real-world information challenges while maintaining transparency and user empowerment.*

