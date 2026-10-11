import React from "react";

function DigestCard({ digest }) {
  if (!digest) return null;

  const {
    headline,
    intro,
    sections,
    model,
    generated_at
  } = digest;

  const formatTime = (isoStr) => {
    if (!isoStr) return "";
    try {
      return new Date(isoStr).toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit"
      });
    } catch {
      return "";
    }
  };

  const sectionEntries = Object.entries(sections || {});

  return (
    <section className="digest-section animate-in">
      <p className="eyebrow">AI DIGEST</p>

      <div className="digest-card">
        <div className="digest-header">
          <h2 className="digest-headline">
            {headline || "Today's News in Brief"}
          </h2>

          {model && (
            <span className="digest-model">
              {model}
              {generated_at && (
                <> · {formatTime(generated_at)}</>
              )}
            </span>
          )}
        </div>

        {intro && (
          <p className="digest-intro">{intro}</p>
        )}

        {sectionEntries.length > 0 && (
          <div className="digest-sections">
            {sectionEntries.map(([category, text]) => (
              <div
                key={category}
                className="digest-section-item"
              >
                <div className="digest-section-label">
                  {category}
                </div>
                <div className="digest-section-text">
                  {text}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

export default DigestCard;
