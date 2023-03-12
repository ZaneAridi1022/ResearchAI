import './App.css';
import { useState, useEffect } from 'react';
import Tree from 'react-d3-tree';
import './custom-tree.css'

var argMap = new Map();

function App() {
    const [value, setValue] = useState('');
    const [query, setQuery] = useState('');

    const handleChange = (event) => {
        setValue(event.target.value);
    };


    return (
        <div className="App">
            <header style={{ backgroundColor: '#1E90FF', color: 'white', padding: '20px' }}>
                <h1 style={{ margin: '0' }}>Research AI</h1>
            </header>
            <div className="outerBox">
                <button className="btn-1" onClick={() => OnEvaluate({value})}>Evaluate</button>
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

function OnEvaluate({value}) {
    if (value)
    {
        const prompt = "hello";
        fetch("http://localhost:5000/evaluate?prompt="+value)
        .then(response => response.json()
        .then(data => {
            console.log(data)
        })
        );
    }
    
}

function CreateTree() {
    var argTree = {
        name: "P: " + "start",
        children: []
    };
    const rec = {
    "refuting_arguments": [
    {
      "argument": "The practice of tax cuts for the wealthy and businesses has been implemented in the past with little to no evidence of trickle down effects. Tax cuts in the 1980s and 2000s resulted in little economic growth or job creation.",
      "tagline": "Lack of evidence in practice",
      "urls": [
        "https://www.thebalancemoney.com/trickle-down-economics-theory-effect-does-it-work-3305572",
        "https://taxfoundation.org/reviewing-recent-evidence-effect-taxes-economic-growth/"
      ]
    },
    {
      "argument": "Trickle down economics benefits only the wealthy, as the tax cut disproportionately benefits them. The working class receives none of the benefits that trickle down claims to provide.",
      "tagline": "Benefits only the wealthy",
      "urls": [
        "https://www.lse.ac.uk/research/research-for-the-world/economics/tax-cuts-for-the-wealthy-only-benefit-the-rich-debunking-trickle-down-economics",
        "https://www.thebalancemoney.com/trickle-down-economics-theory-effect-does-it-work-3305572"
      ]
    },
    {
      "argument": "Trickle down economics leads to increased income inequality since the wealthy will receive a large share of the tax breaks while the working class receives none of the benefits. This disparity leads to a further divide between the rich and the poor.",
      "tagline": "Increased income inequality",
      "urls": [
        "https://www.thebalancemoney.com/trickle-down-economics-theory-effect-does-it-work-3305572",
        "https://www.salon.com/2020/12/27/50-year-study-of-tax-cuts-on-wealthy-shows-they-always-fail-to-trickle-down/",
      ]
    }
  ],
  "supporting_arguments": [
    {
      "argument": "Trickle down economics argues that by reducing taxes on the wealthy and businesses, they will have more disposable income which they will use to invest in their businesses, create jobs, and grow the economy. This increased economic activity will then benefit everyone in society.",
      "tagline": "Incentive to invest and grow the economy",
      "urls": [
        "https://www.thebalancemoney.com/trickle-down-economics-theory-effect-does-it-work-3305572",
        "https://www.economicsonline.co.uk/definitions/trickle-down-economics-why-it-only-works-in-theory.html/"
      ]
    },
    {
      "argument": "Lower taxes on the wealthy and businesses create an incentive for entrepreneurship. Entrepreneurs can take advantage of the tax break and use the saved money to fund their business ventures, creating new jobs and opportunities.",
      "tagline": "Encourages entrepreneurship",
      "urls": [
        "https://link.springer.com/article/10.1007/s00712-013-0375-z",
        "https://www.iedm.org/84452-entrepreneurship-and-fiscal-policy-how-taxes-affect-entrepreneurial-activity/"
      ]
    },
    {
      "argument": "Trickle down economists argue that lower tax rates lead to increased economic growth since businesses and individuals have more money to invest in the economy, which creates more jobs and results in higher economic growth.",
      "tagline": "Lower tax rates lead to increased economic growth",
      "urls": [
        "https://www.brookings.edu/wp-content/uploads/2016/06/09_Effects_Income_Tax_Changes_Economic_Growth_Gale_Samwick.pdf",
        "https://www.brookings.edu/research/effects-of-income-tax-changes-on-economic-growth/"
      ]
    }
  ],
  "topic": "Trickle Down Economics"
}
    rec["refuting_arguments"].forEach((arg) => {
        argTree.children.push({name: "R: " + arg.tagline, children: []});
        argMap.set("R: " + arg.tagline, {desc: arg.argument, link: arg.urls[0]});
    });
    rec["supporting_arguments"].forEach((arg) => {
        argTree.children.push({name: "S: " + arg.tagline, children: []});
        argMap.set("S: " + arg.tagline, {desc: arg.argument, link: arg.urls[0]});
    });
  

    

return (
    <div id="treeWrapper" style={{ width: '100em', height: '100em', align: 'center'}}>
      <Tree data={argTree} 
        
        orientation='vertical'
        pathClassFunc={classifyPosOrNeg}
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

export default App;

