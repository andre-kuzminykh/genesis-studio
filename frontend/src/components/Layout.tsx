import { NavLink, Outlet } from 'react-router-dom'

export default function Layout() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-logo">Genesis Studio</div>
        <nav className="sidebar-nav">
          <NavLink to="/" end className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
            <span>&#9670;</span> Home
          </NavLink>
          <NavLink to="/create" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
            <span>&#43;</span> Create Product
          </NavLink>
          <NavLink to="/products" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
            <span>&#9776;</span> My Products
          </NavLink>
        </nav>
        <div style={{ borderTop: '1px solid var(--border)', paddingTop: 16 }}>
          <a href="https://github.com" target="_blank" rel="noreferrer" className="sidebar-link">
            <span>&#128279;</span> GitHub
          </a>
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
