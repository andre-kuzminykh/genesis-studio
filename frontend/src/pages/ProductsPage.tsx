import { useNavigate } from 'react-router-dom'
import { useState, useEffect, useCallback } from 'react'
import type { Product } from '../types'

function getStoredProducts(): Product[] {
  try {
    return JSON.parse(localStorage.getItem('gs_products') || '[]')
  } catch {
    return []
  }
}

export default function ProductsPage() {
  const navigate = useNavigate()
  const [products, setProducts] = useState<Product[]>([])

  const refresh = useCallback(() => setProducts(getStoredProducts()), [])

  // Reload on mount and when returning from other pages
  useEffect(() => {
    refresh()
    const onStorage = (e: StorageEvent) => {
      if (e.key === 'gs_products') refresh()
    }
    const onFocus = () => refresh()
    window.addEventListener('storage', onStorage)
    window.addEventListener('focus', onFocus)
    return () => {
      window.removeEventListener('storage', onStorage)
      window.removeEventListener('focus', onFocus)
    }
  }, [refresh])

  const statusBadge = (status: string) => {
    const map: Record<string, string> = {
      draft: 'badge-gray',
      discovery_in_progress: 'badge-purple',
      feature_map_draft: 'badge-orange',
      feature_map_approved: 'badge-green',
      in_development: 'badge-green',
    }
    return map[status] || 'badge-gray'
  }

  const statusLabel = (status: string) => status.replace(/_/g, ' ')

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 className="page-title">My Products</h1>
          <p className="page-subtitle">Manage your products and their feature pipelines.</p>
        </div>
        {products.length > 0 && (
          <button className="btn btn-primary" onClick={() => navigate('/create')}>
            + New Product
          </button>
        )}
      </div>

      {products.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon" role="img" aria-label="package">&#128230;</div>
          <p className="empty-state-text">No products yet.</p>
          <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 8 }}>
            Create your first product to start the PRD-first workflow.
          </p>
          <button className="btn btn-primary" style={{ marginTop: 24 }} onClick={() => navigate('/create')}>
            Create Product
          </button>
        </div>
      ) : (
        <div className="card-grid">
          {products.map(p => (
            <div key={p.id} className="card" onClick={() => navigate(`/products/${p.id}`)} style={{ cursor: 'pointer' }}>
              <div className="product-card-header">
                <span className="product-card-name">{p.name || 'Untitled Product'}</span>
                <span className={`badge ${statusBadge(p.status)}`}>{statusLabel(p.status)}</span>
              </div>
              <p className="product-card-idea">{p.idea_text}</p>
              <div className="product-card-footer">
                <span className="product-card-date">{new Date(p.created_at).toLocaleDateString()}</span>
                <button className="btn btn-sm btn-secondary" onClick={e => { e.stopPropagation(); navigate(`/products/${p.id}`) }}>
                  Open
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
