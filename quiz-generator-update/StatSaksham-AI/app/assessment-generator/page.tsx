'use client';
import AppShell from '../../components/AppShell';
import {useRef, useState} from 'react';
import {generateAssessment, generateQuizFromText} from '../../lib/services';
import {isLiveMode} from '../../lib/apiClient';
import {Question} from '../../types';

const COMPETENCIES = ['General','Sampling Methods','Python for Statistical Computing','Data Visualization','APIs & Open Data (SDMX)','Labour Force Frameworks','Data Quality Assurance'];
const MIN_CHARS = 100;

export default function AssessmentGenerator(){
  const [text,setText]=useState('');
  const [fileName,setFileName]=useState('');
  const [num,setNum]=useState('5');
  const [difficulty,setDifficulty]=useState('Medium');
  const [competency,setCompetency]=useState('General');
  const [processing,setProcessing]=useState(false);
  const [error,setError]=useState('');
  const [engine,setEngine]=useState('');
  const [qs,setQs]=useState<Question[]|null>(null);
  const fileRef=useRef<HTMLInputElement>(null);

  const words=text.trim()?text.trim().split(/\s+/).length:0;

  const readFile=async(file:File)=>{
    setError('');
    if(!/\.(txt|md|csv|json)$/i.test(file.name)){
      setError('Only text-based files (.txt, .md, .csv, .json) can be read in the browser. For PDF/DOCX, copy the text and paste it below.');
      return;
    }
    setText(await file.text());
    setFileName(file.name);
  };

  const run=async()=>{
    setError('');
    if(text.trim().length<MIN_CHARS){setError(`Please provide at least ${MIN_CHARS} characters of learning material (upload a .txt file or paste text).`);return}
    setProcessing(true);
    try{
      const res=await generateQuizFromText({text,numQuestions:Number(num),difficulty,competency,title:fileName||'Pasted learning material'});
      setQs(res.questions);setEngine(res.engine);
    }catch(e){
      setError(e instanceof Error?e.message:'Generation failed. Is the backend running?');
    }
    setProcessing(false);
  };

  const loadSample=async()=>{setProcessing(true);setError('');setQs(await generateAssessment());setEngine('sample');setProcessing(false)};

  return <AppShell><div className="page-title"><div><h1>AI Assessment Studio</h1><p>Upload approved learning material, generate traceable objective assessments, then route them through human review.</p></div><span className="status">{isLiveMode()?'Live quiz generator':'Backend required'}</span></div><div className="split"><div className="panel panel-pad"><div className="section-label">01 · Upload or paste</div><div className="upload" onDragOver={e=>e.preventDefault()} onDrop={e=>{e.preventDefault();const f=e.dataTransfer.files?.[0];if(f)readFile(f)}}><div className="upload-icon">⇧</div><h3>{fileName?fileName:'Drop learning material here'}</h3><p>.txt · .md · .csv · .json (PDF/DOCX: paste the text below)</p><input ref={fileRef} type="file" accept=".txt,.md,.csv,.json" style={{display:'none'}} onChange={e=>{const f=e.target.files?.[0];if(f)readFile(f)}}/><button className="btn btn-secondary" onClick={()=>fileRef.current?.click()}>Choose file</button></div><div className="spacer16"/><textarea value={text} onChange={e=>{setText(e.target.value);setFileName('')}} placeholder="…or paste your learning material here (at least a few sentences)" rows={6} style={{width:'100%',padding:12,borderRadius:10,border:'1px solid var(--line, #d5dee6)',font:'inherit',resize:'vertical'}}/><div className="subtle">{words} words · {text.length.toLocaleString()} characters</div></div><div className="panel panel-pad"><div className="section-label">02 · Configure</div><div className="form-grid"><div className="field"><label>Questions</label><select value={num} onChange={e=>setNum(e.target.value)}>{['3','5','8','10','15'].map(n=><option key={n}>{n}</option>)}</select></div><div className="field"><label>Difficulty</label><select value={difficulty} onChange={e=>setDifficulty(e.target.value)}>{['Easy','Medium','Hard'].map(n=><option key={n}>{n}</option>)}</select></div><div className="field"><label>Question type</label><select disabled><option>MCQ</option></select></div><div className="field"><label>Competency</label><select value={competency} onChange={e=>setCompetency(e.target.value)}>{COMPETENCIES.map(n=><option key={n}>{n}</option>)}</select></div><div className="field"><label>Language</label><select disabled><option>English</option></select></div><div className="field"><label>Review policy</label><select disabled><option>Trainer approval required</option></select></div></div><div className="spacer16"/><button className="btn btn-primary" onClick={run} disabled={processing}>{processing?'Generating assessment…':'Generate Assessment'}</button> <button className="btn btn-secondary" onClick={loadSample} disabled={processing}>Load sample question bank</button>{error&&<p style={{color:'#b3261e',marginTop:12}}>{error}</p>}</div></div><div className="spacer24"/><div className="panel panel-pad"><div className="section-label">03 · Understand</div><div className="score-matrix"><div className="score-chip"><span>Words in material</span><strong>{words}</strong></div><div className="score-chip"><span>Questions generated</span><strong>{qs?qs.length:0}</strong></div><div className="score-chip"><span>Engine</span><strong>{engine==='claude'?'Claude AI':engine==='heuristic'?'Rule-based':engine==='sample'?'Sample bank':'—'}</strong></div><div className="score-chip"><span>Competency</span><strong>{competency}</strong></div></div>{engine==='heuristic'&&<p className="subtle" style={{marginTop:12}}>Rule-based mode creates fill-in-the-blank questions. Add an ANTHROPIC_API_KEY on the backend for full AI-written questions.</p>}</div>{qs&&<><div className="spacer24"/><div className="section-head"><div><h2 style={{margin:0}}>Generated questions</h2><p>Each item includes source traceability and confidence. Review before publication.</p></div></div><div className="questions">{qs.map(q=><div className="question-card" key={q.id}><div className="qhead"><div className="qtag"><span className="tag">{q.competency}</span><span className="tag">{q.difficulty}</span><span className="tag">AI Generated</span></div><span className="subtle">Confidence {q.confidence}%</span></div><h3>{q.question}</h3><div className="options">{q.options.map((o,i)=><div className={i===q.answer?'option correct':'option'} key={i}>{String.fromCharCode(65+i)}. {o}</div>)}</div><div className="source"><strong>Source:</strong> {q.source} · <strong>Answer:</strong> {q.options[q.answer]} · <strong>Explanation:</strong> {q.explanation}</div></div>)}</div></>}</AppShell>;
}
