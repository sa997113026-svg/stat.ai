import { Competency, Course, Question, SkillGap } from '../types';

export const demoUser = {
  name:'Ananya Sharma',
  designation:'Senior Statistical Officer',
  department:'Labour Statistics',
  experience:'7 years',
  assignment:'Labour Force Survey – Data Quality & Analysis',
  lastAssessment:'18 Sep 2026',
  learningHours:14.5
};

export const competencies:Competency[] = [
  {id:'survey',name:'Survey Design',domain:'Statistical',current:74,required:82,confidence:91,trend:6,evidenceCount:5},
  {id:'sampling',name:'Sampling Methods',domain:'Statistical',current:52,required:80,confidence:86,trend:4,evidenceCount:4},
  {id:'labour',name:'Labour Statistics',domain:'Statistical',current:84,required:86,confidence:94,trend:3,evidenceCount:6},
  {id:'python',name:'Python for Statistical Computing',domain:'Technical',current:42,required:78,confidence:87,trend:8,evidenceCount:4},
  {id:'viz',name:'Data Visualization',domain:'Technical',current:63,required:82,confidence:89,trend:7,evidenceCount:5},
  {id:'apis',name:'APIs & Open Data',domain:'Digital Governance',current:47,required:70,confidence:81,trend:5,evidenceCount:3},
  {id:'privacy',name:'Data Privacy',domain:'Digital Governance',current:73,required:76,confidence:95,trend:2,evidenceCount:5},
  {id:'lead',name:'Leadership & Communication',domain:'Behavioural & Managerial',current:78,required:84,confidence:90,trend:4,evidenceCount:4}
];

export const gaps:SkillGap[] = [
  {competencyId:'python',competencyName:'Python for Statistical Computing',domain:'Technical',currentLevel:2,requiredLevel:4,priority:'high',confidence:87,reason:'Required for current analytical responsibilities and future data workflows.',nextAction:'Complete the recommended Python pathway.'},
  {competencyId:'sampling',competencyName:'Sampling Methods',domain:'Statistical',currentLevel:2,requiredLevel:4,priority:'high',confidence:86,reason:'Role profile requires advanced sampling design for large-scale surveys.',nextAction:'Take the Sampling Methods learning module and assessment.'},
  {competencyId:'viz',competencyName:'Data Visualization',domain:'Technical',currentLevel:3,requiredLevel:4,priority:'medium',confidence:89,reason:'Required to translate statistical outputs into decision-ready visual stories.',nextAction:'Complete the visual analytics module.'},
  {competencyId:'apis',competencyName:'APIs & Open Data',domain:'Digital Governance',currentLevel:2,requiredLevel:3,priority:'medium',confidence:81,reason:'Supports interoperable data workflows and open-data publication.',nextAction:'Complete API fundamentals and practice lab.'}
];

export const courses:Course[] = [
  {id:'igot-python',title:'Python for Statistical Analysis',provider:'iGOT Karmayogi',competency:'Python for Statistical Computing',domain:'Technical',difficulty:'Intermediate',duration:'4 hrs',language:'English',match:95,status:'Recommended'},
  {id:'igot-viz',title:'Data Visualization for Public Data',provider:'iGOT Karmayogi',competency:'Data Visualization',domain:'Technical',difficulty:'Intermediate',duration:'3.5 hrs',language:'English',match:92,status:'Recommended'},
  {id:'nssta-sampling',title:'Advanced Sampling & Survey Methodology',provider:'NSSTA / TPAC',competency:'Sampling Methods',domain:'Statistical',difficulty:'Advanced',duration:'3 days',language:'English',match:94,status:'Recommended'},
  {id:'lab-api',title:'Open Data & API Integration Lab',provider:'StatSaksham Practice Lab',competency:'APIs & Open Data',domain:'Digital Governance',difficulty:'Intermediate',duration:'2 hrs',language:'English',match:88,status:'Recommended'}
];

export const questions:Question[] = [
  {id:'q1',question:'Which sampling approach selects independent samples from predefined homogeneous groups?',options:['Simple random sampling','Stratified sampling','Systematic sampling','Convenience sampling'],answer:1,explanation:'Stratified sampling divides the population into strata and samples independently from each group.',competency:'Sampling Methods',difficulty:'Medium',source:'Uploaded training material — Section 3.2',confidence:94},
  {id:'q2',question:'Which Python structure is commonly used to represent tabular data in a pandas workflow?',options:['DataFrame','Tuple','Set','Decorator'],answer:0,explanation:'A pandas DataFrame provides a two-dimensional labelled tabular structure.',competency:'Python for Statistical Computing',difficulty:'Easy',source:'Uploaded training material — Page 8',confidence:97},
  {id:'q3',question:'Which visualization best communicates the distribution of a continuous numerical variable?',options:['Histogram','Pie chart','Network diagram','Gantt chart'],answer:0,explanation:'A histogram groups numerical observations into bins and shows their distribution.',competency:'Data Visualization',difficulty:'Easy',source:'Uploaded training material — Section 5.1',confidence:96},
  {id:'q4',question:'What is the primary purpose of an API in an interoperable data ecosystem?',options:['To compress images','To expose structured programmatic access to data/services','To replace databases','To format presentations'],answer:1,explanation:'APIs allow systems to exchange structured data and services through defined interfaces.',competency:'APIs & Open Data',difficulty:'Medium',source:'Uploaded training material — Page 14',confidence:93}
];
