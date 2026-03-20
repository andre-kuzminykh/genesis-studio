import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { generateFeatureMap, approveFeatureMap, connectGithub } from '../api/client'
import { useToast } from '../components/Toast'
import type { Feature } from '../types'

export default function ProductDetailPage() {
  const { productId } = useParams<{ productId: string }>()
  const navigate = useNavigate()
  const toast = useToast()
  const [features, setFeatures] = useState<Feature[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedFeatures, setSelectedFeatures] = useState<Set<string>>(new Set())
  const [showGithub, setShowGithub] = useState(false)
  const [githubOwner, setGithubOwner] = useState('')
  const [githubRepo, setGithubRepo] = useState('')

  const handleGenerateFeatures = async () => {
    if (!productId) return
    setLoading(true)
    try {
      const res = await generateFeatureMap(productId)
      setFeatures(res)
      setSelectedFeatures(new Set(res.map(f => f.id)))
      toast('Feature map generated!', 'success')
    } catch (e: unknown) {
      toast(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    if (!productId) return
    setLoading(true)
    try {
      await approveFeatureMap(productId, Array.from(selectedFeatures))
      toast('Features approved!', 'success')
    } catch (e: unknown) {
      toast(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleConnectGithub = async () => {
    if (!productId || !githubOwner || !githubRepo) return
    setLoading(true)
    try {
      await connectGithub(productId, githubOwner, githubRepo)
      toast('GitHub repository connected!', 'success')
      setShowGithub(false)
    } catch (e: unknown) {
      toast(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const toggleFeature = (id: string) => {
    setSelectedFeatures(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  return (
    <div>
      <a className="back-link" onClick={() => navigate('/products')} style={{ cursor: 'pointer', marginBottom: 16, display: 'inline-flex' }}>
        &larr; Back to Products
      </a>

      <div className="page-header">
        <h1 className="page-title">Product Details</h1>
        <p className="page-subtitle">Product ID: {productId}</p>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 32 }}>
        <button className="btn btn-primary" onClick={handleGenerateFeatures} disabled={loading}>
          {loading ? <><span className="spinner" /> Generating...</> : 'Generate Feature Map'}
        </button>
        <button className="btn btn-secondary" onClick={() => setShowGithub(!showGithub)}>
          Connect GitHub
        </button>
      </div>

      {showGithub && (
        <div className="card" style={{ marginBottom: 24, maxWidth: 500 }}>
          <h3 style={{ marginBottom: 16, fontSize: 16, fontWeight: 600 }}>Connect GitHub Repository</h3>
          <div className="form-group">
            <label className="form-label">Owner</label>
            <input className="input" placeholder="github-username" value={githubOwner} onChange={e => setGithubOwner(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Repository</label>
            <input className="input" placeholder="repo-name" value={githubRepo} onChange={e => setGithubRepo(e.target.value)} />
          </div>
          <button className="btn btn-primary" onClick={handleConnectGithub} disabled={loading || !githubOwner || !githubRepo}>
            Connect
          </button>
        </div>
      )}

      {features.length > 0 && (
        <>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Feature Map</h2>
          <div className="result-panel">
            <div className="result-header">
              <h3>Features ({features.length})</h3>
              <button className="btn btn-sm btn-primary" onClick={handleApprove} disabled={loading || selectedFeatures.size === 0}>
                Approve Selected ({selectedFeatures.size})
              </button>
            </div>
            <div>
              {features.map(f => (
                <div key={f.id} className="checkbox-item" onClick={() => toggleFeature(f.id)}>
                  <div className={`checkbox ${selectedFeatures.has(f.id) ? 'checked' : ''}`} />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: 14 }}>{f.name}</div>
                    {f.overview && <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>{f.overview}</div>}
                  </div>
                  <span className="badge badge-purple">{f.feature_id}</span>
                  <button
                    className="btn btn-sm btn-secondary"
                    onClick={e => { e.stopPropagation(); navigate(`/features/${f.id}`) }}
                  >
                    Open
                  </button>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
