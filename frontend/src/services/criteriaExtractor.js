/**
 * Client-Side 5D Criteria Extraction Engine for RecruitIQ.
 * Extracts Hard Skills, Soft Competencies, Tenure Range, Minimum Education,
 * and Role Proximity from job description text directly in the browser.
 * Provides 100% offline and standalone reliability for Netlify deployments.
 */

import { CANONICAL_ROLES_DATA, TENURE_RANGES } from '../constants/roles';

// Technical Hard Skills Taxonomy
export const HARD_SKILLS = [
  // Programming & Scripting
  "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust", "ruby", "php", "scala", "r", "swift", "kotlin", "bash", "shell scripting",
  // Web & API Frameworks
  "react", "react.js", "vue", "vue.js", "angular", "node.js", "nodejs", "django", "fastapi", "flask", "spring boot", "express", "next.js", "html", "css", "rest apis", "rest api", "graphql", "tailwind",
  // Cloud, DevOps & Infrastructure
  "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "podman", "kubernetes", "k8s", "openshift", "terraform", "ci/cd", "ci-cd", "jenkins",
  "git", "github", "gitlab", "ansible", "linux", "nginx", "kafka", "rabbitmq", "cloudformation", "pulumi", "github actions", "circleci", "argocd", "helm",
  // Monitoring & Observability
  "prometheus", "grafana", "datadog", "new relic", "elk stack", "splunk",
  // Databases & Big Data
  "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "elasticsearch", "cassandra", "sql", "nosql",
  "snowflake", "spark", "apache spark", "hadoop", "hive", "airflow", "dbt", "bigquery", "dynamodb",
  // AI, ML & Data Science
  "machine learning", "deep learning", "nlp", "computer vision", "pytorch", "tensorflow", "scikit-learn", "sklearn", "keras",
  "pandas", "numpy", "transformers", "hugging face", "huggingface", "bert", "sbert", "cuda", "reinforcement learning",
  "llm", "llms", "genai", "generative ai", "statistics", "data analysis", "tableau", "power bi", "powerbi", "matplotlib", "seaborn",
  "mlops", "mlflow", "databricks", "sagemaker", "vertex ai", "langchain", "prompt engineering",
  // Cyber Security
  "incident response", "ids/ips", "iam", "owasp top 10", "owasp", "siem", "vulnerability management", "ceh", "metasploit",
  "burp suite", "firewalls", "comptia security+", "nmap", "wireshark", "saml", "oauth", "aws security", "cissp", "penetration testing", "threat hunting", "zero trust", "network security", "endpoint security",
  // Product Management (Tech)
  "prd writing", "prd", "product roadmap", "roadmap", "product strategy", "wireframing", "wireframes", "user research", "a/b testing", "kpi definition", "kpi", "saas metrics",
  "growth hacking", "amplitude", "mixpanel", "figma", "jira", "confluence", "market analysis", "api integration", "backlog grooming", "user stories", "go-to-market"
];

// Soft Skills & Leadership Competencies
export const SOFT_SKILLS = [
  "communication", "teamwork", "leadership", "collaboration", "problem solving",
  "stakeholder management", "mentoring", "critical thinking", "adaptability",
  "time management", "conflict resolution", "presentation", "analytical thinking",
  "decision making", "agile", "scrum", "agile/scrum", "coaching", "initiative",
  "cross-functional collaboration", "strategic thinking", "emotional intelligence"
];

// Skill Normalization Mapping
const SYNONYMS = {
  "k8s": "kubernetes",
  "golang": "go",
  "postgres": "postgresql",
  "amazon web services": "aws",
  "google cloud platform": "gcp",
  "google cloud": "gcp",
  "node js": "node.js",
  "nodejs": "node.js",
  "react js": "react",
  "react.js": "react",
  "vue js": "vue",
  "vue.js": "vue",
  "ts": "typescript",
  "ci cd": "ci/cd",
  "ci-cd": "ci/cd",
  "continuous integration": "ci/cd",
  "continuous deployment": "ci/cd",
  "github action": "github actions",
  "powerbi": "power bi",
  "huggingface": "hugging face",
  "apache spark": "spark",
  "scikit learn": "scikit-learn",
  "sklearn": "scikit-learn",
  "restful api": "rest apis",
  "restful apis": "rest apis",
  "rest api": "rest apis",
  "owasp": "owasp top 10",
  "pen testing": "penetration testing",
  "pentesting": "penetration testing",
  "prd": "prd writing",
  "roadmap": "product roadmap",
  "wireframes": "wireframing",
  "kpi": "kpi definition",
  "cross-functional collaboration": "collaboration",
  "agile": "agile/scrum",
  "scrum": "agile/scrum",
};

