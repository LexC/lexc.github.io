"""Structured, editable content. Verify every public professional claim before launch."""

PROFILE = {
    "brand": "Lex",
    "name": "Alex Carvalho",
    "eyebrow": "BIOPHYSICS  ·  SCIENTIFIC COMPUTING  ·  ENGINEERING  ·  R&D",
    "headline": "Scientific thinking.",
    "headline_accent": "Engineering execution.",
    "credentials": (
        "Physicist. Biomedical Researcher.",
        "Software Development Leader.",
    ),
    "python_experience": (
        "8+ years of Python experience spanning scientific computing, data science, "
        "and software engineering."
    ),
    "about": (
        "I got into physics because I wanted to understand how the world works, "
        "particularly the human brain. Scientific research taught me more than how "
        "to answer questions. It taught me how to ask the right ones, design "
        "experiments, understand complex systems, and distinguish meaningful "
        "evidence from noise.\n\n"
        "Along the way, I became fascinated by the instruments, people, and "
        "processes that make discoveries possible. Understanding how these pieces "
        "fit together made me better at extracting insights from "
        "complex data, and eventually led me to build tools that help others do "
        "the same.\n\n"
        "What started as the pleasure of finding things out grew into something "
        "equally rewarding: the satisfaction of making things work."
    ),
    "experience_intro": (
        "I see my career as four chapters, each building on the last, "
        "from scientific investigation to engineering leadership."
    ),
    "research_intro": (
        "Scientific contributions in biomedical physics, neuroimaging, "
        "and computational methods."
    ),
    "projects_intro": (
        "Selected work in software development, data analysis, and machine learning, "
        "from industry platforms to public technical projects."
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
    ("Projects", "projects"),
    ("Research", "research"),
    ("Expertise", "expertise"),
    ("Contact", "contact"),
)

RESEARCH = {
    # Replace these placeholders with verified award details when available.
    "award_name": "[Conference award name]",
    "award_details": "[Conference, year, and recognition details]",
}

PUBLICATIONS = (
    {
        "title": "Revealing the spatiotemporal requirements for accurate subject identification with resting-state functional connectivity: a simultaneous fNIRS-fMRI study",
        "journal": "Neurophotonics",
        "year": "2023",
        "url": "https://doi.org/10.1117/1.NPh.10.1.013510",
    },
    {
        "title": "Development of novel methods to investigate the brain at rest",
        "journal": "Revista Brasileira de Física Médica",
        "year": "2017",
        "url": "https://doi.org/10.29384/rbfm.2017.v11.n3.p33",
    },
)

CONTACT = {
    "email": "18586901+LexC@users.noreply.github.com",
    "linkedin_url": "https://www.linkedin.com/in/alexccrv",
    "location": "Netherlands",
    "relocation": "Open to relocation",
}


def validate_content():
    """Fail early on missing copy or invalid navigation."""
    required = {"brand", "name", "eyebrow", "headline", "headline_accent",
                "python_experience", "about", "experience_intro", "research_intro",
                "projects_intro", "contact_intro", "github_url"}
    for key in required:
        if not isinstance(PROFILE.get(key), str) or not PROFILE[key].strip():
            raise ValueError(f"Missing profile content: {key}")
    credentials = PROFILE.get("credentials")
    if not isinstance(credentials, tuple) or not credentials or not all(
        isinstance(role, str) and role.strip() for role in credentials
    ):
        raise ValueError("Missing profile content: credentials")
    targets = [target for _, target in NAVIGATION]
    if targets != ["about", "experience", "projects", "research", "expertise", "contact"]:
        raise ValueError("Navigation must reference all six homepage sections in order")
    from urllib.parse import urlsplit
    url = urlsplit(PROFILE["github_url"])
    if url.scheme != "https" or not url.netloc:
        raise ValueError("github_url must be an absolute HTTPS URL")

EXPERTISE = (
    ("Curiosity", "telescope"),
    ("Systems Thinking", "network"),
    ("Biomedical Research", "brain"),
    ("Scientific Computing & Data", "data"),
    ("Software Engineering", "code"),
    ("Technical Leadership", "users"),
)

EXPERIENCE = (
    {
        "title": "The Scientist",
        "icon": "microscope",
        "period": "2014 – 2020",
        "organization": "Institute of Physics, University of Campinas",
        "detail": "Conducted experimental neuroimaging research, developing scientific methods, processing physiological signals, and working with fNIRS/fMRI instrumentation.",
        "current": False,
    },
    {
        "title": "The Data Scientist",
        "icon": "chart",
        "period": "2021 – 2023",
        "organization": "Faculty of Medical Sciences, University of Campinas",
        "detail": "Developed clinical research data workflows, analyzed neurological datasets, and applied statistical methods to biomedical investigations.",
        "current": False,
    },
    {
        "title": "The Mathematician",
        "icon": "sigma",
        "period": "2025",
        "organization": "Gaming Laboratories International",
        "detail": "Performed mathematical and statistical validation of complex systems, evaluated algorithms, and reviewed source code in an industrial environment.",
        "current": False,
    },
    {
        "title": "The Engineer",
        "icon": "code",
        "period": "2026 – Present",
        "organization": "Gaming Laboratories International",
        "detail": "Created a software platform supporting a 60-person department, progressing into technical leadership of its architecture, development, and contributors.",
        "current": True,
    },
)

PROJECTS = (
    {
        "name": "GOTO",
        "category": "Software Platform for Mathematical Analysis",
        "access": "Internal / Proprietary",
        "internal": True,
        "detail": "GOTO (Game Outcome Testing Optimizer) is an internal Python platform that automates and standardizes mathematical analysis and validation workflows.",
        "role_label": "My role",
        "responsibilities": "Initiated and developed the original framework, and now lead the platform's architecture, development, code reviews, releases, and contributors.",
        "keywords": ("Python", "Software Architecture", "Automation", "Technical Leadership"),
        "image": "images/projects/goto-platform.png",
        "image_width": 1535,
        "image_height": 1024,
        "image_alt": "Conceptual software platform with connected processing modules, mathematical validation, and standardized outputs.",
        "url": None,
    },
    {
        "name": "NuFlow",
        "category": "Scientific Data Analysis & Automation",
        "access": "Independent Project",
        "internal": False,
        "detail": "Independently developed a Python pipeline for statistical analysis of experimental data, automating statistical comparisons, visualizations, and Excel report generation for reproducible scientific workflows.",
        "responsibilities": None,
        "keywords": ("Python", "Scientific Computing", "Statistical Analysis", "Automation"),
        "image": "images/projects/nuflow-genomics.png",
        "image_width": 1536,
        "image_height": 1024,
        "image_alt": "Conceptual genomics visualization combining cell clusters in a UMAP-style scatterplot, a gene-expression heatmap, and expression distributions.",
        "url": "https://github.com/LexC/NuFlow",
    },
    {
        "name": "Fraud_Classifier",
        "category": "Machine Learning Classification",
        "access": "Independent Project",
        "internal": False,
        "detail": "Developed an end-to-end fraud-detection pipeline covering PostgreSQL data ingestion, feature engineering, comparison of nine classification models, hyperparameter optimization, and performance evaluation.",
        "responsibilities": None,
        "keywords": ("Python", "PostgreSQL", "scikit-learn", "LightGBM"),
        "image": "images/projects/fraud-classifier-boundary.png",
        "image_width": 1447,
        "image_height": 1087,
        "image_alt": "Conceptual machine-learning visualization with two classification groups, a nonlinear decision boundary, and confidence regions.",
        "url": "https://github.com/LexC/Fraud_Classifier",
    },
)

EXPERTISE_CATEGORIES = (
    {
        "name": "Scientific Computing",
        "detail": "Numerical analysis, scientific programming, and signal processing.",
        "keywords": ("Python", "NumPy", "SciPy", "MATLAB"),
    },
    {
        "name": "Software Engineering",
        "detail": "Python backend development, software architecture, automation, and object-oriented programming. Code review, testing, and release management.",
        "keywords": ("Python", "Git", "Testing", "Release management"),
    },
    {
        "name": "Data Science & Machine Learning",
        "detail": "Statistical analysis, data processing, classification, model evaluation, and data visualization.",
        "keywords": ("pandas", "scikit-learn", "SQL"),
    },
    {
        "name": "Biomedical Research",
        "detail": "Biomedical physics, neuroimaging, physiological signal processing, experimental design, and scientific instrumentation.",
        "keywords": ("fNIRS", "fMRI", "Experimental design"),
    },
    {
        "name": "Technical Leadership",
        "detail": "Technical decision-making, architecture ownership, contributor coordination, code reviews, technical documentation, and engineering workflows.",
        "keywords": ("Architecture ownership", "Contributor coordination"),
    },
)
