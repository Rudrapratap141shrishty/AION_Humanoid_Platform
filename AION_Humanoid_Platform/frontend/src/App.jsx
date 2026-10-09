import React, { useEffect, useState } from 'react';

const categories = [
  'all', 'humanoid', 'manipulation', 'locomotion', 'perception',
  'digital-twin', 'ros2', 'speech', 'ai-planning', 'safety'
];

export default function App() {
  const [robots, setRobots] = useState([]);
  const [category, setCategory] = useState('all');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('Connecting to services…');
  const [command, setCommand] = useState('show robot status');
  const [commandResult, setCommandResult] = useState('');

  async function loadRobots() {
    try {
      const url = category === 'all' ? '/api/robots' : `/api/robots?category=${encodeURIComponent(category)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`API returned ${response.status}`);
      setRobots(await response.json());
      setStatus('Backend connected');
    } catch (e) {
      setStatus(`Backend unavailable: ${e.message}`);
    }
  }

  useEffect(() => { loadRobots(); }, [category]);

  async function createRobot(e) {
    e.preventDefault();
    try {
      const response = await fetch('/api/robots', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category: category === 'all' ? 'humanoid' : category, description })
      });
      if (!response.ok) throw new Error(await response.text());
      setName(''); setDescription('');
      await loadRobots();
    } catch (e) {
      setStatus(`Create failed: ${e.message}`);
    }
  }

  async function runCommand(e) {
    e.preventDefault();
    try {
      const response = await fetch('/ai/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: command })
      });
      const data = await response.json();
      setCommandResult(JSON.stringify(data, null, 2));
    } catch (e) {
      setCommandResult(`AI service unavailable: ${e.message}`);
    }
  }

  return <main className="shell">
    <header className="topbar">
      <div><div className="eyebrow">ROBOTICS · AI · DIGITAL TWIN</div><h1>AION <span>Humanoid Platform</span></h1></div>
      <div className="status"><i />{status}</div>
    </header>

    <section className="hero">
      <div>
        <p className="eyebrow">UNIFIED ROBOT DEVELOPMENT WORKSPACE</p>
        <h2>Build, observe and orchestrate<br />the next generation of robots.</h2>
        <p className="muted">A starter control plane for projects, visualization and safe AI-assisted workflows.</p>
        <div className="actions">
          <a className="button primary" href="http://localhost:8082" target="_blank" rel="noreferrer">Open 3D Viser Scene ↗</a>
          <button className="button" onClick={loadRobots}>Refresh projects</button>
        </div>
      </div>
      <div className="orb"><div className="orb-ring ring1" /><div className="orb-ring ring2" /><div className="orb-core">AION<br/><small>ROBOT OS</small></div></div>
    </section>

    <section className="stats">
      <div className="stat"><span>01</span><b>Robot projects</b><strong>{robots.length}</strong><small>Loaded from API</small></div>
      <div className="stat"><span>02</span><b>Service architecture</b><strong>4 layers</strong><small>UI · API · AI · Data</small></div>
      <div className="stat"><span>03</span><b>Visualization</b><strong>3D scene</strong><small>Viser scene service</small></div>
      <div className="stat"><span>04</span><b>Control safety</b><strong>Simulation</strong><small>No physical actuation</small></div>
    </section>

    <section className="grid">
      <article className="panel wide">
        <div className="panel-head"><div><p className="eyebrow">WORKSPACE</p><h3>Robot projects</h3></div>
          <select value={category} onChange={e => setCategory(e.target.value)}>
            {categories.map(c => <option key={c} value={c}>{c === 'all' ? 'All categories' : c}</option>)}
          </select>
        </div>
        <form className="create-form" onSubmit={createRobot}>
          <input value={name} onChange={e => setName(e.target.value)} placeholder="Project name" required maxLength="120" />
          <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Short description" maxLength="1000" />
          <button className="button primary">Add project</button>
        </form>
        <div className="project-list">
          {robots.map(r => <div className="project" key={r.id}>
            <div className="project-icon">◇</div><div className="project-info"><b>{r.name}</b><small>{r.description || 'No description yet'}</small></div>
            <span className="tag">{r.category}</span><button className="delete" onClick={async () => { await fetch(`/api/robots/${r.id}`, {method:'DELETE'}); loadRobots(); }}>×</button>
          </div>)}
          {robots.length === 0 && <div className="empty">No projects yet. Create your first robot project above.</div>}
        </div>
      </article>

      <article className="panel">
        <p className="eyebrow">AI AUTOMATION</p><h3>Command console</h3>
        <p className="muted">Text command router with allowlisted browser automation hooks.</p>
        <form onSubmit={runCommand} className="command-form">
          <input value={command} onChange={e => setCommand(e.target.value)} placeholder="Try: show visualization" />
          <button className="button primary">Run</button>
        </form>
        <pre className="result">{commandResult || 'Command results will appear here.'}</pre>
        <div className="chips"><span>SpeechRecognition API</span><span>Selenium</span><span>webbrowser</span></div>
      </article>
    </section>

    <section className="category-section">
      <p className="eyebrow">ROBOTICS MODULES</p><h3>All development categories</h3>
      <div className="category-grid">
        {[
          ['01','Humanoid','URDF, joints, kinematics'],
          ['02','Manipulation','Hands, grippers, motion planning'],
          ['03','Locomotion','Balance, gait, foot contacts'],
          ['04','Perception','Camera, depth, LiDAR, SLAM'],
          ['05','Digital twin','Scene state and telemetry'],
          ['06','ROS 2','Topics, services, actions'],
          ['07','Voice & HRI','Speech, intent, dialogue'],
          ['08','AI planning','Task planning and policies'],
          ['09','Safety','E-stop, limits, audit trail']
        ].map(([n,t,d]) => <div className="category-card" key={n}><span>{n}</span><h4>{t}</h4><p>{d}</p></div>)}
      </div>
    </section>
    <footer> AION starter · secure physical robot control is intentionally not enabled.</footer>
  </main>;
}
