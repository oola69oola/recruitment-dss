export const SAMPLE_JOB_DESCRIPTIONS = {
  "Product Manager (Tech)": "We are seeking a seasoned Technical Product Manager with 4-6 years of experience driving SaaS product strategy, roadmap execution, and Agile sprint planning. The candidate will write comprehensive PRDs, conduct user research and wireframing with Figma, run A/B experimentation, define core product KPIs, and analyze user engagement using Amplitude and SQL. A Bachelor's degree in Computer Science, Business, or a related discipline is required. Must possess strong stakeholder management, cross-functional communication, analytical thinking, and Agile/Scrum leadership.",
  "Data Scientist / AI Engineer": "Looking for an innovative Senior Data Scientist / AI Engineer with 4-6 years of hands-on experience building machine learning models, deep learning architectures, and GenAI/LLM pipelines. Required competencies include Python, SQL, pandas, numpy, scikit-learn, PyTorch, and TensorFlow. Candidate should have demonstrated experience in NLP, Hugging Face transformers, LangChain, and distributed data processing with Spark. A Master's or PhD degree in Computer Science, Data Science, or Mathematics is required. Proven problem solving, critical thinking, and collaborative skills.",
  "DevOps / SRE Engineer": "We are hiring a DevOps / Site Reliability Engineer (SRE) with 4-6 years of experience engineering cloud-native infrastructure, high availability systems, and automated CI/CD pipelines. Key technical proficiencies include Kubernetes, Docker, Terraform, Ansible, AWS, GCP, and Linux. The candidate will build monitoring and observability with Prometheus, Grafana, and Datadog, with scripting in Python, Go, and Bash. A Bachelor's degree in Computer Science or Software Engineering is required. Exceptional teamwork, incident management, and problem solving.",
  "Cyber Security": "Seeking a Cyber Security Specialist with 4-6 years of enterprise experience in threat hunting, incident response, and security architecture. Required skills include SIEM monitoring with Splunk, firewall administration, IDS/IPS, vulnerability management, penetration testing with Metasploit and Burp Suite, IAM, and OWASP Top 10 hardening. Scripting in Python or Bash and network analysis with Wireshark required. Bachelor's degree in Cybersecurity or related field (CISSP / CEH preferred). Strong crisis communication, analytical thinking, and decision making."
};

export const CANONICAL_ROLES_DATA = {
  "Product Manager (Tech)": {
    title: "Product Manager (Tech)",
    tagline: "Product Strategy, PRDs, Roadmaps & SaaS Lifecycle",
    description: "",
    required_hard_skills: [
      "prd writing", "product roadmap", "product strategy", "wireframing",
      "user research", "a/b testing", "kpi definition", "saas metrics",
      "figma", "jira", "confluence", "api integration", "sql", "amplitude"
    ],
    required_soft_skills: [
      "stakeholder management", "communication", "leadership", "analytical thinking", "agile/scrum"
    ],
    target_tenure_years: 5.0,
    target_tenure_range: "4-6 years",
    required_education_level: "bachelor",
  },
  "Data Scientist / AI Engineer": {
    title: "Data Scientist / AI Engineer",
    tagline: "ML Models, Deep Learning, MLOps & GenAI/LLM Pipelines",
    description: "",
    required_hard_skills: [
      "python", "sql", "pandas", "numpy", "scikit-learn", "pytorch",
      "tensorflow", "deep learning", "nlp", "transformers", "llms",
      "langchain", "hugging face", "spark", "mlops", "docker"
    ],
    required_soft_skills: [
      "problem solving", "analytical thinking", "collaboration", "communication", "critical thinking"
    ],
    target_tenure_years: 4.0,
    target_tenure_range: "4-6 years",
    required_education_level: "master",
  },
  "DevOps / SRE Engineer": {
    title: "DevOps / SRE Engineer",
    tagline: "Cloud Infrastructure, Kubernetes, CI/CD & System Reliability",
    description: "",
    required_hard_skills: [
      "kubernetes", "docker", "terraform", "aws", "gcp", "ansible",
      "prometheus", "grafana", "ci/cd", "github actions", "bash",
      "python", "go", "datadog", "linux"
    ],
    required_soft_skills: [
      "problem solving", "incident management", "teamwork", "communication", "adaptability"
    ],
    target_tenure_years: 5.0,
    target_tenure_range: "4-6 years",
    required_education_level: "bachelor",
  },
  "Cyber Security": {
    title: "Cyber Security",
    tagline: "Cloud Security, SIEM Monitoring, Penetration Testing & OWASP Hardening",
    description: "",
    required_hard_skills: [
      "incident response", "vulnerability management", "siem", "splunk",
      "firewalls", "ids/ips", "iam", "owasp top 10", "nmap",
      "wireshark", "metasploit", "burp suite", "aws security", "linux", "python", "bash"
    ],
    required_soft_skills: [
      "analytical thinking", "crisis communication", "decision making", "problem solving", "teamwork"
    ],
    target_tenure_years: 5.0,
    target_tenure_range: "4-6 years",
    required_education_level: "bachelor",
  }
};

export const TENURE_RANGES = [
  { label: '0-1 years (Entry-Level / Intern)', value: '0-1 years', midpoint: 1.0, short: '0-1 yrs', badge: 'Entry' },
  { label: '1-3 years (Junior / Associate)', value: '1-3 years', midpoint: 2.0, short: '1-3 yrs', badge: 'Junior' },
  { label: '4-6 years (Mid-Level / Mid-Senior)', value: '4-6 years', midpoint: 5.0, short: '4-6 yrs', badge: 'Mid-Level' },
  { label: '7-10 years (Senior / Lead)', value: '7-10 years', midpoint: 8.5, short: '7-10 yrs', badge: 'Senior' },
  { label: '10+ years (Principal / Director)', value: '10+ years', midpoint: 12.0, short: '10+ yrs', badge: 'Leadership' },
];

