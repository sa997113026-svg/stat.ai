'use client';
import AppShell from '../../../components/AppShell';
import {getWorkforceAnalytics} from '../../../lib/services';
import {isLiveMode} from '../../../lib/apiClient';
import {useEffect, useState} from 'react';

const skills=['Python','Sampling','Data Visualization','AI / ML','APIs','Cybersecurity'];
const rows=[['Sampling','Survey Methodology','78','86','4','3','4'],['Python','Technical','61','80','2','3','4'],['Data Visualization','Technical','69','82','3','4','5'],['AI / ML','Emerging','41','75','1','2','5'],['APIs','Digital Governance','56','70','2','3','4']];

type Analytics = {
  total_officials:number; average_competency:number; critical_skill_gaps:number;
  training_hours:number; assessment_completion_rate:number;
};

export default function AdminDashboard(){
  const [a,setA]=useState<Analytics>({total_officials:4821,average_competency:64,critical_skill_gaps:17,training_hours:21438,assessment_completion_rate:82});
  const [live,setLive]=useState(false);

  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      const data=await getWorkforceAnalytics();
      if(cancelled)return;
      setA(data);setLive(isLiveMode());
    })();
    return ()=>{cancelled=true};
  },[]);

  const kpis:[string,string][]=[
    [a.total_officials.toLocaleString(),'Officials'],
    [`${Math.round(a.average_competency)}%`,'Average Competency'],
    [String(a.critical_skill_gaps),'Critical Gaps'],
    [a.training_hours.toLocaleString(),'Training Hours'],
    [`${Math.round(a.assessment_completion_rate)}%`,'Assessment Completion'],
    ['+8%','Competency Growth'],
  ];

  return <AppShell><div className="page-title"><div><h1>Workforce Skill Intelligence</h1><p>Organization-wide view of competency distribution, priority gaps and emerging capability requirements.</p></div><span className="status">{live?'Live Backend':'Demonstration Data'}</span></div><div className="admin-kpis">{kpis.map(([v,l])=><div className="admin-kpi" key={l}><span>{l}</span><strong>{v}</strong></div>)}</div><div className="spacer24"/><div className="split"><div className="panel panel-pad"><div className="section-label">Workforce competency distribution</div><div className="heatmap"><div className="head">Competency / Role</div>{['Junior','Mid','Senior','Lead','Specialist'].map(x=><div className="head" key={x}>{x}</div>)}{rows.map((r,i)=><div key={r[0]+i} style={{display:'contents'}}><div>{r[0]}</div>{r.slice(2).map((v,j)=><div className={Number(v)>=80?'heat-5':Number(v)>=70?'heat-4':Number(v)>=60?'heat-3':Number(v)>=50?'heat-2':'heat-1'} key={j}>{v}</div>)}</div>)}</div></div><div className="panel panel-pad"><div className="section-label">Emerging skill requirements</div><div className="bars" style={{marginTop:0}}>{skills.map((s,i)=><div className="bar-row" key={s}><span>{s}</span><div className="bar"><i style={{width:`${92-i*10}%`,background:i<3?'var(--blue)':'var(--teal)'}}/></div><b>+{34-i*4}%</b></div>)}</div><div className="spacer16"/><div className="why-box"><strong>Future workforce readiness</strong><p>Use current capability plus role/future-role requirements to plan learning capacity. Forecasts shown here are demonstration values.</p></div></div></div><div className="spacer24"/><div className="panel panel-pad"><div className="section-label">Critical skill gaps</div><table className="table"><thead><tr><th>Skill</th><th>Domain</th><th>Current</th><th>Required</th><th>Affected officials</th><th>Priority</th></tr></thead><tbody>{rows.map(r=><tr key={r[0]}><td><strong>{r[0]}</strong></td><td>{r[1]}</td><td>{r[2]}%</td><td>{r[3]}%</td><td>{r[4]}</td><td><span className={r[0]==='Python'?'status':'status warn'}>{r[5]} level gap</span></td></tr>)}</tbody></table></div></AppShell>;
}
