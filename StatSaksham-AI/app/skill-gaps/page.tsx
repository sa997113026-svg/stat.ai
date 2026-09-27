'use client';
import AppShell from '../../components/AppShell';
import {gaps as fallbackGaps} from '../../data/mock';
import {getSkillGaps} from '../../lib/services';
import {SkillGap} from '../../types';
import {useEffect, useState} from 'react';

export default function SkillGaps(){
  const [gaps,setGaps]=useState<SkillGap[]>(fallbackGaps);

  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      const data=await getSkillGaps();
      if(!cancelled)setGaps(data);
    })();
    return ()=>{cancelled=true};
  },[]);

  return <AppShell><div className="page-title"><div><h1>Your Priority Skill Gaps</h1><p>Role-aligned gaps ranked by priority, supported by evidence and next actions.</p></div><span className="status">{gaps.length} identified gaps</span></div><div className="gap-grid">{gaps.map(g=><div className="gap-card" key={g.competencyId}><span className={`priority ${g.priority}`}>{g.priority} priority</span><h3>{g.competencyName}</h3><div className="levels">Current Level {g.currentLevel} · Required Level {g.requiredLevel}</div><div className="progressline"><i style={{width:`${Math.round(g.currentLevel/g.requiredLevel*100)}%`}}/></div><div className="spacer8"/><span className="subtle">Confidence {g.confidence}%</span><div className="spacer8"/><p><strong>Why it matters:</strong> {g.reason}</p><p><strong>Next action:</strong> {g.nextAction}</p><button className="btn btn-secondary">View Evidence</button></div>)}</div><div className="spacer24"/><div className="panel panel-pad"><div className="section-label">Gap methodology</div><p className="muted">The prototype compares role-required proficiency with an evidence-weighted estimate based on diagnostic assessments, prior learning, practical evidence and learning history. These scoring weights are configurable in the backend.</p></div></AppShell>;
}
