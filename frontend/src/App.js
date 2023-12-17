import logo from './logo.svg';
import './App.css';
import ReturnsChart from './components/ReturnsChart'
import NavBar from './components/NavBar';
import Overview from './sections/Overview';
import InvestmentStrategy from './sections/InvestmentStrategy';
import Performance from './sections/Performance';
import Risk from './sections/Risk';
import Implementation from './sections/Implementation';
import Contact from './sections/Contact';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <NavBar />
        <Overview />
        <InvestmentStrategy />
        <Performance />
        <Risk />
        <Implementation />
        <Contact />
      </header>
    </div>
  );
}

export default App;
