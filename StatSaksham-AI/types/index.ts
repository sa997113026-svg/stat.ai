export type Priority = 'high'|'medium'|'low';
export type CompetencyDomain = 'Statistical'|'Technical'|'Digital Governance'|'Behavioural & Managerial';

export type SkillGap = {
  competencyId:string;
  competencyName:string;
  domain:CompetencyDomain;
  currentLevel:number;
  requiredLevel:number;
  priority:Priority;
  confidence:number;
  reason:string;
  nextAction:string;
};

export type Competency = {
  id:string;
  name:string;
  domain:CompetencyDomain;
  current:number;
  required:number;
  confidence:number;
  trend:number;
  evidenceCount:number;
};

export type Course = {
  id:string;
  title:string;
  provider:string;
  competency:string;
  domain:CompetencyDomain;
  difficulty:'Beginner'|'Intermediate'|'Advanced';
  duration:string;
  language:string;
  match:number;
  status:'Recommended'|'In Progress'|'Completed';
};

export type Question = {
  id:string;
  question:string;
  options:string[];
  answer:number;
  explanation:string;
  competency:string;
  difficulty:'Easy'|'Medium'|'Hard';
  source:string;
  confidence:number;
};
