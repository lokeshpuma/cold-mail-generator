import re
from pathlib import Path

import pandas as pd


def _tokenize(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[a-zA-Z0-9+#.]+", text) if len(w) > 2}


class Portfolio:
    def __init__(self, file_path: str = "my_portfolio.csv"):
        path = Path(file_path)
        if not path.is_file():
            path = Path(__file__).resolve().parent / file_path
        self.data = pd.read_csv(path)
        self._rows = [
            {
                "techstack": str(row["Techstack"]),
                "link": row["Links"],
                "tokens": _tokenize(str(row["Techstack"])),
            }
            for _, row in self.data.iterrows()
        ]

    def load_portfolio(self):
        """No-op kept for compatibility with the Streamlit app flow."""
        return None

    def query_links(self, skills):
        if isinstance(skills, str):
            skills = [skills]

        results = []
        for skill in skills:
            skill_tokens = _tokenize(str(skill))
            scored = []
            for row in self._rows:
                overlap = len(skill_tokens & row["tokens"])
                if overlap == 0:
                    tech_lower = row["techstack"].lower()
                    skill_lower = str(skill).lower()
                    if any(term in tech_lower for term in skill_lower.split() if len(term) > 3):
                        overlap = 1
                scored.append((overlap, row["link"]))

            scored.sort(key=lambda x: x[0], reverse=True)
            top_links = []
            seen = set()
            for score, link in scored:
                if score <= 0 and top_links:
                    break
                if link in seen:
                    continue
                seen.add(link)
                top_links.append({"links": link})
                if len(top_links) >= 2:
                    break

            if len(top_links) < 2:
                for _, link in scored:
                    if link in seen:
                        continue
                    seen.add(link)
                    top_links.append({"links": link})
                    if len(top_links) >= 2:
                        break

            results.append(top_links)

        return results
