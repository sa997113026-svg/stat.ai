'use client';
import Link from 'next/link';
import AppShell from '../../components/AppShell';
import {courses as fallbackCourses} from '../../data/mock';
import {getCourses} from '../../lib/services';
import {Course} from '../../types';
import {useEffect, useState} from 'react';

export default function LearningPath(){
  const [courses,setCourses]=useState<Course[]>(fallbackCourses);

  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      const data=await getCourses();
      if(!cancelled)setCourses(data);
    })();
    return ()=>{cancelled=true};
  },[]);

  return <AppShell><div className="page-title"><div><h1>Personalized Learning Path</h1><p>Explainable recommendations mapped to competency gaps and role requirements.</p></div><span className="status">Path confidence 91%</span></div><div className="panel panel-pad"><div className="section-label">Role context</div><div className="score-matrix"><div className="score-chip"><span>Role</span><strong>Senior Statistical Officer</strong></div><div className="score-chip"><span>Domain</span><strong>Labour Statistics</strong></div><div className="score-chip"><span>Highest gap</span><strong>Python</strong></div><div className="score-chip"><span>Target</span><strong>Advanced</strong></div></div></div><div className="spacer24"/><div className="path" style={{gridTemplateColumns:'repeat(5,1fr)'}}>{courses.concat([{id:'assessment',title:'AI Competency Assessment',provider:'StatSaksham AI',competency:'Targeted reassessment',domain:'Technical',difficulty:'Advanced',duration:'20 min',language:'English',match:91,status:'Recommended'} as any]).map((c,i)=><div className="path-card" key={c.id}><small>STEP {i+1} · {c.provider}</small><h4>{c.title}</h4><p>{c.competency} · {c.duration}</p><div className="spacer8"/><span className="status">{c.match}% match</span></div>)}</div><div className="spacer24"/><div className="course-grid">{courses.map(c=><div className="course-card" key={c.id}><div className="course-banner"/><div className="course-body"><div className="course-top"><span>{c.provider}</span><span>{c.status}</span></div><h3>{c.title}</h3><p>{c.competency}</p><div className="course-meta"><span>{c.duration}</span><span>{c.difficulty}</span><span>{c.language}</span></div><div className="course-footer"><span className="match">{c.match}% match</span><Link href="/assessment" className="btn btn-primary">Start</Link></div></div></div>)}</div><div className="spacer24"/><div className="panel panel-pad"><div className="section-label">Why this path?</div><div className="why-box"><strong>Recommendation rationale</strong><p>These steps were ordered to close the highest-impact competency gaps first, then reinforce them with practical work and a targeted reassessment.</p></div></div></AppShell>;
}
