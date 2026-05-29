# Cold Mail Generator

Generate personalized cold emails from job posting URLs using LangChain, Groq, and Streamlit.

Visitors enter their own API key in the app sidebar (keys are not stored). The app scrapes a careers page, extracts job details, matches skills to your portfolio CSV, and drafts a cold email.

## Features

- Job URL scraping and structured extraction (role, experience, skills, description)
- Portfolio skill matching from your CSV (keyword overlap)
- Configurable sender name, company, and description
- Sidebar API key input for [Groq](https://console.groq.com/keys)
- Deployable on [Streamlit Community Cloud](https://streamlit.io/cloud)

## Local setup

1. Clone the repository and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) For notebook use, set `GROQ_API_KEY` in a `.env` file in the project root.

3. Run the app:

   ```bash
   streamlit run main.py
   ```

4. Open the sidebar, paste your Groq API key, enter a job URL, and click **Generate email**.

## Portfolio data

Edit `my_portfolio.csv` with your tech stacks and project links.

## Deploy on Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo, and set **Main file path** to `main.py`.
3. Python version is pinned in `runtime.txt` (`python-3.12`) so dependencies install correctly.
4. Users supply their own API keys in the app; you do not need to add secrets for Groq unless you want a default for yourself.

## Notebook

`email_generator.ipynb` walks through the same pipeline step by step for learning and experimentation.

## License

MIT — see [LICENSE](LICENSE).
