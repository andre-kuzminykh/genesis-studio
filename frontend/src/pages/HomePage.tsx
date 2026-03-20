import { useNavigate } from 'react-router-dom'

const FLOW_STEPS = ['Idea', 'Discovery', 'Features', 'PRD', 'Stories', 'UX', 'Use Cases', 'Requirements', 'Tests', 'Code', 'GitHub', 'Deploy']

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="hero">
      <h1 className="hero-title">Genesis Studio</h1>
      <p className="hero-subtitle">
        PRD-first product development platform.<br />
        From idea to deployment — fully automated.
      </p>
      <div className="hero-flow">
        {FLOW_STEPS.map((step, i) => (
          <span key={step} style={{ display: 'contents' }}>
            <span className="hero-flow-item">{step}</span>
            {i < FLOW_STEPS.length - 1 && <span className="hero-flow-arrow">&rarr;</span>}
          </span>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 16, justifyContent: 'center' }}>
        <button className="btn btn-primary btn-lg" onClick={() => navigate('/create')}>
          Create Product
        </button>
        <button className="btn btn-secondary btn-lg" onClick={() => navigate('/products')}>
          My Products
        </button>
      </div>
    </div>
  )
}
