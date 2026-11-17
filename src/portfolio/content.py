"""Structured, editable content. Verify every public professional claim before launch."""

PROFILE = {
    "brand": "Lex",
    "name": "Alex Carvalho",
    "full_name": "Alex de Castro Carvalho",
    "eyebrow": "BIOPHYSICS  ·  SCIENTIFIC COMPUTING  ·  ENGINEERING  ·  R&D",
    "headline": "Scientific thinking.",
    "headline_accent": "Engineering execution.",
    "tagline": "Biophysicist by training, programmer by choice, curious by nature.",
    "intro": (
        "I work across biomedical science, scientific computing, data science, "
        "and software engineering, from exploring complex questions to building "
        "reliable technical solutions."
    ),
    "about": (
        "I'm Alex de Castro Carvalho, a physicist working across scientific "
        "research, software engineering, and technical leadership. "
        "I care about clarity, reproducibility, and tools people can trust."
    ),
    "experience_intro": (
        "My experience connects academic research, applied data science, "
        "and the development of software tools and platforms."
    ),
    "research_intro": (
        "My scientific background includes published research involving machine "
        "learning and work in scientific computing. Publication details will be "
        "added after verification."
    ),
    "projects_intro": (
        "A selection of computational and engineering work. "
        "Public project details and links will be added as they're reviewed."
    ),
    "contact_intro": (
        "Interested in scientific R&D, medical technology, and building useful "
        "software. I'm open to conversations with researchers and engineering teams."
    ),
    "github_url": "https://github.com/LexC",
}

NAVIGATION = (
    ("About", "about"),
    ("Experience", "experience"),
    ("Research", "research"),
    ("Projects", "projects"),
    ("Contact", "contact"),
)

RESEARCH = {
    "kicker": "SCIENTIFIC FOUNDATION",
    "headline": "Questions worth investigating.",
    "description": "Scientific computing, biomedical research, statistical methods, and machine learning.",
    "note": "Publication bibliography coming after review.",
}


def validate_content():
    """Fail early on missing copy or invalid navigation."""
    required = {"brand", "name", "full_name", "eyebrow", "headline", "headline_accent",
                "tagline", "intro", "about", "experience_intro", "research_intro",
                "projects_intro", "contact_intro", "github_url"}
    for key in required:
        if not isinstance(PROFILE.get(key), str) or not PROFILE[key].strip():
            raise ValueError(f"Missing profile content: {key}")
    targets = [target for _, target in NAVIGATION]
    if len(set(targets)) != len(targets) or set(targets) != {"about", "experience", "research", "projects", "contact"}:
        raise ValueError("Navigation must reference each homepage section exactly once")
    from urllib.parse import urlsplit
    url = urlsplit(PROFILE["github_url"])
    if url.scheme != "https" or not url.netloc:
        raise ValueError("github_url must be an absolute HTTPS URL")

EXPERTISE = (
    ("Biomedical science", "science"),
    ("Software engineering", "code"),
    ("Data science", "data"),
    ("Machine learning", "ml"),
    ("Technical leadership", "lead"),
)

EXPERIENCE = (
    {
        "title": "Research & computational science",
        "detail": "Biomedical physics, mathematical modeling, and scientific methods.",
    },
    {
        "title": "Data & software development",
        "detail": "Python workflows, statistical analysis, automation, and engineering.",
    },
    {
        "title": "Technical leadership",
        "detail": "Architecture, backend development, technical decisions, and code review.",
    },
)

PROJECTS = (
    {
        "number": "01",
        "name": "Software platforms",
        "detail": "Architecture, backend engineering, and maintainable systems.",
        "icon": "⌘",
    },
    {
        "number": "02",
        "name": "Scientific computing",
        "detail": "Numerical methods, modeling, and computational tools.",
        "icon": "∿",
    },
    {
        "number": "03",
        "name": "Data & automation",
        "detail": "Reproducible data workflows and reliable automation.",
        "icon": "◇",
    },
)
