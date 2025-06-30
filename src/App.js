import React, { useState } from "react";
import ImageGallery from "./ImageGallery";
import Wardrobe from "./Wardrobe";
import "./App.css";

function App() {
  const [selectedItems, setSelectedItems] = useState([]);
  const [highlightedItem, setHighlightedItem] = useState(null);

  const handleSelectItem = (item) => {
    setSelectedItems((prev) => {
      const filtered = prev.filter((i) => i.category !== item.category);
      return [...filtered, item];
    });
    setHighlightedItem(item);
  };

  const handleRemoveItem = (category) => {
    setSelectedItems((prev) => prev.filter((i) => i.category !== category));
  };

  return (
    <div className="app-container">
      <div className="left-panel">
        <Wardrobe
          selectedItems={selectedItems}
          onRemoveItem={handleRemoveItem}
          onSelectItem={handleSelectItem}
        />
      </div>

      <div className="right-panel">
        <ImageGallery onSelectItem={handleSelectItem} />
      </div>
    </div>
  );
}

export default App;
