'use client';
import AppShell from '../../components/AppShell';
import {competencies as fallbackCompetencies} from '../../data/mock';
import {getCompetencyProfile, getMyProfile} from '../../lib/services';
import {Competency} from '../../types';
import {useEffect, useState} from 'react';

export default function CompetencyPage(){
  const [competencies,setCompetencies]=useState<Competency[]>(fallbackCompetencies);
  const [overall,setOverall]=useState(67);

  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      const [comps,profile]=await Promise.all([getCompetencyProfile(),getMyProfile()]);
      if(cancelled)return;
      setCompetencies(comps);setOverall(profile.overallScore);
    })();
    return ()=>{cancelled=true};
  },[]);

  return <AppShell><div className="page-title"><div><h1>My Competency Profile</h1><p>Current capability, required proficiency and evidence supporting the estimate.</p></div><button className="btn btn-secondary">Download profile</button></div><div className="panel panel-pad"><div className="section-label">Competency overview</div><div className="comp-overview" style={{display:'grid',gridTemplateColumns:'260px 1fr',gap:24}}><div style={{display:'flex',alignItems:'center',gap:18}}><div className="score-ring lg"><div className="score-text">{overall}</div></div><div><strong style={{fontSize:18}}>Overall</strong><div className="subtle">Confidence-weighted</div><div className="subtle">{competencies.length} evidence-linked competencies</div></div></div><div className="competency-list">{competencies.map(c=><div className="comp-row" key={c.id}><span className="label">{c.name}</span><div className="bar"><i style={{display:'block',height:'100%',width:`${c.current}%`,background:'var(--blue)',borderRadius:999}}/></div><span className="value">{c.current}</span></div>)}</div></div></div><div className="spacer24"/><div className="section-label">Evidence and explainability</div><div className="course-grid"><div className="panel panel-pad"><h3 style={{marginTop:0}}>Python for Statistical Computing</h3><div className="score-matrix"><div className="score-chip"><span>Current</span><strong>Level 2</strong></div><div className="score-chip"><span>Required</span><strong>Level 4</strong></div><div className="score-chip"><span>Confidence</span><strong>87%</strong></div><div className="score-chip"><span>Evidence</span><strong>4 sources</strong></div></div><div className="spacer16"/><div className="why-box"><strong>Evidence</strong><p>Diagnostic assessment, previous training, a practical exercise and learning history contribute to this estimate.</p></div></div><div className="panel panel-pad"><h3 style={{marginTop:0}}>Assessment → competency update</h3><div className="chart-wrap"><div className="line-chart"><span style={{height:'48%'}}/><span style={{height:'56%'}}/><span style={{height:'63%'}}/><span style={{height:'74%'}}/></div><div className="chart-labels"><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span></div></div><div className="subtle">Demonstration trend: assessment evidence is expected to update the competency profile.</div></div></div></AppShell>;
}
