import React from "react";
import "./Wardrobe.css";

export default function Wardrobe({
  selectedItems,
  onRemoveItem,
  onSelectItem,
}) {
  const categories = ["Accessories", "Hats", "Tees", "Pants", "Shoes"];

  const totalCost = selectedItems.reduce((sum, item) => {
    const price = parseFloat(item.price?.replace(/[^0-9.]/g, "")) || 0;
    return sum + price;
  }, 0);

  return (
    <div className="wardrobe">
      <h2>Wardrobe</h2>
      {categories.map((cat) => {
        const item = selectedItems.find((i) => i.category === cat);
        return (
          <div key={cat} className={`wardrobe-slot ${cat.toLowerCase()}`}>
            {item && (
              <div
                className="wardrobe-item-wrapper"
                onClick={() => onSelectItem(item)}
              >
                <img
                  src={`data:image/png;base64,${item.images_upd}`}
                  alt={item.title}
                  title={item.title}
                  className="wardrobe-item"
                />
                <div
                  className="item-actions"
                  onClick={(e) => e.stopPropagation()}
                >
                  <button
                    className="remove-btn"
                    onClick={() => onRemoveItem(item.category)}
                  >
                    ×
                  </button>
                  <a
                    className="view-link"
                    href={item.link}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    view
                  </a>
                </div>
              </div>
            )}
          </div>
        );
      })}
      <div className="wardrobe-total">Total: ${totalCost.toFixed(2)}</div>
    </div>
  );
}
