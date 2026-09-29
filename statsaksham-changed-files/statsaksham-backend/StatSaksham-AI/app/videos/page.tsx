'use client';
import {useState} from 'react';
import AppShell from '../../components/AppShell';
import VideoPlayer, {toEmbed} from '../../components/VideoPlayer';
import {videos} from '../../data/videos';

export default function VideosPage(){
  const firstPlayable=videos.find(v=>toEmbed(v.url).kind!=='none');
  const [activeId,setActiveId]=useState<string>((firstPlayable??videos[0])?.id??'');
  const active=videos.find(v=>v.id===activeId);

  return <AppShell>
    <div className="page-title"><div><h1>Training Videos</h1><p>Short lessons mapped to your competency gaps.</p></div><span className="status">{videos.filter(v=>toEmbed(v.url).kind!=='none').length} of {videos.length} available</span></div>
    {active&&<div className="panel panel-pad"><VideoPlayer url={active.url} title={active.title}/><div className="spacer16"/><div className="section-label">{active.competency}</div><h3 style={{margin:0}}>{active.title}</h3></div>}
    <div className="spacer24"/>
    <div className="course-grid">{videos.map(v=>{
      const ready=toEmbed(v.url).kind!=='none';
      return <div className="course-card" key={v.id}><div className="course-banner"/><div className="course-body">
        <div className="course-top"><span>{v.competency}</span><span>{ready?'Ready':'Link needed'}</span></div>
        <h3>{v.title}</h3>
        {v.duration&&<p>{v.duration}</p>}
        <div className="course-footer"><span/><button className="btn btn-primary" disabled={!ready} onClick={()=>{setActiveId(v.id);window.scrollTo({top:0,behavior:'smooth'})}}>{ready?'Play':'Not available'}</button></div>
      </div></div>})}
    </div>
  </AppShell>;
}
