import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { generateFeatureMap, approveFeatureMap, connectGithub } from '../api/client'
import { useToast } from '../components/Toast'
import type { Product, Feature } from '../types'

function getProductFromStorage(id: string): Product | null {
  try {
    const products: Product[] = JSON.parse(localStorage.getItem('gs_products') || '[]')
    return products.find(p => p.id === id) || null
  } catch {
    return null
  }
}

export default function ProductDetailPage() {
  const { productId } = useParams<{ productId: string }>()
  const navigate = useNavigate()
  const toast = useToast()
  const [product, setProduct] = useState<Product | null>(null)
  const [features, setFeatures] = useState<Feature[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedFeatures, setSelectedFeatures] = useState<Set<string>>(new Set())
  const [approved, setApproved] = useState(false)
  const [showGithub, setShowGithub] = useState(false)
  const [githubOwner, setGithubOwner] = useState('')
  const [githubRepo, setGithubRepo] = useState('')

  useEffect(() => {
    if (productId) {
      setProduct(getProductFromStorage(productId))
    }
  }, [productId])

  const handleGenerateFeatures = async () => {
    if (!productId) return
    setLoading(true)
    try {
      const res = await generateFeatureMap(productId)
      setFeatures(res)
      setSelectedFeatures(new Set(res.map(f => f.id)))
      toast('Feature map generated!', 'success')
    } catch (e: unknown) {
      toast(`Failed to generate features: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    if (!productId || selectedFeatures.size === 0) return
    if (!confirm(`Approve ${selectedFeatures.size} feature(s)? This will lock the feature map.`)) return
    setLoading(true)
    try {
      await approveFeatureMap(productId, Array.from(selectedFeatures))
      setApproved(true)
      toast('Features approved! You can now work on each feature.', 'success')
    } catch (e: unknown) {
      toast(`Failed to approve features: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleConnectGithub = async () => {
    if (!productId || !githubOwner.trim() || !githubRepo.trim()) return
    setLoading(true)
    try {
      await connectGithub(productId, githubOwner.trim(), githubRepo.trim())
      toast('GitHub repository connected!', 'success')
      setShowGithub(false)
    } catch (e: unknown) {
      toast(`Failed to connect GitHub: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const toggleFeature = (id: string) => {
    if (approved) return
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
        <h1 className="page-title">{product?.name || 'Product Details'}</h1>
        <p className="page-subtitle">
          {product?.idea_text
            ? product.idea_text.length > 200 ? product.idea_text.slice(0, 200) + '...' : product.idea_text
            : `Product ID: ${productId}`
          }
        </p>
      </div>

      {/* Product info card */}
      {product && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
            {product.summary && (
              <div style={{ flex: 1, minWidth: 200 }}>
                <div className="form-label">Summary</div>
                <p style={{ fontSize: 14, lineHeight: 1.6 }}>{product.summary}</p>
              </div>
            )}
            {product.target_users && (
              <div style={{ minWidth: 150 }}>
                <div className="form-label">Target Users</div>
                <p style={{ fontSize: 14 }}>{product.target_users}</p>
              </div>
            )}
            {product.goal && (
              <div style={{ minWidth: 150 }}>
                <div className="form-label">Goal</div>
                <p style={{ fontSize: 14 }}>{product.goal}</p>
              </div>
            )}
          </div>
        </div>
      )}

      <div style={{ display: 'flex', gap: 12, marginBottom: 32 }}>
        <button className="btn btn-primary" onClick={handleGenerateFeatures} disabled={loading}>
          {loading && features.length === 0
            ? <><span className="spinner" /> Generating...</>
            : features.length > 0 ? 'Regenerate Feature Map' : 'Generate Feature Map'}
        </button>
        <button className="btn btn-secondary" onClick={() => setShowGithub(!showGithub)}>
          Connect GitHub
        </button>
      </div>

      {features.length === 0 && !loading && (
        <div className="card" style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
          <div style={{ fontSize: 32, marginBottom: 12 }}>&#128736;</div>
          <p>Click "Generate Feature Map" to create features from your product discovery data.</p>
        </div>
      )}

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
          <div style={{ display: 'flex', gap: 12 }}>
            <button className="btn btn-primary" onClick={handleConnectGithub} disabled={loading || !githubOwner.trim() || !githubRepo.trim()}>
              {loading ? <><span className="spinner" /> Connecting...</> : 'Connect'}
            </button>
            <button className="btn btn-ghost" onClick={() => setShowGithub(false)}>Cancel</button>
          </div>
        </div>
      )}

      {features.length > 0 && (
        <>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Feature Map</h2>
          <div className="result-panel">
            <div className="result-header">
              <h3>Features ({features.length})</h3>
              {!approved ? (
                <button className="btn btn-sm btn-primary" onClick={handleApprove} disabled={loading || selectedFeatures.size === 0}>
                  Approve Selected ({selectedFeatures.size})
                </button>
              ) : (
                <span className="badge badge-green">Approved</span>
              )}
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
                    Open Pipeline
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
