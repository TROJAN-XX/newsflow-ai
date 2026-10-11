import React from "react";

const CATEGORY_ICONS = {
  all: "◉",
  world: "🌍",
  technology: "⚡",
  business: "📈",
  science: "🔬",
  health: "🏥",
  sports: "⚽",
  entertainment: "🎬",
  politics: "🏛️",
  other: "📰"
};

function CategoryBar({
  categories,
  selectedCategory,
  onCategoryChange
}) {
  const categoryList = [
    "all",
    ...Object.keys(categories || {})
  ];

  return (
    <nav className="category-bar" role="tablist">
      {categoryList.map((category) => {
        const count =
          category === "all"
            ? Object.values(categories || {}).reduce(
                (sum, n) => sum + n,
                0
              )
            : categories[category] || 0;

        const icon = CATEGORY_ICONS[category] || "📰";

        return (
          <button
            key={category}
            role="tab"
            aria-selected={selectedCategory === category}
            className={
              selectedCategory === category
                ? "category-button active"
                : "category-button"
            }
            onClick={() => onCategoryChange(category)}
          >
            <span>{icon}</span>{" "}
            {category === "all"
              ? "All"
              : category.charAt(0).toUpperCase() +
                category.slice(1)}
            <span style={{
              opacity: 0.6,
              marginLeft: 4,
              fontSize: "0.85em"
            }}>
              {count}
            </span>
          </button>
        );
      })}
    </nav>
  );
}

export default CategoryBar;