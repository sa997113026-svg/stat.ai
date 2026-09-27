'use client';
import AppShell from '../../components/AppShell';
import {questions as fallbackQuestions} from '../../data/mock';
import {startAssessment, submitAssessment, AssessmentResult} from '../../lib/services';
import {useEffect, useState} from 'react';

type UIOption = {key:string; text:string};
type UIQuestion = {id:string; text:string; competency:string; difficulty:string; options:UIOption[]};

const ASSESSMENT_ID = 'asmt-plfs-2026';
const LETTERS = ['A','B','C','D'];

function fromMock(): UIQuestion[] {
  return fallbackQuestions.map(q=>({
    id:q.id, text:q.question, competency:q.competency, difficulty:q.difficulty,
    options:q.options.map((t,i)=>({key:LETTERS[i],text:t})),
  }));
}

export default function Assessment(){
  const [questions,setQuestions]=useState<UIQuestion[]>(fromMock());
  const [live,setLive]=useState(false);
  const [idx,setIdx]=useState(0);
  const [answers,setAnswers]=useState<Record<string,string>>({});
  const [done,setDone]=useState(false);
  const [submitting,setSubmitting]=useState(false);
  const [result,setResult]=useState<AssessmentResult|null>(null);

  useEffect(()=>{
    let cancelled=false;
    (async()=>{
      const started=await startAssessment(ASSESSMENT_ID);
      if(cancelled||!started)return;
      setQuestions(started.questions.map(sq=>({id:sq.id,text:sq.text,competency:sq.competency,difficulty:sq.difficulty,options:sq.options})));
      setIdx(0);
      setAnswers({});
      setLive(true);
    })();
    return ()=>{cancelled=true};
  },[]);

  const q = questions[idx];
  const selectedKey = answers[q.id];

  const submit = async () => {
    if (live) {
      setSubmitting(true);
      const r = await submitAssessment(ASSESSMENT_ID, answers);
      setSubmitting(false);
      setResult(r);
    }
    setDone(true);
  };

  if (done) {
    if (live && result) {
      const scorePct = Math.round(result.score_percent);
      return <AppShell><div className="page-title"><div><h1>Assessment Complete</h1><p>Your results are ready and can be fed back into the competency engine.</p></div><span className="status">{result.correct_answers} / {result.total_questions}</span></div><div className="split"><div className="panel panel-pad"><div className="section-label">Backend-graded result</div><div className="score-matrix"><div className="score-chip"><span>Score</span><strong>{scorePct}%</strong></div><div className="score-chip"><span>Correct</span><strong>{result.correct_answers}</strong></div><div className="score-chip"><span>Incorrect</span><strong>{result.incorrect_answers}</strong></div><div className="score-chip"><span>Total</span><strong>{result.total_questions}</strong></div></div><div className="spacer16"/><div className="why-box"><strong>Competency update</strong><p>{result.competency_update?`Verified level moved from Level ${result.competency_update.previous_level} to Level ${result.competency_update.new_level} based on this graded attempt.`:'This attempt did not cross the level-upgrade threshold. Keep practising and reattempt when ready.'}</p></div></div><div className="panel panel-pad"><div className="section-label">Recommended reinforcement</div><h3 style={{marginTop:0}}>Advanced Sampling & Survey Methodology</h3><p className="muted">This score and competency update were computed live by the FastAPI AssessmentService, not simulated in the browser.</p><a href="/learning-path" className="btn btn-primary">Open Learning Path</a></div></div></AppShell>;
    }
    return <AppShell><div className="page-title"><div><h1>Assessment Complete</h1><p>Your results are ready and can be fed back into the competency engine.</p></div><span className="status">8 / 10</span></div><div className="split"><div className="panel panel-pad"><div className="section-label">Competency performance</div><div className="score-matrix"><div className="score-chip"><span>Python</span><strong>74%</strong></div><div className="score-chip"><span>Sampling</span><strong>58%</strong></div><div className="score-chip"><span>Data Visualization</span><strong>82%</strong></div><div className="score-chip"><span>APIs</span><strong>71%</strong></div></div><div className="spacer16"/><div className="why-box"><strong>Competency update</strong><p>Sampling Methods is now estimated at Level 3 in the demo scenario, subject to the platform&apos;s evidence and validation policy.</p></div></div><div className="panel panel-pad"><div className="section-label">Recommended reinforcement</div><h3 style={{marginTop:0}}>Advanced Sampling & Survey Methodology</h3><p className="muted">Your result indicates a reinforcement need in sampling design.</p><a href="/learning-path" className="btn btn-primary">Open Learning Path</a></div></div></AppShell>;
  }

  return <AppShell><div className="page-title"><div><h1>Official Statistics Diagnostic Assessment</h1><p>Question {idx+1} of {questions.length} · {live?'Live backend-graded assessment':'Adaptive assessment demo'}</p></div><span className="status">20 min</span></div><div className="panel panel-pad"><div className="progressline"><i style={{width:`${((idx+1)/questions.length)*100}%`}}/></div><div className="spacer24"/><div className="qhead"><div className="qtag"><span className="tag">{q.competency}</span><span className="tag">{q.difficulty}</span></div><span className="subtle">Question {idx+1}/{questions.length}</span></div><h2 style={{fontSize:22,lineHeight:1.45}}>{q.text}</h2><div className="options">{q.options.map(o=><label key={o.key} className={selectedKey===o.key?'option correct':'option'}><input type="radio" name="q" checked={selectedKey===o.key} onChange={()=>setAnswers(a=>({...a,[q.id]:o.key}))}/> {o.key}. {o.text}</label>)}</div><div className="spacer24"/><div className="action-row"><button className="btn btn-secondary" disabled={idx===0} onClick={()=>setIdx(Math.max(0,idx-1))}>Previous</button>{idx<questions.length-1?<button className="btn btn-primary" disabled={!selectedKey} onClick={()=>setIdx(idx+1)}>Next Question</button>:<button className="btn btn-primary" disabled={!selectedKey||submitting} onClick={submit}>{submitting?'Submitting…':'Submit Assessment'}</button>}</div><div className="spacer16"/><div className="source"><strong>Assessment design:</strong> {live?'Questions and grading are served live by the FastAPI backend (sanitized on the wire; scored server-side on submit).':'adaptive question selection should be driven by the backend; this prototype demonstrates the learner experience.'}</div></div></AppShell>;
}
