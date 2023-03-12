import './App.css';
import { useState, useEffect } from 'react';
import Tree from 'react-d3-tree';
import './custom-tree.css'

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
                <button className="btn-1" onClick={OnEvaluate}>Evaluate</button>
                <button className="btn-1">Criticize</button>
                <button className="btn-1">Support</button>
            </div>
            <div className="main-input-div">
                <input className="main-input" type="text" value={value} onChange={handleChange} />
                <p>You typed: {value}</p>
            </div>
            
            <CreateTree />
            
        </div>
        
    );
}

function OnEvaluate() {

    const prompt = "hello";
    fetch("http://localhost:5000/evaluate?prompt="+prompt)
    .then(response => response.json()
    .then(data => {
        console.log(data)
    })
    );
}

function CreateTree() {
  const orgChart = {
  name: 'CEO',
  children: [
    {
      name: 'Manager',
      children: [
        {
          name: 'Foreman',
          children: [
            {
              name: 'Worker',
            },
          ],
        },
        {
          name: 'Foreman',
          children: [
            {
              name: 'Worker',
            },
          ],
        },
      ],
    },
  ],
};

return (
    <div id="treeWrapper" style={{ width: '100em', height: '100em', align: 'center'}}>
      <Tree data={orgChart} 
        rootNodeClassName="node__root"
        branchNodeClassName="node__branch"
        leafNodeClassName="node__leaf"/>
    </div>
);
}

export default App;
