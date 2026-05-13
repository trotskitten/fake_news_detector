# Deployment Guide

This guide explains how to put the Streamlit fake news headline classifier online.

## Files Required

Your repository should contain these files in the project root:

```text
app.py
requirements.txt
README.md
.gitignore
```

Optional but recommended:

```text
DEPLOYMENT.md
```

## Test Locally First

Install dependencies and run the app locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Push to GitHub

Create a new GitHub repository, then run:

```bash
git init
git add .
git commit -m "Add fake news headline classifier app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your real GitHub username and repository name.

## Deploy on Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Sign in with GitHub.
3. Create a new app.
4. Select the GitHub repository that contains this project.
5. Select the branch, usually `main`.
6. Set the main file path to:

```text
app.py
```

7. Deploy the app.

No secrets are needed because the Hugging Face model is public.

## Deploy on Hugging Face Spaces

1. Go to Hugging Face Spaces.
2. Create a new Space.
3. Choose `Streamlit` as the SDK.
4. Upload or push these files:

```text
app.py
requirements.txt
README.md
.gitignore
```

5. Make sure the Space app file is:

```text
app.py
```

6. Hugging Face Spaces will install dependencies from `requirements.txt` and launch the app.

The README already includes Hugging Face Spaces metadata:

```yaml
sdk: streamlit
app_file: app.py
```

## Important Notes

- First startup can take a few minutes because the platform installs dependencies and downloads the model.
- The app loads this public Hugging Face model:

```text
Trotskitten/fake_news_detector
```

- The app does not need an API key or Hugging Face token unless the model is made private later.
- If deployment fails, check that `requirements.txt` is in the repository root.
- If Streamlit cannot find the app, check that the main file path is exactly `app.py`.
