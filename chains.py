from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

SUPPORTED_PROVIDERS = {
    "groq": {
        "label": "Groq",
        "key_url": "https://console.groq.com/keys",
        "default_model": "llama-3.3-70b-versatile",
    },
}


class Chain:
    def __init__(self, api_key: str, provider: str = "groq", model_name=None):
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")
        if not api_key or not api_key.strip():
            raise ValueError("API key is required.")

        provider_config = SUPPORTED_PROVIDERS[provider]
        model = model_name or provider_config["default_model"]
        self.llm = ChatGroq(temperature=0, groq_api_key=api_key.strip(), model_name=model)

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from a careers or job posting page.
            Extract the job posting and return JSON with keys: `role`, `experience`, `skills`, `description`.
            Only return valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            parsed = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too large. Unable to parse job details.")
        return parsed if isinstance(parsed, list) else [parsed]

    def write_mail(self, job, links, sender_name: str, company_name: str, company_description: str):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {sender_name}, a business development professional at {company_name}.
            {company_name} is described as: {company_description}

            Write a professional, personalized cold email to the hiring team about the role above.
            Explain how {company_name} can help meet their needs.
            Include the most relevant portfolio links from this list: {link_list}

            Write as {sender_name} from {company_name}.
            Do not include a preamble—output only the email (subject line optional).
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke(
            {
                "job_description": str(job),
                "link_list": links,
                "sender_name": sender_name,
                "company_name": company_name,
                "company_description": company_description,
            }
        )
        return res.content
