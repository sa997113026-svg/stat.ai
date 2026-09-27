import './globals.css';
import type { Metadata } from 'next';
export const metadata:Metadata={title:'StatSaksham AI | Skill Intelligence for Official Statistics',description:'AI-enabled competency assessment, skill-gap analysis, personalized learning and intelligent assessments for India\'s Official Statistical System.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
