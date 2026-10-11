import React, { useEffect, useMemo, useState, useCallback } from "react";

import Header from "./components/Header";
import CategoryBar from "./components/CategoryBar";
import DateSelector from "./components/DateSelector";
import DigestCard from "./components/DigestCard";
import SearchBar from "./components/SearchBar";
import NewsCard from "./components/NewsCard";

function App() {
  const [archive, setArchive] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [currentView, setCurrentView] = useState("today");

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/news_archive.json`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load news archive.");
        }
        return response.json();
      })
      .then((data) => {
        setArchive(data);
        const dates = Object.keys(data).sort().reverse();
        if (dates.length > 0) {
          setSelectedDate(dates[0]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const dates = useMemo(() => {
    if (!archive) return [];
    return Object.keys(archive).sort().reverse();
  }, [archive]);

  const handleDateChange = useCallback((date) => {
    setSelectedDate(date);
    setSelectedCategory("all");
    setSearchQuery("");
  }, []);

  const handleViewChange = useCallback((view) => {
    setCurrentView(view);
    setSearchQuery("");
    setSelectedCategory("all");
  }, []);

  // ── Loading ────────────────────────────────────

  if (loading) {
    return (
      <div className="app">
        <div className="loading-screen">
          <div className="loading-spinner"></div>
          <h1>NewsFlow AI</h1>
          <p>Loading today's intelligence...</p>
        </div>
      </div>
    );
  }

  // ── Error ──────────────────────────────────────

  if (error) {
    return (
      <div className="app">
        <div className="error-screen">
          <h1>NewsFlow AI</h1>
          <p>Unable to load the news archive.</p>
          <small>{error}</small>
        </div>
      </div>
    );
  }

  // ── Empty ──────────────────────────────────────

  if (!archive || dates.length === 0) {
    return (
      <div className="app">
        <div className="empty-screen">
          <h1>NewsFlow AI</h1>
          <p>No news editions available yet.</p>
          <p style={{ fontSize: 13, opacity: 0.5 }}>
            Run the pipeline to generate your first edition.
          </p>
        </div>
      </div>
    );
  }

  // ── Data ───────────────────────────────────────

  const edition = archive[selectedDate];
  const stats = edition?.statistics || {};
  const digest = edition?.daily_digest;

  // Filter by category
  let articles = edition?.articles || [];

  if (selectedCategory !== "all") {
    articles = articles.filter(
      (a) => a.category === selectedCategory
    );
  }

  // Filter by search query
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase();
    articles = articles.filter((a) => {
      const title = (a.title || "").toLowerCase();
      const summary = (a.ai?.summary || "").toLowerCase();
      const source = (a.source?.name || "").toLowerCase();
      const keywords = (a.ai?.keywords || [])
        .join(" ")
        .toLowerCase();
      return (
        title.includes(q) ||
        summary.includes(q) ||
        source.includes(q) ||
        keywords.includes(q)
      );
    });
  }

  // ── Today View ─────────────────────────────────

  const renderToday = () => (
    <>
      {/* Hero */}
      <section className="hero animate-in">
        <div className="hero-content">
          <p className="eyebrow">DAILY INTELLIGENCE</p>
          <h2>Today's News</h2>
          <p>
            AI-curated summaries from {" "}
            {stats.articles_collected || 0} sources,
            distilled into actionable intelligence.
          </p>
        </div>

        <DateSelector
          dates={dates}
          selectedDate={selectedDate}
          onDateChange={handleDateChange}
        />
      </section>

      {/* Stats */}
      <section className="stats animate-in">
        <div className="stat">
          <span className="stat-value">
            {stats.total_articles || 0}
          </span>
          <span className="stat-label">Stories</span>
        </div>

        <div className="stat">
          <span className="stat-value">
            {Object.keys(edition?.categories || {}).length}
          </span>
          <span className="stat-label">Categories</span>
        </div>

        <div className="stat">
          <span className="stat-value">
            {stats.duplicates_removed || 0}
          </span>
          <span className="stat-label">
            Duplicates Filtered
          </span>
        </div>

        <div className="stat">
          <span className="stat-value">
            {stats.ai_processed || stats.total_articles || 0}
          </span>
          <span className="stat-label">AI Processed</span>
        </div>
      </section>

      {/* Digest */}
      {digest && <DigestCard digest={digest} />}

      {/* Search + Category */}
      <SearchBar
        query={searchQuery}
        onQueryChange={setSearchQuery}
      />

      <CategoryBar
        categories={edition?.categories}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      {/* Articles */}
      <section className="news-section">
        <div className="section-heading">
          <p className="eyebrow">
            {selectedCategory === "all"
              ? "ALL STORIES"
              : selectedCategory.toUpperCase()}
          </p>
          <h2>
            {articles.length}{" "}
            {articles.length === 1 ? "Story" : "Stories"}
            {searchQuery && (
              <span style={{
                fontSize: "0.6em",
                color: "var(--text-muted)",
                fontWeight: 400,
                marginLeft: 12
              }}>
                matching "{searchQuery}"
              </span>
            )}
          </h2>
        </div>

        <div className="news-grid">
          {articles.length > 0 ? (
            articles.map((article) => (
              <NewsCard
                key={article.id}
                article={article}
              />
            ))
          ) : (
            <div className="no-results">
              <div className="no-results-icon">🔍</div>
              <h3>No articles found</h3>
              <p>
                Try adjusting your search or category filter.
              </p>
            </div>
          )}
        </div>
      </section>
    </>
  );

  // ── Archive View ───────────────────────────────

  const renderArchive = () => (
    <>
      <section className="hero animate-in">
        <div className="hero-content">
          <p className="eyebrow">NEWS ARCHIVE</p>
          <h2>Past Editions</h2>
          <p>
            Browse {dates.length} edition{dates.length !== 1 ? "s" : ""}{" "}
            of AI-curated news intelligence.
          </p>
        </div>
      </section>

      <div className="news-grid" style={{ gap: 14 }}>
        {dates.map((date) => {
          const ed = archive[date];
          const edStats = ed?.statistics || {};
          const edDigest = ed?.daily_digest;

          return (
            <article
              key={date}
              className="news-card"
              style={{ cursor: "pointer" }}
              onClick={() => {
                setSelectedDate(date);
                setCurrentView("today");
              }}
            >
              <div className="news-content">
                <div className="news-meta">
                  <span className="category-tag">
                    EDITION
                  </span>
                  <span className="source-name">
                    {edStats.total_articles || 0} stories
                  </span>
                </div>

                <h3>
                  {new Date(date + "T00:00:00").toLocaleDateString(
                    "en-US",
                    {
                      weekday: "long",
                      month: "long",
                      day: "numeric",
                      year: "numeric"
                    }
                  )}
                </h3>

                <p className="news-summary">
                  {edDigest?.intro ||
                    `${edStats.total_articles || 0} articles across ${
                      Object.keys(ed?.categories || {}).length
                    } categories.`}
                </p>

                {ed?.categories && (
                  <div className="keywords" style={{ marginTop: 14 }}>
                    {Object.entries(ed.categories).map(
                      ([cat, count]) => (
                        <span key={cat} className="keyword-tag">
                          {cat} ({count})
                        </span>
                      )
                    )}
                  </div>
                )}

                <div className="news-footer">
                  <span>
                    {edStats.duplicates_removed || 0} duplicates
                    filtered
                  </span>
                  <span style={{ color: "var(--text-accent)", fontWeight: 700 }}>
                    View edition <span className="arrow">→</span>
                  </span>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </>
  );

  // ── Render ─────────────────────────────────────

  return (
    <div className="app">
      <Header
        currentView={currentView}
        onViewChange={handleViewChange}
      />

      <main className="container">
        {currentView === "today"
          ? renderToday()
          : renderArchive()}
      </main>

      <footer className="site-footer">
        <div className="footer-inner">
          <span className="footer-brand">
            <strong>NewsFlow AI</strong> · AI-powered news intelligence
          </span>
          <div className="footer-links">
            <a
              href="https://github.com/TROJAN-XX/newsflow-ai"
              target="_blank"
              rel="noreferrer"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;