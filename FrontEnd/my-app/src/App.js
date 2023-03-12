import './App.css';
import { useState, useEffect } from 'react';
import Tree from 'react-d3-tree';
import './custom-tree.css'

var argMap = new Map();

function App() {
    const [value, setValue] = useState('');
    const [queryResponse, setQueryResponse] = useState('');
    const [showTree, setShowTree] = useState(true);

    function OnEvaluate() {
        useEffect(() => {
            fetch("http://localhost:5000/evaluate?prompt="+value)
            .then(response => response.json()
            .then(data => {
                console.log(data);
                setQueryResponse(data);
                setShowTree(false);
            })
            );
        },[]);
        
    }

    function CreateTree(show) {
        if (show)
            return
        var argTree = {
            name: "P: " + "start",
            children: []
        };

        queryResponse["refuting_arguments"].forEach((arg) => {
            argTree.children.push({name: "R: " + arg.tagline, children: []});
            argMap.set("R: " + arg.tagline, {desc: arg.argument, link: arg.urls[0]});
        });
        queryResponse["supporting_arguments"].forEach((arg) => {
            argTree.children.push({name: "S: " + arg.tagline, children: []});
            argMap.set("S: " + arg.tagline, {desc: arg.argument, link: arg.urls[0]});
        });

        return (
            <div id="treeWrapper" style={{ width: '100em', height: '100em', align: 'center'}}>
            <Tree data={argTree} 
                
                orientation='vertical'
                rootNodeClassName="node__root"
                onNodeClick={(nodeData, evt) => {
                    if (nodeData.data.children.length != 0)
                        console.log(`Toggle children`);
                    else
                        console.log(`Create More`);
                    }}
                onNodeMouseOver={(nodeData, evt) => {
                    if (nodeData.data.children.length != 0)
                        console.log(`Toggle children`);
                    else
                        console.log(`Create More`);             
                    }}
            />
            </div>
        );
        }

    const handleChange = (event) => {
        setValue(event.target.value);
    };

    return (
        <div className="App">
            <header style={{ backgroundColor: '#1E90FF', color: 'white', padding: '20px' }}>
                <h1 style={{ margin: '0' }}>Research AI</h1>
            </header>
            <div className="outerBox">
                <button className="btn-1" onClick={() => OnEvaluate}>Evaluate</button>
                <button className="btn-1">Criticize</button>
                <button className="btn-1">Support</button>
            </div>
            <div className="main-input-div">
                <input className="main-input" type="text" value={value} onChange={handleChange} />
                <p>You typed: {value}</p>
            </div>
            
            <CreateTree show={showTree}/>
            
        </div>
        
    );
}





export default App;

