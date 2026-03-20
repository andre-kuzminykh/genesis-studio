import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'

export default function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <div className="layout">
      {/* Mobile hamburger */}
      <button className="mobile-menu-btn" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">
        &#9776;
      </button>

      {/* Overlay for mobile */}
      {mobileOpen && <div className="sidebar-overlay" onClick={() => setMobileOpen(false)} />}

      <aside className={`sidebar ${mobileOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-logo">Genesis Studio</div>
        <nav className="sidebar-nav">
          <NavLink to="/" end className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`} onClick={() => setMobileOpen(false)}>
            <span>&#9670;</span> Home
          </NavLink>
          <NavLink to="/create" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`} onClick={() => setMobileOpen(false)}>
            <span>&#43;</span> Create Product
          </NavLink>
          <NavLink to="/products" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`} onClick={() => setMobileOpen(false)}>
            <span>&#9776;</span> My Products
          </NavLink>
        </nav>
        <div style={{ borderTop: '1px solid var(--border)', paddingTop: 16, fontSize: 12, color: 'var(--text-muted)' }}>
          Genesis Studio v1.0
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
