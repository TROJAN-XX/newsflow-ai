import React from "react";

function NewsCard({ article }) {
  const {
    title,
    description,
    original_url,
    published_at,
    category,
    author,
    image_url,
    source,
    ai
  } = article;

  const summary =
    ai?.summary || description || "No summary available.";

  const formatDate = (dateStr) => {
    if (!dateStr) return "Unknown date";
    try {
      const date = new Date(dateStr);
      const now = new Date();
      const diffMs = now - date;
      const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));

      if (diffHrs < 1) return "Just now";
      if (diffHrs < 24) return `${diffHrs}h ago`;
      if (diffHrs < 48) return "Yesterday";

      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric"
      });
    } catch {
      return "Unknown date";
    }
  };

  const importance = ai?.importance;
  const maxImportance = 10;

  return (
    <article className="news-card" id={`card-${article.id}`}>

      {image_url ? (
        <div className="news-image-wrapper">
          <img
            className="news-image"
            src={image_url}
            alt=""
            loading="lazy"
            onError={(e) => {
              e.target.parentElement.style.display = "none";
            }}
          />
        </div>
      ) : (
        <div className="news-image-placeholder">
          📰
        </div>
      )}

      <div className="news-content">
        <div className="news-meta">
          <span className="category-tag">
            {category}
          </span>

          <span className="source-name">
            {source?.name || "Unknown source"}
          </span>
        </div>

        <h3>{title}</h3>

        <p className="news-summary">
          {summary}
        </p>

        {ai?.key_points?.length > 0 && (
          <ul className="key-points">
            {ai.key_points.slice(0, 3).map(
              (point, index) => (
                <li key={index}>
                  {point}
                </li>
              )
            )}
          </ul>
        )}

        {importance != null && (
          <div className="importance-bar">
            <span className="importance-label">
              Impact
            </span>
            <div className="importance-dots">
              {Array.from({ length: maxImportance }).map(
                (_, i) => (
                  <span
                    key={i}
                    className={
                      i < importance
                        ? "importance-dot filled"
                        : "importance-dot"
                    }
                  />
                )
              )}
            </div>
          </div>
        )}

        {ai?.keywords?.length > 0 && (
          <div className="keywords">
            {ai.keywords.map((keyword) => (
              <span key={keyword} className="keyword-tag">
                #{keyword}
              </span>
            ))}
          </div>
        )}

        <div className="news-footer">
          <span>
            {author
              ? `${author} · ${formatDate(published_at)}`
              : formatDate(published_at)}
          </span>

          <a
            href={original_url}
            target="_blank"
            rel="noreferrer"
          >
            Read original{" "}
            <span className="arrow">→</span>
          </a>
        </div>
      </div>
    </article>
  );
}

export default NewsCard;