// Role Indicators for Title Proximity Scoring
const ROLE_INDICATORS = {
  "Product Manager (Tech)": [
    "product manager", "product management", "prd", "roadmaps", "roadmap", "user research",
    "wireframing", "wireframes", "a/b testing", "kpi", "saas metrics", "figma", "jira",
    "backlog", "product strategy", "customer discovery", "go-to-market", "user stories",
    "feature prioritization", "product lifecycle", "stakeholder management"
  ],
  "Data Scientist / AI Engineer": [
    "data scientist", "ai engineer", "machine learning", "deep learning", "nlp", "llm",
    "transformers", "pytorch", "tensorflow", "scikit-learn", "mlops", "data science",
    "predictive modeling", "computer vision", "pandas", "numpy", "statistics", "feature engineering",
    "neural networks", "genai", "generative ai", "sagemaker", "langchain"
  ],
  "DevOps / SRE Engineer": [
    "devops", "sre", "site reliability", "kubernetes", "k8s", "docker", "terraform",
    "ci/cd", "infrastructure as code", "ansible", "prometheus", "grafana", "helm",
    "cloud architecture", "linux", "systems engineer", "datadog", "high availability",
    "containerization", "monitoring", "argocd", "cloudformation"
  ],
  "Cyber Security": [
    "cyber security", "cybersecurity", "security engineer", "siem", "splunk", "firewalls",
    "ids/ips", "penetration testing", "vulnerability management", "owasp", "incident response",
    "threat hunting", "iam", "zero trust", "cissp", "ceh", "network security", "endpoint security",
    "burp suite", "metasploit", "wireshark", "compliance"
  ]
};

/**
 * Extract required tenure range and midpoint years from text.
 */
export function extractTenure(text) {
  const normalized = text.toLowerCase();

  // 1. Explicit range regex: e.g. "4-6 years", "3 to 5 yrs", "1-3 years"
  const rangeMatch = normalized.match(/(\d+(?:\.\d+)?)\s*(?:-|–|—|to)\s*(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?|y)\b/i);
  if (rangeMatch) {
    const low = parseFloat(rangeMatch[1]);
    const high = parseFloat(rangeMatch[2]);
    const avg = (low + high) / 2.0;

    if (avg <= 1.5) return { range: '0-1 years', years: 1.0 };
    if (avg <= 3.5) return { range: '1-3 years', years: 2.0 };
    if (avg <= 6.5) return { range: '4-6 years', years: 5.0 };
    if (avg <= 10.0) return { range: '7-10 years', years: 8.5 };
    return { range: '10+ years', years: 12.0 };
  }

  // 2. Minimum or Plus regex: e.g. "5+ years", "minimum 4 years", "at least 3 years"
  const minMatch = normalized.match(/(?:at least|minimum|min|over|\+)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?|y)\b/i) ||
                   normalized.match(/(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?|y)\b/i);
  if (minMatch) {
    const val = parseFloat(minMatch[1]);
    if (val <= 1.0) return { range: '0-1 years', years: 1.0 };
    if (val <= 3.0) return { range: '1-3 years', years: 2.0 };
    if (val <= 6.0) return { range: '4-6 years', years: 5.0 };
    if (val <= 9.0) return { range: '7-10 years', years: 8.5 };
    return { range: '10+ years', years: 12.0 };
  }

  // Fallback to Mid-Level (4-6 years) default standard
  return { range: '4-6 years', years: 5.0 };
}

/**
 * Extract minimum education level from text.
 */
