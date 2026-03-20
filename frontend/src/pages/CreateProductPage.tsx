import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createProduct, submitDiscovery } from '../api/client'
import { useToast } from '../components/Toast'

interface ChatMessage {
  role: 'system' | 'user'
  text: string
}

export default function CreateProductPage() {
  const navigate = useNavigate()
  const toast = useToast()
  const [step, setStep] = useState<'idea' | 'discovery' | 'done'>('idea')
  const [idea, setIdea] = useState('')
  const [loading, setLoading] = useState(false)
  const [productId, setProductId] = useState<string | null>(null)
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
        setStep('done')
        toast('Product created successfully!', 'success')
      }
    } catch (e: unknown) {
      toast(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
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
        setStep('done')
        toast('Discovery complete!', 'success')
      } else {
        setQuestions(res.follow_up_questions)
        setCurrentQ(0)
        setMessages(m => [...m, { role: 'system', text: res.follow_up_questions[0] }])
      }
    } catch (e: unknown) {
      toast(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`, 'error')
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
        <div className="chat">
          {messages.map((m, i) => (
            <div key={i} className={`chat-bubble ${m.role}`}>{m.text}</div>
          ))}
          <div className="chat-bubble system">Discovery complete! Your product is ready.</div>
        </div>
        <div style={{ marginTop: 32, display: 'flex', gap: 12 }}>
          <button className="btn btn-primary" onClick={() => navigate(`/products/${productId}`)}>
            Go to Product
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/products')}>
            My Products
          </button>
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
              placeholder="Describe your product idea..."
              value={idea}
              onChange={e => setIdea(e.target.value)}
              rows={6}
              disabled={loading}
            />
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
              onKeyDown={e => e.key === 'Enter' && handleSubmitAnswer()}
              disabled={loading}
            />
            <button className="btn btn-primary" onClick={handleSubmitAnswer} disabled={loading || !answer.trim()}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
