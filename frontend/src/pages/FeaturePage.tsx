import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import * as api from '../api/client'
import { useToast } from '../components/Toast'
import type { PRDVersion, UXFlow, UseCase, Requirement, TestCase, CodeGenerateResponse, GitHubPushResponse, DeployResponse, Traceability } from '../types'

type ResultType =
  | { kind: 'prd'; data: PRDVersion }
  | { kind: 'ux'; data: UXFlow[] }
  | { kind: 'usecases'; data: UseCase[] }
  | { kind: 'requirements'; data: Requirement[] }
  | { kind: 'tests'; data: TestCase[] }
  | { kind: 'code'; data: CodeGenerateResponse }
  | { kind: 'github'; data: GitHubPushResponse }
  | { kind: 'deploy'; data: DeployResponse }
  | { kind: 'traceability'; data: Traceability }

const PIPELINE_STEPS = [
  { key: 'prd', label: 'PRD Draft' },
  { key: 'stories', label: 'Stories' },
  { key: 'ux', label: 'UX Preview' },
  { key: 'usecases', label: 'Use Cases' },
  { key: 'requirements', label: 'Requirements' },
  { key: 'tests', label: 'Tests' },
  { key: 'code', label: 'Code' },
  { key: 'github', label: 'GitHub' },
  { key: 'deploy', label: 'Deploy' },
]

const ACTIONS = [
  { key: 'prd', icon: '\u{1F4DD}', title: 'Generate PRD Draft', desc: 'Create feature PRD from discovery' },
  { key: 'stories', icon: '\u{1F464}', title: 'Approve Stories', desc: 'Review and approve user stories' },
  { key: 'ux', icon: '\u{1F3A8}', title: 'Generate UX Preview', desc: 'Telegram UX & Mermaid diagrams' },
  { key: 'usecases', icon: '\u{1F4CB}', title: 'Generate Use Cases', desc: 'Given / When / Then scenarios' },
  { key: 'requirements', icon: '\u{2699}\u{FE0F}', title: 'Generate Requirements', desc: 'Derive FR & NFR' },
  { key: 'tests', icon: '\u{1F9EA}', title: 'Generate Tests', desc: 'Unit, integration, e2e tests' },
  { key: 'code', icon: '\u{1F4BB}', title: 'Generate Code', desc: 'Backend & bot code generation' },
  { key: 'github', icon: '\u{1F680}', title: 'Push to GitHub', desc: 'Push generated code to repo' },
  { key: 'deploy', icon: '\u{26A1}', title: 'Deploy Locally', desc: 'Deploy backend & bot locally' },
  { key: 'traceability', icon: '\u{1F517}', title: 'Traceability', desc: 'Full traceability graph' },
]

