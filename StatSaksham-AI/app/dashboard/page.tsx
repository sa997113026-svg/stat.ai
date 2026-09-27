'use client';
import Link from 'next/link';
import AppShell from '../../components/AppShell';
import {demoUser as fallbackUser, competencies as fallbackCompetencies, gaps as fallbackGaps, courses as fallbackCourses} from '../../data/mock';
import {getMyProfile, getSkillGaps, getCourses, getCompetencyProfile, ProfileSummary} from '../../lib/services';
import {isLiveMode} from '../../lib/apiClient';
import {Competency, Course, SkillGap} from '../../types';
import {useEffect, useState} from 'react';

const DOMAIN_LABELS: Record<string,string> = {
  'Statistical':'Statistical Competencies',
  'Technical':'Technical Competencies',
  'Digital Governance':'Digital Governance',
  'Behavioural & Managerial':'Behavioural & Managerial',
};

function groupByDomain(items:Competency[]){
  const domains = Object.keys(DOMAIN_LABELS);
  return domains.map(d=>{
    const inDomain = items.filter(c=>c.domain===d);
    const avg=(key:'current'|'required')=>inDomain.length?Math.round(inDomain.reduce((s,c)=>s+c[key],0)/inDomain.length):0;
    return {title:DOMAIN_LABELS[d],score:avg('current'),req:avg('required')};
  });
}

export default function Dashboard(){
  const [profile,setProfile]=useState<ProfileSummary>({
    name:fallbackUser.name,designation:fallbackUser.designation,department:fallbackUser.department,
    experience:fallbackUser.experience,assignment:fallbackUser.assignment,lastAssessment:fallbackUser.lastAssessment,
    learningHours:fallbackUser.learningHours,overallScore:67,
  });
  const [gaps,setGaps]=useState<SkillGap[]>(fallbackGaps);
  const [courses,setCourses]=useState<Course[]>(fallbackCourses);
  const [competencies,setCompetencies]=useState<Competency[]>(fallbackCompetencies);
  const [live,setLive]=useState(false);

  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      const [p,g,c,comps]=await Promise.all([getMyProfile(),getSkillGaps(),getCourses(),getCompetencyProfile()]);
      if(cancelled)return;
      setProfile(p);setGaps(g);setCourses(c);setCompetencies(comps);setLive(isLiveMode());
    })();
    return ()=>{cancelled=true};
  },[]);

  const domainRows = groupByDomain(competencies);

  return <AppShell><div className="page-title"><div><h1>Good morning, {profile.name.split(' ')[0]}</h1><p>Your role requires these competencies. Here is where you are, where the gaps are, and what to do next.</p></div><span className="status">{live?'Live Backend':'Demo Data'}</span></div><div className="dashboard-top"><div className="profile-card"><h2>{profile.designation}</h2><p>{profile.department} · {profile.experience} experience</p><div className="profile-meta"><span>{profile.assignment}</span><span>Last assessment: {profile.lastAssessment}</span><span>{profile.learningHours} learning hours</span></div></div><div className="score-card"><div><h3>Overall competency</h3><strong>{profile.overallScore}<span style={{fontSize:20,color:'#7990a0'}}> / 100</span></strong><div className="subtle">Confidence-weighted score</div></div><div className="score-ring lg"><div className="score-text">{profile.overallScore}</div></div></div></div><div className="section-label">Your competency profile</div><div className="domain-grid">{domainRows.map(d=><Domain key={d.title} title={d.title} score={d.score} req={d.req}/>)}</div><div className="spacer24"/><div className="section-label">Your priority skill gaps</div><div className="gap-grid">{gaps.map(g=><div className="gap-card" key={g.competencyId}><span className={`priority ${g.priority}`}>{g.priority} priority</span><h3>{g.competencyName}</h3><div className="levels">Level {g.currentLevel} current · Level {g.requiredLevel} required</div><span className="gap-number">Gap: {g.requiredLevel-g.currentLevel} levels</span><p>{g.reason}</p><Link href="/skill-gaps" className="action">View evidence and next action →</Link></div>)}</div><div className="spacer24"/><div className="section-label">Personalized learning path</div><div className="path">{courses.slice(0,5).map((c,i)=><div className="path-card" key={c.id}><small>STEP {i+1} · {c.provider}</small><h4>{c.title}</h4><p>{c.competency} · {c.duration}</p></div>)}</div><div className="spacer24"/><div className="split"><div className="panel panel-pad"><div className="section-label">Why these recommendations?</div><div className="score-matrix"><div className="score-chip"><span>Competency match</span><strong>92%</strong></div><div className="score-chip"><span>Role relevance</span><strong>95%</strong></div><div className="score-chip"><span>Difficulty fit</span><strong>88%</strong></div><div className="score-chip"><span>Evidence confidence</span><strong>91%</strong></div></div></div><div className="panel panel-pad"><div className="section-label">Next action</div><h3 style={{marginTop:0}}>Complete: Python for Statistical Analysis</h3><p className="muted">Recommended because your role requires advanced Python capability and your current level is estimated at Basic.</p><Link href="/learning-path" className="btn btn-primary">Start Learning</Link></div></div></AppShell>;
}
function Domain({title,score,req}:{title:string,score:number,req:number}){return <div className="domain-card"><h4>{title}</h4><div className="domain-meter"><i style={{width:`${score}%`}}/></div><div className="domain-meta"><span>{score}/100</span><span>Target {req}</span></div></div>}
