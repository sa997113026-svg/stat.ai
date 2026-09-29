'use client';
import Link from 'next/link';
import {usePathname} from 'next/navigation';
const items=[['/dashboard','Overview'],['/competency','My Competency'],['/skill-gaps','Skill Gaps'],['/learning-path','Learning Path'],['/videos','Training Videos'],['/assessment-generator','AI Assessment'],['/assessment','Take Assessment'],['/admin/dashboard','Workforce Analytics'],['/integrations/igot','iGOT Integration']];
export default function Sidebar(){const path=usePathname();return <aside className="sidebar"><div className="side-label">STATSAKSHAM AI</div><div className="side-role">Learner / Official</div>{items.map(([href,label])=><Link key={href} className={path===href?'active':''} href={href}><span>{icon(label)}</span>{label}</Link>)}<div className="side-note"><strong>Demo mode</strong><span>Fictional data</span></div></aside>}
function icon(label:string){const map:any={'Overview':'⌂','My Competency':'◎','Skill Gaps':'△','Learning Path':'→','Training Videos':'▶','AI Assessment':'✓','Take Assessment':'□','Workforce Analytics':'▥','iGOT Integration':'↗'};return map[label]||'•'}
