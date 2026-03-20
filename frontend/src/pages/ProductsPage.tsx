import { useNavigate } from 'react-router-dom'

// Since there's no list endpoint yet, we show stored products from localStorage
import { useState, useEffect } from 'react'
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

  useEffect(() => {
    setProducts(getStoredProducts())
  }, [])

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

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">My Products</h1>
        <p className="page-subtitle">Manage your products and their feature pipelines.</p>
      </div>

      {products.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">&#128230;</div>
          <p className="empty-state-text">No products yet. Create your first product to get started.</p>
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
                <span className={`badge ${statusBadge(p.status)}`}>{p.status.replace(/_/g, ' ')}</span>
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
