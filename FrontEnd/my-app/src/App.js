import './App.css';
import {useState, useEffect} from 'react';
import { Audio } from 'react-loader-spinner'


function App() {
    const [value, setValue] = useState('');
    const [responseBool, setResponseBool] = useState(false);
    const [isLoader, setIsLoader] = useState(false);


    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const clickHandler = async () => {
        setIsLoader(true);
        setResponseBool(false);
        const timer = setTimeout(() => {
            setIsLoader(false);
            setResponseBool(true)
        }, 5000);
    }

    const OnEvaluate = () => {
        const prompt = "hello";
        fetch("http://localhost:5000/evaluate? ="+prompt)
            .then(response => response.json()
                .then(data => {
                    console.log(data)
                })
            );
    }

    return (
        <div className="App">
            <header style={{backgroundColor: '#1E90FF', color: 'white', padding: '20px'}}>
                <h1 style={{margin: '0'}}>Research AI</h1>
            </header>
            <div className="outerBox">
                <button className="btn-1" onClick={clickHandler}>Evaluate</button>
                <button className="btn-1">Criticize</button>
                <button className="btn-1">Support</button>
            </div>
            <div className="main-input-div">
                <input className="main-input" type="text" value={value} onChange={handleChange}/>
                <p>You typed: {value}</p>
            </div>
            {
                responseBool ? (
                    <p>KAHSVCIASHC KASJCB</p>
                ) : isLoader ? (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                        <Audio
                            height="80"
                            width="80"
                            radius="9"
                            color="green"
                            ariaLabel="loading"
                            style={{
                                justifyContent:'center'
                            }}
                        />
                    </div>
                ) : null
            }
        </div>

    );
}

export default App;
