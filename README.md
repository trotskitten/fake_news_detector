---
title: Fake News Headline Classifier
sdk: streamlit
app_file: app.py
pinned: false
---

# Fake News Headline Classifier

A deployable Streamlit web application for binary fake news headline classification using a fine-tuned Hugging Face model.

## Model

Hugging Face Hub model:

```text
Trotskitten/fake_news_detector
```

Label mapping:

```text
0 = FAKE
1 = REAL
```

The app maps `LABEL_0` to `FAKE` and `LABEL_1` to `REAL` when those labels are returned by the Transformers pipeline.

## Features

- Loads the model from Hugging Face Hub with `transformers.pipeline`
- Caches the model with `st.cache_resource`
- Classifies user-entered headlines as `FAKE` or `REAL`
- Shows the model confidence score
- Handles empty input
- Includes example headlines for quick testing
- Includes a disclaimer that predictions are based on learned headline patterns, not verified factual truth

## Run Locally

Create a virtual environment, install dependencies, and start Streamlit.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Deploy

This app can be deployed on Streamlit Community Cloud or Hugging Face Spaces.

For a standalone deployment checklist, see [DEPLOYMENT.md](DEPLOYMENT.md).

### 1. Push the project to GitHub

Create a GitHub repository and push these files:

```text
app.py
requirements.txt
README.md
.gitignore
```

Example git commands:

```bash
git init
git add .
git commit -m "Add fake news headline classifier app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

### 2. Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud.
2. Create a new app.
3. Select the GitHub repository that contains this project.
4. Select the branch, usually `main`.
5. Set the main file path to `app.py`.
6. Deploy the app.

No secret keys are required because the model is loaded from the public Hugging Face Hub.

### 3. Deploy on Hugging Face Spaces

1. Create a new Space with the Streamlit SDK.
2. Upload or push `app.py`, `requirements.txt`, `README.md`, and `.gitignore`.
3. Make sure the Space SDK is set to `streamlit`.
4. Make sure the app file is set to `app.py`.
5. The Space will install dependencies from `requirements.txt` and run the app.

The metadata at the top of this README is included for Hugging Face Spaces:

```yaml
sdk: streamlit
app_file: app.py
```

## Troubleshooting

- First startup can take a few minutes because dependencies and the model are downloaded.
- If deployment fails during installation, check that `requirements.txt` is present in the repository root.
- If the model cannot be loaded, confirm that `Trotskitten/fake_news_detector` is still public on Hugging Face Hub.
- If Streamlit cannot find the app, confirm that the main file path is `app.py`.

## Disclaimer

This model predicts based on patterns learned during training. It does not verify whether a headline is factually true, whether sources are reliable, or whether a claim reflects current events.
