import Sidebar from './Sidebar';
import Header from './Header';
export default function AppShell({children}:{children:React.ReactNode}){return <><Header/><div className="app-frame"><Sidebar/><div className="app-content" id="main">{children}</div></div></>}
