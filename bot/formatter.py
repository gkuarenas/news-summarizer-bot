import re


def escape(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+=|{}.!-])', r'\\\1', text)


def format_section(source_label: str, articles: list[dict]) -> str:
    sections = []
    for a in articles:
        section = f"*{escape(a['title'])}*\n{escape(a['summary'])}\n[Read more]({a['url']})"
        sections.append(section)
    return f"*{escape(source_label)}*" + "\n\n" + "\n\n".join(sections)