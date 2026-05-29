import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import SUPPORTED_PROVIDERS, Chain
from portfolio import Portfolio
from utils import clean_text

DEFAULT_COMPANY_DESCRIPTION = (
    "An AI and software consulting company that helps businesses integrate automated tools, "
    "scale operations, optimize processes, and improve efficiency through tailored solutions."
)


def render_api_sidebar():
    st.sidebar.header("API configuration")
    provider = st.sidebar.selectbox(
        "Provider",
        options=list(SUPPORTED_PROVIDERS.keys()),
        format_func=lambda p: SUPPORTED_PROVIDERS[p]["label"],
    )
    config = SUPPORTED_PROVIDERS[provider]
    st.sidebar.caption(f"Get a free API key from [{config['label']}]({config['key_url']}).")
    api_key = st.sidebar.text_input(
        f"{config['label']} API key",
        type="password",
        help="Your key stays in this session and is not stored on the server.",
    )
    model_name = st.sidebar.text_input("Model", value=config["default_model"])
    return provider, api_key, model_name


def render_sender_form():
    st.sidebar.header("Your details")
    sender_name = st.sidebar.text_input("Your name", value="Alex")
    company_name = st.sidebar.text_input("Company name", value="Your Company")
    company_description = st.sidebar.text_area(
        "Company description",
        value=DEFAULT_COMPANY_DESCRIPTION,
        height=120,
    )
    return sender_name, company_name, company_description


def create_streamlit_app():
    st.set_page_config(
        layout="wide",
        page_title="Cold Mail Generator",
        page_icon="📧",
    )
    st.title("Cold Mail Generator")
    st.caption(
        "Paste a job posting URL, match skills to your portfolio, and generate a personalized cold email."
    )

    provider, api_key, model_name = render_api_sidebar()
    sender_name, company_name, company_description = render_sender_form()

    url_input = st.text_input(
        "Job posting URL",
        placeholder="https://example.com/careers/software-engineer",
    )
    submit_button = st.button("Generate email", type="primary")

    if not submit_button:
        return

    if not api_key:
        st.error("Enter your API key in the sidebar to continue.")
        return

    if not url_input.strip():
        st.error("Enter a job posting URL.")
        return

    try:
        with st.spinner("Loading job page and generating email..."):
            loader = WebBaseLoader([url_input.strip()])
            data = clean_text(loader.load().pop().page_content)
            chain = Chain(api_key=api_key, provider=provider, model_name=model_name)
            portfolio = Portfolio()
            portfolio.load_portfolio()
            jobs = chain.extract_jobs(data)
            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = chain.write_mail(
                    job,
                    links,
                    sender_name=sender_name,
                    company_name=company_name,
                    company_description=company_description,
                )
                st.subheader(job.get("role", "Generated email"))
                st.code(email, language="markdown")
    except Exception as e:
        st.error(f"Something went wrong: {e}")


if __name__ == "__main__":
    create_streamlit_app()
