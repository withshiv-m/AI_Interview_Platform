import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  LayoutDashboard, BriefcaseBusiness, Users, FileUp, Play, Search,
  Trash2, Eye, ChevronRight, RefreshCw, CheckCircle2, AlertTriangle,
  XCircle, Sparkles, Menu, X, Plus, UploadCloud, FileText, Activity,
  GraduationCap, Award, Mail, Phone, ArrowLeft, SlidersHorizontal
} from "lucide-react";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function api(path, options = {}) {
  const res = await fetch(`${API}${path}`, options);
  const body = await res.json().catch(() => ({}));
  if (!res.ok || body.success === false) {
    throw new Error(body.message || body.detail?.message || `Request failed (${res.status})`);
  }
  return body.data;
}

const pct = (n) => `${Number(n || 0).toFixed(0)}%`;
const scoreClass = (n) => Number(n) >= 80 ? "excellent" : Number(n) >= 60 ? "good" : Number(n) >= 40 ? "medium" : "low";

function App() {
  const [page, setPage] = useState("dashboard");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [results, setResults] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const notify = (message, type = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  const loadAll = async () => {
    setLoading(true);
    try {
      const [j, c] = await Promise.all([api("/api/jobs"), api("/api/candidates")]);
      setJobs(j || []);
      setCandidates(c || []);
    } catch (e) {
      notify(e.message, "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadAll(); }, []);

  const openCandidate = async (id) => {
    setLoading(true);
    try {
      const c = await api(`/api/candidates/${id}`);
      setSelectedCandidate(c);
      setPage("candidate-detail");
    } catch (e) { notify(e.message, "error"); }
    finally { setLoading(false); }
  };

  const runScreening = async (job) => {
    setSelectedJob(job);
    setLoading(true);
    try {
      const data = await api(`/api/matching/run/${job.job_id}`, { method: "POST" });
      setResults(data.results || []);
      setPage("screening");
      notify(`Screened ${data.results?.length || 0} candidates`);
    } catch (e) { notify(e.message, "error"); }
    finally { setLoading(false); }
  };

  const deleteJob = async (id) => {
    if (!confirm("Delete this job and its screening records?")) return;
    try {
      await api(`/api/jobs/${id}`, { method: "DELETE" });
      notify("Job deleted");
      await loadAll();
    } catch (e) { notify(e.message, "error"); }
  };

  const deleteCandidate = async (id) => {
    if (!confirm("Delete this candidate?")) return;
    try {
      await api(`/api/candidates/${id}`, { method: "DELETE" });
      notify("Candidate deleted");
      await loadAll();
    } catch (e) { notify(e.message, "error"); }
  };

  const nav = [
    ["dashboard", "Dashboard", LayoutDashboard],
    ["jobs", "Jobs", BriefcaseBusiness],
    ["candidates", "Candidates", Users],
    ["upload", "Upload Resumes", FileUp],
  ];

  const navigate = (p) => {
    setPage(p);
    setMobileOpen(false);
    if (p !== "candidate-detail") setSelectedCandidate(null);
  };

  return (
    <div className="app">
      <aside className={`sidebar ${mobileOpen ? "open" : ""}`}>
        <div className="brand">
          <div className="brand-mark"><Sparkles size={19}/></div>
          <div><strong>HireMind</strong><span>AI Screening</span></div>
          <button className="mobile-close" onClick={() => setMobileOpen(false)}><X/></button>
        </div>
        <div className="nav-label">WORKSPACE</div>
        <nav>
          {nav.map(([key, label, Icon]) => (
            <button key={key} className={page === key ? "nav-item active" : "nav-item"} onClick={() => navigate(key)}>
              <Icon size={18}/><span>{label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="api-status"><span className="dot"/> API connected</div>
          <small>PS03 • Multi-Agent Recruitment</small>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <button className="mobile-menu" onClick={() => setMobileOpen(true)}><Menu/></button>
          <div>
            <h1>{page === "dashboard" ? "Recruitment Dashboard" :
                page === "jobs" ? "Job Management" :
                page === "candidates" ? "Candidates" :
                page === "upload" ? "Resume Upload" :
                page === "screening" ? "AI Screening Results" : "Candidate Profile"}</h1>
            <p>{page === "dashboard" ? "Find the best candidates with multi-agent AI." :
              "Manage your recruitment workflow from one place."}</p>
          </div>
          <button className="icon-btn" onClick={loadAll} title="Refresh"><RefreshCw size={18}/></button>
        </header>

        <section className="content">
          {page === "dashboard" && <Dashboard jobs={jobs} candidates={candidates} onJobs={() => navigate("jobs")} onCandidates={() => navigate("candidates")} onUpload={() => navigate("upload")} onScreen={runScreening} loading={loading}/>}
          {page === "jobs" && <Jobs jobs={jobs} onCreate={() => navigate("create-job")} onDelete={deleteJob} onScreen={runScreening} onView={setSelectedJob}/>}
          {page === "create-job" && <CreateJob onDone={async () => { await loadAll(); navigate("jobs"); notify("Job created successfully"); }} onCancel={() => navigate("jobs")} notify={notify}/>}
          {page === "candidates" && <Candidates candidates={candidates} onOpen={openCandidate} onDelete={deleteCandidate}/>}
          {page === "upload" && <Upload onDone={async () => { await loadAll(); navigate("candidates"); }} notify={notify}/>}
          {page === "screening" && <Screening job={selectedJob} results={results} onBack={() => navigate("jobs")} onCandidate={openCandidate}/>}
          {page === "candidate-detail" && <CandidateDetail candidate={selectedCandidate} result={results.find(r => r.candidate_id === selectedCandidate?.candidate_id)} onBack={() => navigate("candidates")}/>}
        </section>
      </main>
      {toast && <div className={`toast ${toast.type}`}><CheckCircle2 size={18}/>{toast.message}</div>}
    </div>
  );
}

function Dashboard({ jobs, candidates, onJobs, onCandidates, onUpload, onScreen, loading }) {
  const recent = jobs.slice(0, 3);
  return <div>
    <div className="hero">
      <div><div className="eyebrow"><Sparkles size={14}/> AI-POWERED RECRUITING</div>
        <h2>Screen smarter.<br/><span>Hire faster.</span></h2>
        <p>Upload resumes, define a job, and let the multi-agent pipeline rank candidates automatically.</p>
        <div className="hero-actions"><button className="primary" onClick={onUpload}><UploadCloud size={17}/> Upload resumes</button><button className="secondary" onClick={onJobs}>Manage jobs</button></div>
      </div>
      <div className="hero-orbit"><div className="orbit-card"><Sparkles size={26}/><strong>Multi-Agent AI</strong><span>Resume → Match → Skill Gap → Recruiter</span></div></div>
    </div>

    <div className="stats">
      <Stat icon={BriefcaseBusiness} label="Active Jobs" value={jobs.length} />
      <Stat icon={Users} label="Candidates" value={candidates.length} />
      <Stat icon={FileText} label="Resumes Processed" value={candidates.length} />
      <Stat icon={Activity} label="Screening Ready" value={jobs.length && candidates.length ? "YES" : "—"} />
    </div>

    <div className="section-head"><div><h3>Quick actions</h3><p>Start your recruitment workflow.</p></div></div>
    <div className="quick-grid">
      <ActionCard icon={Plus} title="Create a job" text="Add a job description and extract requirements." onClick={onJobs}/>
      <ActionCard icon={UploadCloud} title="Upload resumes" text="Process PDF or DOCX resumes with the Resume Agent." onClick={onUpload}/>
      <ActionCard icon={Play} title="Run AI screening" text="Rank every candidate against a selected job." onClick={onJobs}/>
    </div>

    <div className="section-head"><div><h3>Recent jobs</h3><p>Your latest recruitment roles.</p></div><button className="link-btn" onClick={onJobs}>View all <ChevronRight size={15}/></button></div>
    {recent.length ? <div className="job-list">{recent.map(j => <JobRow key={j.job_id} job={j} onScreen={onScreen}/>)}</div> :
      <Empty title="No jobs yet" text="Create your first job to start screening."/>}
  </div>;
}

function Stat({icon: Icon, label, value}) { return <div className="stat-card"><div className="stat-icon"><Icon size={19}/></div><div><span>{label}</span><strong>{value}</strong></div></div> }
function ActionCard({icon: Icon, title, text, onClick}) { return <button className="action-card" onClick={onClick}><div className="action-icon"><Icon size={20}/></div><div><strong>{title}</strong><p>{text}</p></div><ChevronRight className="action-arrow" size={18}/></button> }

function Jobs({ jobs, onCreate, onDelete, onScreen, onView }) {
  return <div>
    <div className="page-actions"><div><h2>Jobs</h2><p>Create roles and run AI candidate screening.</p></div><button className="primary" onClick={onCreate}><Plus size={17}/> New job</button></div>
    {jobs.length ? <div className="cards-grid">{jobs.map(j => <div className="job-card" key={j.job_id}>
      <div className="job-card-top"><div className="job-icon"><BriefcaseBusiness size={19}/></div><span className="badge green">Ready</span></div>
      <h3>{j.title}</h3><p className="clamp">{j.description}</p>
      <div className="chips">{(j.required_skills || []).slice(0,5).map(s => <span key={s}>{s}</span>)}</div>
      <div className="job-meta"><span>{j.minimum_experience || 0}+ yrs exp.</span><span>{j.education_requirements || "Any education"}</span></div>
      <div className="card-actions"><button className="secondary small" onClick={() => onScreen(j)}><Play size={15}/> Screen candidates</button><button className="icon-btn danger" onClick={() => onDelete(j.job_id)}><Trash2 size={16}/></button></div>
    </div>)}</div> : <Empty title="No jobs created" text="Create a job description and the Job Agent will extract its requirements." action={onCreate}/>}
  </div>;
}

function JobRow({job, onScreen}) { return <div className="job-row"><div className="job-icon"><BriefcaseBusiness size={18}/></div><div className="job-row-main"><strong>{job.title}</strong><span>{(job.required_skills || []).slice(0,4).join(" • ") || "No skills extracted"}</span></div><span className="job-exp">{job.minimum_experience || 0}+ yrs</span><button className="secondary small" onClick={() => onScreen(job)}><Play size={14}/> Screen</button></div> }

function CreateJob({onDone, onCancel, notify}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [saving, setSaving] = useState(false);
  const submit = async (e) => {
    e.preventDefault();
    if (description.trim().length < 10) return notify("Description must be at least 10 characters", "error");
    setSaving(true);
    try { await api("/api/jobs", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({title, description})}); await onDone(); }
    catch(e) { notify(e.message, "error"); } finally { setSaving(false); }
  };
  return <div className="form-page"><button className="back-btn" onClick={onCancel}><ArrowLeft size={16}/> Back to jobs</button>
    <div className="form-card"><div className="form-title"><div className="job-icon"><BriefcaseBusiness size={20}/></div><div><h2>Create a new job</h2><p>The Job Agent will analyze your description automatically.</p></div></div>
      <form onSubmit={submit}><label>Job title<input value={title} onChange={e=>setTitle(e.target.value)} placeholder="e.g. Python Backend Developer" required maxLength={255}/></label>
      <label>Job description<textarea value={description} onChange={e=>setDescription(e.target.value)} rows={12} placeholder="Example: Build APIs using Python, FastAPI and SQL. 2 years experience. Bachelor degree. Knowledge of Docker is preferred." required/></label>
      <div className="hint"><Sparkles size={15}/> AI will extract required skills, preferred skills, experience, education and other requirements.</div>
      <div className="form-actions"><button type="button" className="secondary" onClick={onCancel}>Cancel</button><button className="primary" disabled={saving}>{saving ? "Analyzing..." : "Create & analyze job"} <Sparkles size={16}/></button></div>
      </form>
    </div>
  </div>;
}

function Upload({onDone, notify}) {
  const [files, setFiles] = useState([]);
  const [drag, setDrag] = useState(false);
  const [uploading, setUploading] = useState(false);
  const onFiles = (list) => setFiles(Array.from(list).filter(f => /\.(pdf|docx)$/i.test(f.name)));
  const submit = async () => {
    if (!files.length) return notify("Choose at least one PDF or DOCX resume", "error");
    const fd = new FormData(); files.forEach(f => fd.append("files", f));
    setUploading(true);
    try { await api("/api/resumes/upload", {method:"POST", body:fd}); notify(`Processed ${files.length} resume(s)`); await onDone(); }
    catch(e) { notify(e.message, "error"); } finally { setUploading(false); }
  };
  return <div className="form-page"><div className="page-actions"><div><h2>Upload resumes</h2><p>Upload up to 20 PDF/DOCX resumes, maximum 5 MB each.</p></div></div>
    <div className={`dropzone ${drag ? "drag" : ""}`} onDragOver={e=>{e.preventDefault();setDrag(true)}} onDragLeave={()=>setDrag(false)} onDrop={e=>{e.preventDefault();setDrag(false);onFiles(e.dataTransfer.files)}} onClick={()=>document.getElementById("resume-input").click()}>
      <input id="resume-input" type="file" hidden multiple accept=".pdf,.docx" onChange={e=>onFiles(e.target.files)}/>
      <div className="upload-circle"><UploadCloud size={27}/></div><h3>Drop resumes here</h3><p>or click to browse files</p><span>PDF and DOCX • up to 20 files • 5 MB each</span>
    </div>
    {files.length > 0 && <div className="selected-files">{files.map(f=><div className="file-item" key={f.name}><FileText size={18}/><div><strong>{f.name}</strong><span>{(f.size/1024/1024).toFixed(2)} MB</span></div><button onClick={()=>setFiles(files.filter(x=>x!==f))}><X size={16}/></button></div>)}</div>}
    <div className="upload-bottom"><div className="pipeline"><span>1</span> Upload <ChevronRight size={14}/><span>2</span> Parse <ChevronRight size={14}/><span>3</span> Extract profile <ChevronRight size={14}/><span>4</span> Save</div><button className="primary" onClick={submit} disabled={uploading || !files.length}>{uploading ? "Processing..." : `Process ${files.length || ""} resume${files.length === 1 ? "" : "s"}`} <Sparkles size={16}/></button></div>
  </div>;
}

function Candidates({candidates, onOpen, onDelete}) {
  const [q,setQ]=useState("");
  const [sort,setSort]=useState("newest");
  const filtered = useMemo(() => {
    const x = candidates.filter(c => `${c.name} ${c.email} ${(c.skills||[]).join(" ")}`.toLowerCase().includes(q.toLowerCase()));
    return [...x].sort((a,b)=>sort==="name"?a.name.localeCompare(b.name):Number(b.experience)-Number(a.experience));
  }, [candidates,q,sort]);
  return <div><div className="page-actions"><div><h2>Candidates</h2><p>Profiles extracted from uploaded resumes.</p></div></div>
    <div className="toolbar"><div className="search"><Search size={17}/><input placeholder="Search name, email or skill..." value={q} onChange={e=>setQ(e.target.value)}/></div><div className="select"><SlidersHorizontal size={15}/><select value={sort} onChange={e=>setSort(e.target.value)}><option value="newest">Experience high → low</option><option value="name">Name A → Z</option></select></div></div>
    {filtered.length ? <div className="candidate-table"><div className="table-head"><span>Candidate</span><span>Experience</span><span>Skills</span><span>Education</span><span>Action</span></div>
      {filtered.map(c=><div className="table-row" key={c.candidate_id}><div className="candidate-cell"><Avatar name={c.name}/><div><strong>{c.name}</strong><span>{c.email || "No email"}</span></div></div><strong>{c.experience || 0} yrs</strong><div className="chips compact">{(c.skills||[]).slice(0,3).map(s=><span key={s}>{s}</span>)}</div><span>{c.education || "—"}</span><div className="row-actions"><button className="icon-btn" onClick={()=>onOpen(c.candidate_id)}><Eye size={16}/></button><button className="icon-btn danger" onClick={()=>onDelete(c.candidate_id)}><Trash2 size={16}/></button></div></div>)}
    </div> : <Empty title="No candidates found" text={q ? "Try another search." : "Upload resumes to create candidate profiles."}/>}
  </div>;
}

function Avatar({name}) { const initials=(name||"?").split(" ").map(x=>x[0]).slice(0,2).join("").toUpperCase(); return <div className="avatar">{initials}</div> }

function Screening({job, results, onBack, onCandidate}) {
  const [filter,setFilter]=useState("all");
  const shown = results.filter(r => filter==="all" || (filter==="strong" ? r.score>=70 : r.score<70));
  return <div><div className="page-actions"><div><button className="back-btn" onClick={onBack}><ArrowLeft size={16}/> Back to jobs</button><h2>{job?.title || "Screening results"}</h2><p>AI-ranked candidates using deterministic scoring + recruiter analysis.</p></div></div>
    <div className="screen-summary"><div><span>Candidates screened</span><strong>{results.length}</strong></div><div><span>Strong matches</span><strong>{results.filter(r=>r.score>=70).length}</strong></div><div><span>Average score</span><strong>{results.length ? pct(results.reduce((a,r)=>a+r.score,0)/results.length) : "—"}</strong></div></div>
    <div className="toolbar"><div className="tabs"><button className={filter==="all"?"tab active":"tab"} onClick={()=>setFilter("all")}>All ({results.length})</button><button className={filter==="strong"?"tab active":"tab"} onClick={()=>setFilter("strong")}>Strong ({results.filter(r=>r.score>=70).length})</button><button className={filter==="review"?"tab active":"tab"} onClick={()=>setFilter("review")}>Review ({results.filter(r=>r.score<70).length})</button></div></div>
    {shown.length ? <div className="results-list">{shown.map((r,i)=><div className="result-card" key={r.candidate_id}><div className="rank">#{i+1}</div><Avatar name={r.candidate_name}/><div className="result-main"><div className="result-title"><strong>{r.candidate_name}</strong><span className={`recommend ${r.recommendation?.toLowerCase().replaceAll(" ","-")}`}>{r.recommendation}</span></div><p>{r.recruiter_summary || r.explanation || "AI analysis completed."}</p><div className="score-bars"><MiniScore label="Skills" value={r.skill_score}/><MiniScore label="Experience" value={r.experience_score}/><MiniScore label="Education" value={r.education_score}/><MiniScore label="Other fit" value={r.other_fit_score}/></div><div className="chips">{(r.matched_skills||[]).slice(0,6).map(s=><span className="match-chip" key={s}>✓ {s}</span>)}{(r.missing_skills||[]).slice(0,3).map(s=><span className="missing-chip" key={s}>+ {s}</span>)}</div></div><div className={`big-score ${scoreClass(r.score)}`}><strong>{pct(r.score)}</strong><span>match</span></div><button className="icon-btn" onClick={()=>onCandidate(r.candidate_id)}><ChevronRight size={18}/></button></div>)}</div> : <Empty title="No screening results" text="Run screening after you have at least one candidate."/>}
  </div>;
}

function MiniScore({label,value}) { return <div className="mini-score"><div><span>{label}</span><strong>{pct(value)}</strong></div><div className="bar"><i style={{width:`${Math.min(100,Number(value)||0)}%`}}/></div></div> }

function CandidateDetail({candidate,result,onBack}) {
  if (!candidate) return <Empty title="Candidate not found" text="Go back and select a candidate." action={onBack}/>;
  return <div><button className="back-btn" onClick={onBack}><ArrowLeft size={16}/> Back to candidates</button>
    <div className="profile-head"><Avatar name={candidate.name}/><div><h2>{candidate.name}</h2><div className="contact-line">{candidate.email && <span><Mail size={14}/> {candidate.email}</span>}{candidate.phone && <span><Phone size={14}/> {candidate.phone}</span>}</div></div>{result && <div className={`profile-score ${scoreClass(result.score)}`}><strong>{pct(result.score)}</strong><span>job match</span></div>}</div>
    {result && <div className="analysis-panel"><div className="analysis-header"><Sparkles size={18}/><div><strong>AI recruiter analysis</strong><span>{result.recommendation}</span></div></div><p>{result.explanation}</p><div className="analysis-grid"><AnalysisList icon={CheckCircle2} title="Strengths" items={result.strengths}/><AnalysisList icon={AlertTriangle} title="Concerns" items={result.concerns}/></div></div>}
    <div className="detail-grid"><div className="detail-card"><h3><GraduationCap size={18}/> Education & experience</h3><div className="detail-value"><strong>{candidate.experience || 0} years</strong><span>Professional experience</span></div><p>{candidate.education || "Education not extracted."}</p></div><div className="detail-card"><h3><Award size={18}/> Certifications</h3>{(candidate.certifications||[]).length ? <ul>{candidate.certifications.map(x=><li key={x}>{x}</li>)}</ul> : <p>No certifications extracted.</p>}</div><div className="detail-card wide"><h3><Sparkles size={18}/> Skills</h3><div className="chips large">{(candidate.skills||[]).map(x=><span key={x}>{x}</span>)}</div></div><div className="detail-card wide"><h3><BriefcaseBusiness size={18}/> Projects & relevant experience</h3>{(candidate.projects||[]).length ? <ul>{candidate.projects.map(x=><li key={x}>{x}</li>)}</ul> : <p>{candidate.relevant_experience?.join(" • ") || "No project details extracted."}</p>}</div></div>
  </div>;
}

function AnalysisList({icon:Icon,title,items=[]}) { return <div><h4><Icon size={15}/>{title}</h4>{items?.length ? <ul>{items.map(x=><li key={x}>{x}</li>)}</ul> : <span className="muted">None identified.</span>}</div> }
function Empty({title,text,action}) { return <div className="empty"><div className="empty-icon"><FileText size={22}/></div><h3>{title}</h3><p>{text}</p>{action && <button className="primary" onClick={action}>Get started</button>}</div> }

createRoot(document.getElementById("root")).render(<App />);
