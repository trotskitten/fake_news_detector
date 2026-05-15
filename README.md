---
title: Fake News Headline Classifier
sdk: streamlit
app_file: app.py
pinned: false
---

# Fake News Headline Classifier

This project started as an NLP modeling workflow and ended as a deployable Streamlit app. The goal was to take a raw collection of news headlines, build a reliable fake-news headline classifier, compare several modeling approaches, and expose the best result through a simple interface that anyone can test.

The final app classifies a news-style headline as `FAKE` or `REAL` using a fine-tuned Hugging Face Transformer model.

## Live App

Try the deployed Streamlit app [here](https://strangerstrings.streamlit.app/).

## Project Story

The first step was preparing the text data. In `01_Data_Preprocessing.ipynb`, the raw headlines were loaded, checked, cleaned, normalized, and transformed into datasets that could be used consistently across experiments. This created the foundation for the rest of the project: a training dataset, a testing dataset, and reusable processed text.

After preprocessing, the project moved through a set of classic machine learning baselines in `02_Classic_ML_Classification.ipynb`. Logistic Regression, Support Vector Machines, and Random Forest models were tested with Bag-of-Words and TF-IDF features. These experiments helped establish a performance baseline and showed how far traditional NLP features could go before moving to more contextual representations.

The next stage, `03_sentence_embedding_svc.ipynb`, tested sentence embeddings with a linear SVC classifier. Instead of representing headlines only as word counts, each headline was converted into a dense semantic vector with a SentenceTransformer model. This step explored whether pretrained sentence-level representations could improve the classifier while keeping the downstream model relatively lightweight.

The final modeling stage was Transformer fine-tuning in `04_distilbert_FineTuning.ipynb`. At this point, the project moved from external feature representations to a model that could learn directly from tokenized headline text. The base model was `distilbert/distilbert-base-uncased`, a lighter version of BERT that keeps strong language understanding while being faster and easier to deploy.

The cleaned training data was split into training and validation sets with stratification, so both classes stayed balanced during evaluation. Headlines were tokenized with a maximum length of 128 tokens, then passed into `AutoModelForSequenceClassification` with two output labels: `FAKE` and `REAL`. Training was handled with the Hugging Face `Trainer`, using a learning rate of `2e-5`, batch size `8`, two training epochs, weight decay, and periodic validation checks.

Model selection focused on validation F1 score rather than accuracy alone, because the project needed a classifier that balanced false positives and false negatives. During training, validation accuracy and F1 rose quickly and stabilized around `0.986-0.987`, with a short temporary dip before recovering in the later training steps. The final validation report showed strong and balanced performance across both classes:

| Class | Precision | Recall | F1-score | Support |
| --- | ---: | ---: | ---: | ---: |
| FAKE | 0.9906 | 0.9849 | 0.9877 | 3,515 |
| REAL | 0.9841 | 0.9900 | 0.9871 | 3,316 |
| Accuracy |  |  | 0.9874 | 6,831 |
| Macro avg | 0.9873 | 0.9875 | 0.9874 | 6,831 |
| Weighted avg | 0.9874 | 0.9874 | 0.9874 | 6,831 |

The confusion matrix also showed that the errors were limited and fairly balanced: `53` fake headlines were predicted as real, while `33` real headlines were predicted as fake. After validation, the notebook used the trained model to create `BERT_predictions.csv` for the test headlines. Once the model was validated, it was prepared for Hugging Face Hub upload so the Streamlit app could load it directly without storing model weights in the GitHub repository.

The last step was turning the notebook workflow into an interactive app. `app.py` loads the fine-tuned Hugging Face model, accepts a headline from the user, runs the prediction, and displays both the predicted label and confidence score. The app is intentionally simple: it focuses on making the model easy to test without exposing notebook complexity.

## Final Model

The Streamlit app loads this public Hugging Face model:

```text
Trotskitten/fake_news_detector
```

Label mapping:

```text
0 = FAKE
1 = REAL
```

The app also maps Hugging Face pipeline labels such as `LABEL_0` and `LABEL_1` to the project labels.

## What The App Does

- Accepts one news-style headline from the user
- Loads the model from Hugging Face Hub with `transformers.pipeline`
- Caches the model with `st.cache_resource`
- Predicts whether the headline is `FAKE` or `REAL`
- Shows the model confidence score
- Provides example headlines for quick testing
- Reminds users that the prediction is not a factual verification

## Repository Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- datasets/
|   |-- training_data.csv
|   |-- testing_data.csv
|   `-- BERT_predictions.csv
`-- notebooks/
    |-- 01_Data_Preprocessing.ipynb
    |-- 02_Classic_ML_Classification.ipynb
    |-- 03_sentence_embedding_svc.ipynb
    `-- 04_distilbert_FineTuning.ipynb
```

## Data And Outputs

The repository includes the project data files so the development path can be reviewed alongside the app.

- `datasets/training_data.csv`: training data used during model development
- `datasets/testing_data.csv`: testing headlines used for final prediction
- `datasets/BERT_predictions.csv`: predictions generated by the BERT model for the testing data

Before publishing or reusing the data outside this project, confirm that the original dataset license allows redistribution.

## Run Locally

Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies and start the Streamlit app.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes And Limitations

This classifier predicts from patterns learned in headline text. It does not verify facts, check sources, evaluate article content, or determine whether a claim is currently true.

If local prediction fails with `CERTIFICATE_VERIFY_FAILED` on Windows, the issue is usually the local Python certificate store rather than the app code. Updating Python/certificates or retrying from a clean virtual environment should resolve it.

## Contributors

- [Jan-Sael](https://github.com/Jan-Sael)
- [gkahl-sudo](https://github.com/gkahl-sudo)
