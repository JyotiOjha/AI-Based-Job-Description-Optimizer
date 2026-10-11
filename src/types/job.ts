export interface JobInput {
  title: string;
  experience: string;
  skills: string[];
  description: string;
}

export interface JDResponse {
  enhanced_skills: string[];
  generated_jd: {
    summary: string;
    responsibilities: string[];
    requirements: string[];
    nice_to_have: string[];
  };
  jd_score: {
    score: number;
    ats_score: number;
    issues: string[];
    improvements: string[];
  };
}