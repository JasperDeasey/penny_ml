import { Link } from 'react-scroll';
import './NavBar.css';

const NavBar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="overview" smooth={true} duration={500}>Overview</Link></li>
        <li><Link to="investment-strategy" smooth={true} duration={500}>Strategy</Link></li>
        <li><Link to="performance" smooth={true} duration={500}>Performance</Link></li>
        <li><Link to="risk" smooth={true} duration={500}>Risk</Link></li>
        <li><Link to="limitations" smooth={true} duration={500}>Limitations</Link></li>
        <li><Link to="contact" smooth={true} duration={500}>Contact</Link></li>
      </ul>
    </nav>
  );
};

export default NavBar;