export function extractEducation(text) {
  const normalized = text.toLowerCase();

  if (/\b(?:phd|ph\.d|doctorate|doctoral)\b/i.test(normalized)) {
    return 'phd';
  }
  if (/\b(?:master'?s?|msc|m\.sc|m\.eng|meng|mba)\b/i.test(normalized)) {
    return 'master';
  }
  if (/\b(?:bachelor'?s?|bsc|b\.sc|b\.eng|beng|b\.tech|btech|degree|undergraduate)\b/i.test(normalized)) {
    return 'bachelor';
  }
  if (/\b(?:diploma|associate'?s?|high school|secondary)\b/i.test(normalized)) {
    return 'high_school';
  }

  return 'bachelor';
}

/**
 * Detect matching Canonical Role from title hint and text keyword frequency.
 */
export function detectRoleProximity(text, titleHint = '') {
  const normalized = (text + ' ' + titleHint).toLowerCase();
  let bestRole = titleHint && CANONICAL_ROLES_DATA[titleHint] ? titleHint : "Product Manager (Tech)";
  let maxScore = -1;

  for (const [role, keywords] of Object.entries(ROLE_INDICATORS)) {
    let score = 0;
    // Check if role title is explicitly mentioned
    if (normalized.includes(role.toLowerCase())) {
      score += 5;
    }
    // Count keyword indicator hits
    for (const kw of keywords) {
      if (normalized.includes(kw)) {
        score += 1;
      }
    }

    if (score > maxScore) {
      maxScore = score;
      bestRole = role;
    }
  }

  return bestRole;
}

/**
 * Comprehensive 5D Criteria Extractor
 * Automatically parses text into Hard Skills, Soft Skills, Tenure Range, Minimum Education,
 * Role Proximity, and Balanced 5D Weight Vector.
 */
export function extract5DCriteria(text, titleHint = '') {
  if (!text || text.trim().length === 0) {
    return null;
  }

  const normalized = text.toLowerCase();

  // 1. Extract Hard Skills
  const detectedHard = new Set();
  for (const skill of HARD_SKILLS) {
    const escaped = skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(?:^|[^a-zA-Z0-9_+#-])${escaped}(?:$|[^a-zA-Z0-9_+#-])`, 'i');
    if (regex.test(normalized)) {
      const canonical = SYNONYMS[skill] || skill;
      detectedHard.add(canonical);
    }
  }

  // 2. Extract Soft Skills
  const detectedSoft = new Set();
  for (const skill of SOFT_SKILLS) {
    const escaped = skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(?:^|[^a-zA-Z0-9_+#-])${escaped}(?:$|[^a-zA-Z0-9_+#-])`, 'i');
    if (regex.test(normalized)) {
      const canonical = SYNONYMS[skill] || skill;
      detectedSoft.add(canonical);
    }
  }

  // 3. Extract Tenure Range
  const tenure = extractTenure(text);

  // 4. Extract Minimum Education
  const education = extractEducation(text);

  // 5. Detect Role Proximity
  const matchedRole = detectRoleProximity(text, titleHint);

  // If few skills detected, augment with canonical baseline skills for the matched role
  const canonicalRoleDef = CANONICAL_ROLES_DATA[matchedRole];
  if (detectedHard.size < 4 && canonicalRoleDef?.required_hard_skills) {
    canonicalRoleDef.required_hard_skills.forEach(s => detectedHard.add(s));
  }
  if (detectedSoft.size < 2 && canonicalRoleDef?.required_soft_skills) {
    canonicalRoleDef.required_soft_skills.forEach(s => detectedSoft.add(s));
  }

  const hardSkillsList = Array.from(detectedHard);
  const softSkillsList = Array.from(detectedSoft);

  // 6. Optimal 5D Weight Vector per Role Archetype
  let weights = { w_h: 0.35, w_s: 0.15, w_t: 0.20, w_e: 0.20, w_d: 0.10 };
  if (matchedRole === "Product Manager (Tech)") {
    weights = { w_h: 0.30, w_s: 0.25, w_t: 0.20, w_e: 0.15, w_d: 0.10 };
  } else if (matchedRole === "Data Scientist / AI Engineer") {
    weights = { w_h: 0.35, w_s: 0.15, w_t: 0.20, w_e: 0.20, w_d: 0.10 };
  } else if (matchedRole === "DevOps / SRE Engineer") {
    weights = { w_h: 0.40, w_s: 0.15, w_t: 0.20, w_e: 0.15, w_d: 0.10 };
  } else if (matchedRole === "Cyber Security") {
    weights = { w_h: 0.35, w_s: 0.15, w_t: 0.25, w_e: 0.15, w_d: 0.10 };
  }

  return {
    extracted: true,
    is_auto_extracted: true,
    title: matchedRole,
    title_proximity_match: matchedRole,
    required_hard_skills: hardSkillsList,
    required_soft_skills: softSkillsList,
    target_tenure_range: tenure.range,
    target_tenure_years: tenure.years,
    required_education_level: education,
    weight_vector: weights,
    summary: `Extracted ${hardSkillsList.length} technical skills, ${softSkillsList.length} soft competencies, ${tenure.range} experience, and ${education} degree benchmark.`
  };
}
