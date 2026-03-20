import { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { createProduct, submitDiscovery } from '../api/client'
import { useToast } from '../components/Toast'

interface ChatMessage {
  role: 'system' | 'user'
  text: string
}

export default function CreateProductPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const toast = useToast()

  // Restore productId from URL if page was refreshed after creation
  const savedProductId = searchParams.get('productId')
  const [step, setStep] = useState<'idea' | 'discovery' | 'done'>(savedProductId ? 'done' : 'idea')
  const [idea, setIdea] = useState('')
  const [loading, setLoading] = useState(false)
  const [productId, setProductId] = useState<string | null>(savedProductId)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [questions, setQuestions] = useState<string[]>([])
  const [currentQ, setCurrentQ] = useState(0)
  const [answer, setAnswer] = useState('')

  const handleSubmitIdea = async () => {
    if (idea.trim().length < 10) {
      toast('Please provide a more detailed description (at least 10 characters).', 'error')
      return
    }
    setLoading(true)
    try {
      const res = await createProduct(idea.trim())
      setProductId(res.product.id)
      // Save product to localStorage for listing
      const stored = JSON.parse(localStorage.getItem('gs_products') || '[]')
      stored.unshift(res.product)
      localStorage.setItem('gs_products', JSON.stringify(stored))
      setMessages([{ role: 'user', text: idea.trim() }])

      if (res.follow_up_questions.length > 0 && !res.is_complete) {
        setQuestions(res.follow_up_questions)
        setCurrentQ(0)
        setMessages(m => [...m, { role: 'system', text: res.follow_up_questions[0] }])
        setStep('discovery')
        toast('Product draft created! Answer discovery questions.', 'success')
      } else {
        // Persist productId in URL so refresh won't lose it
        navigate(`/create?productId=${res.product.id}`, { replace: true })
        setStep('done')
        toast('Product created successfully!', 'success')
      }
    } catch (e: unknown) {
      toast(`Failed to create product: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || !productId) return
    const q = questions[currentQ]
    setMessages(m => [...m, { role: 'user', text: answer.trim() }])
    setLoading(true)
    try {
      const res = await submitDiscovery(productId, q, answer.trim())
      setAnswer('')

      if (res.is_complete || res.follow_up_questions.length === 0) {
        setMessages(m => [...m, { role: 'system', text: 'Discovery complete! Your product is ready.' }])
        navigate(`/create?productId=${productId}`, { replace: true })
        setStep('done')
        toast('Discovery complete!', 'success')
      } else {
        setQuestions(res.follow_up_questions)
        setCurrentQ(0)
        setMessages(m => [...m, { role: 'system', text: res.follow_up_questions[0] }])
      }
    } catch (e: unknown) {
      toast(`Failed to submit answer: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  if (step === 'done') {
    return (
      <div>
        <div className="page-header">
          <h1 className="page-title">Product Created</h1>
          <p className="page-subtitle">Your product is ready for feature map generation.</p>
        </div>
        {messages.length > 0 && (
          <div className="chat" style={{ marginBottom: 32 }}>
            {messages.map((m, i) => (
              <div key={i} className={`chat-bubble ${m.role}`}>{m.text}</div>
            ))}
          </div>
        )}
        <div className="card" style={{ maxWidth: 500, padding: 32, textAlign: 'center' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>&#10003;</div>
          <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8 }}>Ready to go!</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>
            Next step: generate the feature map for your product.
          </p>
          <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
            {productId && (
              <button className="btn btn-primary" onClick={() => navigate(`/products/${productId}`)}>
                Go to Product
              </button>
            )}
            <button className="btn btn-secondary" onClick={() => navigate('/products')}>
              My Products
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Create Product</h1>
        <p className="page-subtitle">
          {step === 'idea'
            ? 'Describe your product idea in detail. Tell us what problem it solves, who the users are, and what it should do.'
            : 'Answer discovery questions to refine your product.'}
        </p>
      </div>

      {step === 'idea' && (
        <div style={{ maxWidth: 700 }}>
          <div className="form-group">
            <label className="form-label">Product Idea</label>
            <textarea
              className="textarea"
              placeholder="Example: A task management app for remote teams that integrates with Slack, supports time tracking, and provides weekly productivity reports..."
              value={idea}
              onChange={e => setIdea(e.target.value)}
              rows={6}
              disabled={loading}
              autoFocus
            />
            <div style={{ marginTop: 8, fontSize: 12, color: idea.trim().length < 10 ? 'var(--text-muted)' : 'var(--success)' }}>
              {idea.trim().length}/10 characters minimum
            </div>
          </div>
          <button
            className="btn btn-primary btn-lg"
            onClick={handleSubmitIdea}
            disabled={loading || idea.trim().length < 10}
          >
            {loading ? <><span className="spinner" /> Creating...</> : 'Create Product'}
          </button>
        </div>
      )}

      {step === 'discovery' && (
        <div className="chat">
          {messages.map((m, i) => (
            <div key={i} className={`chat-bubble ${m.role}`}>{m.text}</div>
          ))}
          {loading && (
            <div className="loading-overlay">
              <span className="spinner" /> Processing...
            </div>
          )}
          <div className="chat-input-row">
            <input
              className="input"
              placeholder="Type your answer..."
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !loading && answer.trim() && handleSubmitAnswer()}
              disabled={loading}
              autoFocus
            />
            <button className="btn btn-primary" onClick={handleSubmitAnswer} disabled={loading || !answer.trim()}>
              {loading ? <span className="spinner" /> : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
