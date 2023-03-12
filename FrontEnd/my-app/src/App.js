import './App.css';
import { useState } from 'react';

function App() {
    const [value, setValue] = useState('');


    const handleChange = (event) => {
        setValue(event.target.value);
    };


    return (
        <div className="App">
            <header style={{ backgroundColor: '#1E90FF', color: 'white', padding: '20px' }}>
                <h1 style={{ margin: '0' }}>Research AI</h1>
            </header>
            <div className="outerBox">
                <button className="btn-1">Evaluate</button>
                <button className="btn-1">Criticize</button>
                <button className="btn-1">Support</button>
            </div>
            <div className="main-input-div">
                <input className="main-input" type="text" value={value} onChange={handleChange} />
                <p>You typed: {value}</p>
            </div>
        </div>
    );
}

export default App;
