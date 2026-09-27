import Header from './Header';
import Footer from './Footer';
export default function LayoutShell({children}:{children:React.ReactNode}){return <><Header/><main id="main">{children}</main><Footer/></>}