export default function FeaturePage() {
  const { featureId } = useParams<{ featureId: string }>()
  const navigate = useNavigate()
  const toast = useToast()
  const [loading, setLoading] = useState<string | null>(null)
  const [result, setResult] = useState<ResultType | null>(null)
  const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set())

  const markDone = (key: string) => setCompletedSteps(s => new Set(s).add(key))

  const handleAction = async (key: string) => {
    if (!featureId) return
    setLoading(key)
    try {
      switch (key) {
        case 'prd': {
          const d = await api.generatePrdDraft(featureId)
          setResult({ kind: 'prd', data: d })
          markDone('prd')
          toast('PRD Draft generated!', 'success')
          break
        }
        case 'stories': {
          toast('Stories auto-approved from PRD generation.', 'info')
          markDone('stories')
          break
        }
        case 'ux': {
          const d = await api.generateUx(featureId)
          setResult({ kind: 'ux', data: d })
          markDone('ux')
          toast('UX Preview generated!', 'success')
          break
        }
        case 'usecases': {
          const d = await api.generateUseCases(featureId)
          setResult({ kind: 'usecases', data: d })
          markDone('usecases')
          toast('Use Cases generated!', 'success')
          break
        }
        case 'requirements': {
          const d = await api.generateRequirements(featureId)
          setResult({ kind: 'requirements', data: d })
          markDone('requirements')
          toast('Requirements derived!', 'success')
          break
        }
        case 'tests': {
          const d = await api.generateTests(featureId)
          setResult({ kind: 'tests', data: d })
          markDone('tests')
          toast('Tests generated!', 'success')
          break
        }
        case 'code': {
          const d = await api.generateCode(featureId)
          setResult({ kind: 'code', data: d })
          markDone('code')
          toast('Code generated!', 'success')
          break
        }
        case 'github': {
          const d = await api.pushToGithub(featureId)
          setResult({ kind: 'github', data: d })
          markDone('github')
          toast('Pushed to GitHub!', 'success')
          break
        }
        case 'deploy': {
          const d = await api.deployLocal(featureId)
          setResult({ kind: 'deploy', data: d })
          markDone('deploy')
          toast(`Deployment: ${d.status}`, d.status === 'success' ? 'success' : 'error')
          break
        }
        case 'traceability': {
          const d = await api.getTraceability(featureId)
          setResult({ kind: 'traceability', data: d })
          toast('Traceability loaded.', 'info')
          break
        }
      }
    } catch (e: unknown) {
      toast(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(null)
    }
  }

  return (
    <div>
      <a className="back-link" onClick={() => navigate(-1)} style={{ cursor: 'pointer', marginBottom: 16, display: 'inline-flex' }}>
        &larr; Back
      </a>

      <div className="feature-header">
        <h1>Feature Pipeline</h1>
        <span className="badge badge-purple" style={{ fontSize: 12 }}>{featureId?.slice(0, 8)}</span>
      </div>

      {/* Pipeline stepper */}
      <div className="pipeline">
        {PIPELINE_STEPS.map(s => (
          <div
            key={s.key}
            className={`pipeline-step ${completedSteps.has(s.key) ? 'done' : ''} ${loading === s.key ? 'active' : ''}`}
            onClick={() => handleAction(s.key)}
          >
            {completedSteps.has(s.key) ? '\u2713 ' : ''}{s.label}
          </div>
        ))}
      </div>

      {/* Action cards */}
      <div className="actions-grid">
        {ACTIONS.map(a => (
          <button
            key={a.key}
            className="action-card"
            onClick={() => handleAction(a.key)}
            disabled={loading !== null}
          >
            <div className="action-icon">{a.icon}</div>
            <div className="action-title">{a.title}</div>
            <div className="action-desc">{a.desc}</div>
            {loading === a.key && (
              <div style={{ marginTop: 12, display: 'flex', justifyContent: 'center' }}>
                <span className="spinner" />
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Results */}
      {result && (
        <div className="result-panel" style={{ marginTop: 32 }}>
          <div className="result-header">
            <h3>
              {result.kind === 'prd' && 'PRD Draft'}
              {result.kind === 'ux' && 'UX Previews'}
              {result.kind === 'usecases' && 'Use Cases'}
              {result.kind === 'requirements' && 'Requirements'}
              {result.kind === 'tests' && 'Test Cases'}
              {result.kind === 'code' && 'Code Generation Report'}
              {result.kind === 'github' && 'GitHub Push'}
              {result.kind === 'deploy' && 'Deployment'}
              {result.kind === 'traceability' && 'Traceability Graph'}
            </h3>
          </div>
          <div className="result-body">
            {result.kind === 'prd' && (
              <div>
                <div style={{ marginBottom: 12 }}>
                  <span className="badge badge-purple">Version {result.data.version_number}</span>
                  <span className="badge badge-gray" style={{ marginLeft: 8 }}>{result.data.status}</span>
                </div>
                {result.data.summary && <p style={{ lineHeight: 1.6 }}>{result.data.summary}</p>}
                {result.data.content && (
                  <pre className="result-code" style={{ marginTop: 16 }}>
                    {JSON.stringify(result.data.content, null, 2)}
                  </pre>
                )}
              </div>
            )}

            {result.kind === 'ux' && result.data.map((flow, i) => (
              <div key={i} className="result-item">
                <div style={{ fontWeight: 600, marginBottom: 8 }}>
                  {flow.title}
                  <span className="result-item-type">{flow.flow_type}</span>
                </div>
                <pre className="result-code">{flow.content}</pre>
              </div>
            ))}

            {result.kind === 'usecases' && result.data.map(uc => (
              <div key={uc.id} className="result-item">
                <span className="result-item-id">[{uc.use_case_id}]</span>
                <strong>{uc.title}</strong>
                <div style={{ marginTop: 8, fontSize: 13, color: 'var(--text-secondary)' }}>
                  <div><strong>Given:</strong> {uc.given}</div>
                  <div><strong>When:</strong> {uc.when}</div>
                  <div><strong>Then:</strong> {uc.then}</div>
                </div>
              </div>
            ))}

            {result.kind === 'requirements' && result.data.map(r => (
              <div key={r.id} className="result-item">
                <span className="result-item-id">[{r.req_id}]</span>
                <span className="result-item-type">({r.req_type})</span>
                {' '}{r.title}
                <div style={{ marginTop: 4, fontSize: 13, color: 'var(--text-secondary)' }}>{r.description}</div>
              </div>
            ))}

            {result.kind === 'tests' && result.data.map(t => (
              <div key={t.id} className="result-item">
                <span className="result-item-id">[{t.test_id}]</span>
                {t.title}
                <span className="result-item-type">({t.test_type})</span>
                <div style={{ marginTop: 4, fontSize: 13, color: 'var(--text-secondary)' }}>{t.description}</div>
              </div>
            ))}

            {result.kind === 'code' && (
              <div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
                  <div className="card" style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--purple-light)' }}>{result.data.generation_report.backend_files ?? 0}</div>
                    <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Backend Files</div>
                  </div>
                  <div className="card" style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--orange-light)' }}>{result.data.generation_report.bot_files ?? 0}</div>
                    <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Bot Files</div>
                  </div>
                  <div className="card" style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--text-primary)' }}>{result.data.generation_report.total_files ?? 0}</div>
                    <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Total Files</div>
                  </div>
                </div>
                {result.data.commit_sha && (
                  <p style={{ marginTop: 16, fontSize: 13, color: 'var(--text-secondary)' }}>
                    Commit: <code>{result.data.commit_sha}</code>
                  </p>
                )}
              </div>
            )}

            {result.kind === 'github' && (
              <div>
                <p><strong>Branch:</strong> {result.data.branch}</p>
                <p><strong>Commit:</strong> <code>{result.data.commit_sha}</code></p>
                <p><strong>Status:</strong> <span className="badge badge-green">{result.data.status}</span></p>
              </div>
            )}

            {result.kind === 'deploy' && (
              <div>
                <p><strong>Status:</strong> <span className={`badge ${result.data.status === 'success' ? 'badge-green' : 'badge-red'}`}>{result.data.status}</span></p>
                {result.data.endpoints && (
                  <div style={{ marginTop: 12 }}>
                    <strong>Endpoints:</strong>
                    {Object.entries(result.data.endpoints).map(([k, v]) => (
                      <div key={k} style={{ fontSize: 13, marginTop: 4 }}>{k}: <code>{v}</code></div>
                    ))}
                  </div>
                )}
                {result.data.logs && (
                  <pre className="result-code" style={{ marginTop: 16 }}>{result.data.logs}</pre>
                )}
                {result.data.error_message && (
                  <p style={{ marginTop: 12, color: 'var(--error)' }}>{result.data.error_message}</p>
                )}
              </div>
            )}

            {result.kind === 'traceability' && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
                {[
                  { label: 'User Stories', count: result.data.user_stories_count },
                  { label: 'Use Cases', count: result.data.use_cases_count },
                  { label: 'Requirements', count: result.data.requirements_count },
                  { label: 'Test Cases', count: result.data.test_cases_count },
                  { label: 'Code Artifacts', count: result.data.code_artifacts_count },
                ].map(item => (
                  <div key={item.label} className="card" style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--purple-light)' }}>{item.count}</div>
                    <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{item.label}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
