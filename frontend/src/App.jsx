import React, { useEffect, useMemo, useState } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function callApi(path, options = {}) {
  const res = await fetch(`${API}${path}`, options)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`)
  return data
}

function Stat({ label, value, accent }) {
  return (
    <div className={`stat ${accent || ''}`}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  )
}

function SkillChip({ name, proficiency = 0, confidence = 0 }) {
  return (
    <div className="skill-chip reveal">
      <div className="skill-chip-top">
        <span>{name}</span>
        <span>{proficiency}/5</span>
      </div>
      <div className="chip-bar"><div className="chip-fill" style={{ width: `${(proficiency / 5) * 100}%` }} /></div>
      <small>{Math.round(confidence * 100)}% confidence</small>
    </div>
  )
}

function Toast({ kind = 'success', text, onClose }) {
  if (!text) return null
  return (
    <div className={`toast ${kind}`}>
      <div>
        <strong>{kind === 'error' ? 'Something broke' : 'Nice'}</strong>
        <p>{text}</p>
      </div>
      <button className="glass-btn small" onClick={onClose}>Dismiss</button>
    </div>
  )
}

function SectionTitle({ eyebrow, title, subtitle }) {
  return (
    <div className="section-title reveal">
      {eyebrow && <span className="eyebrow">{eyebrow}</span>}
      <h2>{title}</h2>
      {subtitle && <p>{subtitle}</p>}
    </div>
  )
}

function EmptyState({ title, body, action, actionLabel }) {
  return (
    <div className="empty-state reveal">
      <div className="empty-icon">✦</div>
      <h3>{title}</h3>
      <p>{body}</p>
      {action && <button className="gradient-btn" onClick={action}>{actionLabel}</button>}
    </div>
  )
}

function LoadingSkeleton() {
  return (
    <div className="skeleton-wrap reveal">
      <div className="skeleton h-20" />
      <div className="skeleton h-14" />
      <div className="skeleton h-14" />
      <div className="skeleton h-32" />
    </div>
  )
}

function EmployeeModal({ open, onClose, onCreate, busy }) {
  const [form, setForm] = useState({ name: '', role: '', geography: '', career_stage: '' })

  useEffect(() => {
    if (!open) setForm({ name: '', role: '', geography: '', career_stage: '' })
  }, [open])

  if (!open) return null

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal card glass reveal" onClick={(e) => e.stopPropagation()}>
        <SectionTitle eyebrow="New employee" title="Create employee profile" subtitle="Start from a clean profile instead of relying on a fixed ID." />
        <div className="modal-grid">
          <input placeholder="Full name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Role" value={form.role} onChange={e => setForm({ ...form, role: e.target.value })} />
          <input placeholder="Geography" value={form.geography} onChange={e => setForm({ ...form, geography: e.target.value })} />
          <input placeholder="Career stage" value={form.career_stage} onChange={e => setForm({ ...form, career_stage: e.target.value })} />
        </div>
        <div className="hero-actions">
          <button className="glass-btn" onClick={onClose}>Cancel</button>
          <button className="gradient-btn" disabled={busy} onClick={() => onCreate(form)}>Create profile</button>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [employeeId, setEmployeeId] = useState(1)
  const [employee, setEmployee] = useState(null)
  const [searchText, setSearchText] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [modalOpen, setModalOpen] = useState(false)

  const [cvFile, setCvFile] = useState(null)
  const [cvFallbackText, setCvFallbackText] = useState('Python FastAPI AWS Docker SQL')

  const [availableCerts, setAvailableCerts] = useState([])
  const [certSlug, setCertSlug] = useState('aws-certified-solutions-architect-associate')

  const [skillSuggestions, setSkillSuggestions] = useState([])
  const [targetSkill, setTargetSkill] = useState('aws')
  const [timelineWeeks, setTimelineWeeks] = useState(6)
  const [learningPath, setLearningPath] = useState([])

  const [busy, setBusy] = useState(false)
  const [booting, setBooting] = useState(true)
  const [toast, setToast] = useState({ kind: 'success', text: '' })

  const skills = useMemo(() => Object.entries(employee?.skills || {}), [employee])
  const topSkills = skills.slice(0, 6)
  const remainingSkills = skills.slice(6)

  useEffect(() => {
    bootstrap()
  }, [])

  async function bootstrap() {
    setBooting(true)
    try {
      const [certs, suggestions] = await Promise.all([
        callApi('/certifications/available'),
        callApi('/employees/skills/suggestions')
      ])
      setAvailableCerts(certs)
      setSkillSuggestions(suggestions)
    } catch (e) {
      setToast({ kind: 'error', text: e.message })
    } finally {
      setBooting(false)
    }
  }

  async function withBusy(fn) {
    setBusy(true)
    try {
      await fn()
    } catch (e) {
      setToast({ kind: 'error', text: e.message })
    } finally {
      setBusy(false)
    }
  }

  async function loadEmployee(id) {
    const profile = await callApi(`/employees/${id}`)
    setEmployee(profile)
    setEmployeeId(id)
    setLearningPath([])
  }

  async function createEmployee(form) {
    await withBusy(async () => {
      const created = await callApi('/employees', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      setModalOpen(false)
      setEmployee(created)
      setEmployeeId(created.id)
      setSearchResults([])
      setToast({ kind: 'success', text: `Employee profile created for ${created.name}.` })
    })
  }

  function prettyName(slug) {
    return slug.split('-').map((w) => w[0].toUpperCase() + w.slice(1)).join(' ')
  }

  async function runSearch() {
    await withBusy(async () => {
      const results = await callApi(`/employees/search?name=${encodeURIComponent(searchText)}`)
      setSearchResults(results)
      setToast({ kind: 'success', text: `${results.length} employee match${results.length === 1 ? '' : 'es'} found.` })
    })
  }

  async function processCv() {
    await withBusy(async () => {
      const fd = new FormData()
      if (cvFile) fd.append('file', cvFile)
      else fd.append('file', new Blob([cvFallbackText], { type: 'text/plain' }), 'cv.txt')
      const res = await callApi(`/employees/${employeeId}/cv/upload`, { method: 'POST', body: fd })
      await loadEmployee(employeeId)
      setToast({ kind: 'success', text: `CV processed. ${res.extracted_skills?.length || 0} skills were updated.` })
    })
  }

  async function applyCertification() {
    await withBusy(async () => {
      const res = await callApi(`/employees/${employeeId}/certifications`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ certification_slug: certSlug })
      })
      await loadEmployee(employeeId)
      setToast({ kind: 'success', text: `Certification synced. ${res.mapped_skills?.length || 0} skills were enriched.` })
    })
  }

  async function generatePath() {
    await withBusy(async () => {
      const res = await callApi(`/employees/${employeeId}/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_skill: targetSkill, timeline_weeks: Number(timelineWeeks) })
      })
      setLearningPath(res.analysis?.learning_path || [])
      setToast({ kind: 'success', text: `Fresh learning path ready for ${targetSkill.toUpperCase()}.` })
    })
  }

  return (
    <main className="page">
      <div className="bg-orb orb-1" />
      <div className="bg-orb orb-2" />
      <Toast kind={toast.kind} text={toast.text} onClose={() => setToast({ ...toast, text: '' })} />
      <EmployeeModal open={modalOpen} onClose={() => setModalOpen(false)} onCreate={createEmployee} busy={busy} />

      <section className="hero-shell">
        <div className="hero card glass reveal">
          <div className="hero-copy">
            <span className="eyebrow">AI-driven workforce intelligence</span>
            <h1>Build a smoother talent intelligence experience</h1>
            <p>Upload CVs, enrich skill profiles, sync certifications, and create guided learning journeys with a cleaner, more modern interface.</p>
            <div className="hero-actions">
              <button className="gradient-btn" onClick={() => setModalOpen(true)}>Create employee</button>
              <button className="glass-btn" disabled={busy || !employee} onClick={() => employee && withBusy(() => loadEmployee(employee.id))}>Refresh profile</button>
            </div>
          </div>
          <div className="stats-grid">
            <Stat label="Active employee" value={employee?.name || 'No one loaded'} accent="pink" />
            <Stat label="Skill count" value={skills.length} accent="blue" />
            <Stat label="Certifications" value={employee?.certifications?.length || 0} accent="green" />
          </div>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="left-column">
          <div className="card glass panel-card reveal">
            <SectionTitle eyebrow="Lookup" title="Find an employee" subtitle="Search by name or load directly by ID." />
            <div className="inline-form">
              <input value={searchText} onChange={e => setSearchText(e.target.value)} placeholder="Search by name" />
              <button className="gradient-btn" disabled={busy} onClick={runSearch}>Search</button>
            </div>
            {searchResults.length > 0 ? (
              <div className="result-stack">
                {searchResults.map((r) => (
                  <button key={r.id} className="result-card reveal" onClick={() => withBusy(() => loadEmployee(r.id))}>
                    <div>
                      <strong>{r.name}</strong>
                      <p>{r.role}</p>
                    </div>
                    <span>#{r.id}</span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="muted inline-note">No search results yet. Try a name or create a fresh profile.</p>
            )}
            <div className="inline-form compact">
              <input type="number" min={1} value={employeeId} onChange={e => setEmployeeId(Number(e.target.value))} placeholder="Employee ID" />
              <button className="glass-btn" disabled={busy} onClick={() => withBusy(() => loadEmployee(employeeId))}>Load</button>
            </div>
          </div>

          <div className="card glass profile-card reveal">
            <SectionTitle eyebrow="Profile" title={employee?.name || 'No employee loaded'} subtitle={employee ? `${employee.role} · ${employee.geography} · ${employee.career_stage}` : 'Create or load a profile to view skills and certifications.'} />

            {booting ? <LoadingSkeleton /> : !employee ? (
              <EmptyState
                title="No profile loaded yet"
                body="Create a new employee profile or search for an existing one to start exploring the full experience."
                action={() => setModalOpen(true)}
                actionLabel="Create employee"
              />
            ) : (
              <div className="profile-panels">
                <div className="mini-panel reveal">
                  <h4>Top skills</h4>
                  {topSkills.length ? (
                    <div className="skills-mosaic">
                      {topSkills.map(([skill, meta]) => (
                        <SkillChip key={skill} name={prettyName(skill)} proficiency={meta.proficiency} confidence={meta.confidence} />
                      ))}
                    </div>
                  ) : <p className="muted">No skills yet.</p>}
                </div>

                <div className="mini-panel reveal">
                  <h4>Certifications</h4>
                  <div className="tag-wrap">
                    {(employee?.certifications || []).length
                      ? employee.certifications.map(c => <span key={c} className="tag">{prettyName(c)}</span>)
                      : <span className="muted">No certifications yet.</span>}
                  </div>

                  {remainingSkills.length > 0 && (
                    <>
                      <h4 className="subtle-gap">More skills</h4>
                      <div className="pill-cloud">
                        {remainingSkills.map(([skill, meta]) => (
                          <span key={skill} className="skill-pill">{prettyName(skill)} · {meta.proficiency}/5</span>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="right-column">
          <div className="card glass flow-card reveal">
            <SectionTitle eyebrow="1" title="CV skill extraction" subtitle="Upload a CV or paste a summary to infer and update skills." />
            <div className="split-grid">
              <div className="input-group soft-box">
                <label>Upload CV file</label>
                <input type="file" onChange={(e) => setCvFile(e.target.files?.[0] || null)} />
              </div>
              <div className="input-group soft-box">
                <label>Fallback summary text</label>
                <textarea rows={5} value={cvFallbackText} onChange={e => setCvFallbackText(e.target.value)} />
              </div>
            </div>
            <button className="gradient-btn wide" disabled={busy || !employee} onClick={processCv}>Process CV</button>
          </div>

          <div className="card glass flow-card reveal">
            <SectionTitle eyebrow="2" title="Certification sync" subtitle="Apply certification intelligence to strengthen the employee skill profile." />
            <div className="soft-box">
              <label>Select certification</label>
              <select value={certSlug} onChange={e => setCertSlug(e.target.value)}>
                {availableCerts.map(c => <option key={c.slug} value={c.slug}>{c.name}</option>)}
              </select>
            </div>
            <button className="gradient-btn wide alt" disabled={busy || !employee} onClick={applyCertification}>Add certification</button>
          </div>

          <div className="card glass flow-card reveal">
            <SectionTitle eyebrow="3" title="Personalized learning path" subtitle="Generate a more guided timeline instead of a plain list of links." />
            <div className="split-grid single-height">
              <div className="input-group soft-box">
                <label>Target skill</label>
                <input list="skills" value={targetSkill} onChange={e => setTargetSkill(e.target.value)} />
                <datalist id="skills">
                  {skillSuggestions.map(s => <option key={s} value={s} />)}
                </datalist>
              </div>
              <div className="input-group soft-box">
                <label>Timeline (weeks)</label>
                <input type="number" min={1} value={timelineWeeks} onChange={e => setTimelineWeeks(Number(e.target.value))} />
              </div>
            </div>
            <button className="gradient-btn wide purple" disabled={busy || !employee} onClick={generatePath}>Generate path</button>

            {learningPath.length > 0 ? (
              <div className="timeline pretty">
                {learningPath.map((item, i) => (
                  <div key={`${item.week}-${i}`} className="timeline-card reveal">
                    <div className="timeline-mark">{item.week}</div>
                    <div>
                      <strong>{item.stage}</strong>
                      <p>{item.goal}</p>
                      <a href={item.resource?.url} target="_blank" rel="noreferrer">{item.resource?.title}</a>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState title="No learning path yet" body="Choose a target skill and generate a path to turn this area into a structured roadmap." />
            )}
          </div>
        </div>
      </section>
    </main>
  )
}
