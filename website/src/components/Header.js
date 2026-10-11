import React from "react";

function Header({ currentView, onViewChange }) {
  return (
    <header className="site-header">
      <div className="header-inner">
        <div className="logo-group">
          <div className="logo-icon">N</div>
          <div>
            <h1 className="logo">NewsFlow AI</h1>
            <p className="tagline">
              AI-powered daily news intelligence
            </p>
          </div>
        </div>

        <div className="header-right">
          <nav className="nav-links">
            <button
              className={
                currentView === "today"
                  ? "nav-link active"
                  : "nav-link"
              }
              onClick={() => onViewChange("today")}
            >
              Today
            </button>

            <button
              className={
                currentView === "archive"
                  ? "nav-link active"
                  : "nav-link"
              }
              onClick={() => onViewChange("archive")}
            >
              Archive
            </button>
          </nav>

          <div className="status">
            <span className="status-dot"></span>
            <span>Live</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;