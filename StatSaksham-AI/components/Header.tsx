'use client';
import Link from 'next/link';
import {useState} from 'react';

export default function Header(){
  const [open,setOpen]=useState(false);
  return <>
    <div className="utility"><div className="container utility-inner"><span><a href="#main">Skip to Main Content</a></span><span>Screen Reader Access</span><span>Accessibility</span><span className="push">English ▾</span><span>Help</span></div></div>
    <header className="header"><div className="container header-inner">
      <Link href="/" className="brand" aria-label="StatSaksham AI home"><span className="brand-mark"><i></i><i></i><i></i></span><span><strong>StatSaksham AI</strong><small>AI Skill Intelligence for Official Statistics</small></span></Link>
      <button className="menu-btn" onClick={()=>setOpen(v=>!v)} aria-expanded={open}>☰</button>
      <nav className={open?'nav open':'nav'}>
        <Link href="/">Home</Link><Link href="/competency">Competency</Link><Link href="/learning-path">Learning</Link><Link href="/assessment-generator">Assessment</Link><Link href="/admin/dashboard">Analytics</Link><Link href="/integrations/igot">Integrations</Link>
        <Link href="/dashboard" className="header-login">Login / Demo</Link>
      </nav>
    </div></header>
  </>
}
