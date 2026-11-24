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
    ("Expertise", "expertise"),
    ("Projects", "projects"),
    ("Research", "research"),
    ("Contact", "contact"),
)

RESEARCH = {
    "paragraphs": (
        "My research at the University of Campinas (UNICAMP) encompassed experimental "
        "biophysics, biomedical optics, and neuroscience, with emphasis on cerebral "
        "neurovascular coupling, hemodynamics, and functional brain networks. I designed "
        "and conducted multimodal neuroimaging experiments using functional near-infrared "
        "spectroscopy (fNIRS) and functional magnetic resonance imaging (fMRI), operating "
        "NIRScout instrumentation and 3 T MRI systems, developing acquisition protocols, "
        "and engineering custom MRI-compatible hardware through CAD modeling, 3D "
        "printing, and experimental prototyping. I served as a technical reference for "
        "fMRI acquisition and processing, supervised experimental activities, and trained "
        "master's and doctoral researchers.",
        "My computational research focused on multidimensional biomedical signal and "
        "image processing, developing scientific software and analytical methodologies "
        "in MATLAB and Python. These incorporated wavelet and spline-based artifact "
        "correction, principal component analysis, nuisance regression, spatial "
        "normalization, temporal filtering, and hemoglobin concentration estimation. "
        "I investigated resting-state functional connectivity and neurological disorders "
        "through regional time-series analysis, correlation matrices, and brain network "
        "characterization, contributing to published research involving spectral analysis, "
        "graph theory, complex systems, Riemannian geometry, pattern recognition, and "
        "machine learning.",
        "Within clinical neuroscience, I investigated the neurological and neuropsychiatric "
        "sequelae of COVID-19, developing computational infrastructure for large-scale "
        "clinical research, including clinical database development, data curation, quality "
        "control, biostatistical analysis, and temporal characterization of persistent "
        "symptoms. My responsibilities extended to research coordination, methodological "
        "development, scientific interpretation, and communication of results. These "
        "scientific investigations resulted in multiple publications and scientific awards, "
        "including recognition for first-author research.",
    ),
    "distinctions": (
        {
            "title": "Best Scientific Work Award",
            "role": "First Author & Oral Presenter",
            "event": "XXIX Brazilian Congress of Neurology",
            "year": "2021",
            "work": "Persistent neurological symptoms after mild infection with COVID-19: analysis of 6,989 individuals",
        },
        {
            "title": "Best Scientific Work Award",
            "role": "Coauthor",
            "event": "XXIX Brazilian Congress of Neurology",
            "year": "2021",
            "work": None,
        },
        {
            "title": "Award-Winning Doctoral Oral Presentation",
            "role": "Coauthor",
            "event": "8th BRAINN Congress",
            "year": "2022",
            "work": None,
        },
    ),
    "metrics": (
        ("4", "Scientific Research Papers"),
        ("7", "Scientific Conference Contributions"),
        ("4", "First-Author Contributions"),
    ),
}

PUBLICATIONS = (
    {
        "title": "Graph Analysis of Age-Related Changes in Resting-State Functional Connectivity Measured with fNIRS",
        "journal": "Journal of Ageing and Longevity",
        "year": "2026",
        "image": "jal-06-00011-g003.png",
        "image_width": 4271,
        "image_height": 3616,
        "image_fit": "cover",
        "image_alt": "Cortical maps of resting-state functional brain networks across age groups and hemoglobin signals.",
        "authors_before": "Sánchez, V., Novi, S., ",
        "author": "Carvalho, A. C.",
        "keywords": ("Graph Theory", "Complex Networks", "Spectral Analysis", "Biomedical Optics", "Statistical Analysis"),
        "url": "https://doi.org/10.3390/jal6010011",
    },
    {
        "title": "Revealing the spatiotemporal requirements for accurate subject identification with resting-state functional connectivity: a simultaneous fNIRS-fMRI study",
        "journal": "Neurophotonics",
        "year": "2023",
        "image": "NPh_10_1_013510_f001.png",
        "image_width": 1245,
        "image_height": 602,
        "image_fit": "contain",
        "image_alt": "Frontal and lateral brain views showing the fNIRS optical probe configuration, with red sources, blue detectors, and yellow channels.",
        "authors_before": "Novi, S. L., ",
        "author": "Carvalho, A. C.",
        "keywords": ("Machine Learning", "Pattern Recognition", "Biomedical Signal Processing", "Multimodal Neuroimaging", "Riemannian Geometry"),
        "url": "https://doi.org/10.1117/1.NPh.10.1.013510",
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
    if targets != ["about", "experience", "expertise", "projects", "research", "contact"]:
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
        "name": "Software Engineering",
        "icon": "code",
        "detail": "Reliable software platforms and automation for scientific and engineering applications.",
        "keywords": (
            "Python", "Java", "Software Architecture", "Backend Development",
            "Object-Oriented Programming (OOP)", "Software Testing", "Test Automation",
            "Git", "Docker", "Linux",
        ),
    },
    {
        "name": "Scientific Computing",
        "icon": "processor",
        "detail": "Computational algorithms for scientific modeling, signal processing, and image analysis.",
        "keywords": (
            "Python", "MATLAB", "NumPy", "SciPy", "Algorithm Development",
            "Numerical Analysis", "Digital Signal Processing (DSP)", "Image Processing",
            "Data Visualization", "Scientific Programming",
        ),
    },
    {
        "name": "Experimental & Biomedical R&D",
        "icon": "microscope",
        "detail": "Biomedical instrumentation, experimental methodology, neuroimaging, and hardware prototyping.",
        "keywords": (
            "Biomedical Optics", "Medical Imaging", "Neuroimaging",
            "Biomedical Instrumentation", "Experimental Design", "Clinical Research",
            "fMRI", "fNIRS", "LabVIEW", "Rapid Prototyping",
        ),
    },
    {
        "name": "Data Science & Machine Learning",
        "icon": "chart",
        "detail": "Predictive modeling and reproducible data pipelines for scientific applications.",
        "keywords": (
            "Python", "SQL", "Machine Learning", "scikit-learn", "pandas",
            "Data Engineering", "ETL", "Statistical Modeling", "Predictive Modeling",
            "Data Pipelines",
        ),
    },
    {
        "name": "Applied Mathematics",
        "icon": "sigma",
        "detail": "Mathematical modeling, algorithm verification, and quantitative validation of complex systems.",
        "keywords": (
            "Mathematical Modeling", "Statistical Analysis", "Probability Theory",
            "Hypothesis Testing", "Regression Analysis", "Graph Theory", "Spectral Analysis",
            "Mathematical Analysis", "Algorithm Validation", "Verification & Validation (V&V)",
        ),
    },
    {
        "name": "Technical Leadership",
        "icon": "network",
        "detail": "Software architecture ownership, technical direction, and engineering team leadership.",
        "keywords": (
            "Technical Leadership", "Team Leadership", "System Architecture",
            "Technical Project Management", "Software Development Life Cycle (SDLC)",
            "Code Review", "Release Management", "Process Improvement",
            "Technical Documentation", "Mentoring",
        ),
    },
)
