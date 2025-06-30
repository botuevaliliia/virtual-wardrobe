import { useEffect, useRef, useState } from "react";
import "./ImageGallery.css";

const categoryFiles = {
  Pants: "pants_images.json",
  Tees: "tee_images.json",
  Shoes: "shoe_images.json",
  Hats: "hat_images.json",
  Accessories: "acces_images.json",
};

export default function ImageGallery({ onSelectItem }) {
  const [images, setImages] = useState([]);
  const [selected, setSelected] = useState(null);
  const [category, setCategory] = useState("Pants");
  const [hovered, setHovered] = useState(null);
  const containerRef = useRef(null);

  const fetchData = (category) => {
    const file = categoryFiles[category];
    fetch(`/jsons/${file}`)
      .then((res) => res.json())
      .then((data) => {
        const takenSpots = [];
        const getSafePosition = (width = 100, height = 100) => {
          for (let i = 0; i < 1000; i++) {
            const x = Math.random() * (window.innerWidth - width);
            const y = Math.random() * (window.innerHeight - height);
            const tooClose = takenSpots.some(
              (spot) =>
                Math.abs(spot.x - x) < width && Math.abs(spot.y - y) < height
            );
            if (!tooClose) {
              takenSpots.push({ x, y });
              return { x, y };
            }
          }
          return { x: 50, y: 50 };
        };

        setImages(
          data.map((item, index) => {
            const { x, y } = getSafePosition();
            return {
              id: index,
              ...item,
              category,
              x,
              y,
              dx: (Math.random() - 0.5) * 0.2,
              dy: (Math.random() - 0.5) * 0.2,
              rotation: Math.random() * 360,
              dr: (Math.random() - 0.5) * 0.2,
              width: 100,
              height: 100,
            };
          })
        );
      });
  };

  useEffect(() => {
    fetchData(category);
  }, [category]);

  useEffect(() => {
    const interval = setInterval(() => {
      setImages((prev) =>
        prev.map((img, i, arr) => {
          let x = img.x + img.dx;
          let y = img.y + img.dy;
          let dx = img.dx;
          let dy = img.dy;

          const width = window.innerWidth;
          const height = window.innerHeight;

          if (x < 0 || x > width - img.width) dx *= -1;
          if (y < 0 || y > height - img.height) dy *= -1;

          for (let j = 0; j < arr.length; j++) {
            if (i === j) continue;
            const other = arr[j];
            const dist = Math.hypot(img.x - other.x, img.y - other.y);
            if (dist < img.width) {
              dx = -dx;
              dy = -dy;
              x += dx * 2;
              y += dy * 2;
              break;
            }
          }

          return {
            ...img,
            x,
            y,
            dx,
            dy,
            rotation: img.rotation + img.dr,
          };
        })
      );
    }, 30);

    return () => clearInterval(interval);
  }, []);

  return (
    <div ref={containerRef} className="floating-gallery">
      <div className="category-bar">
        {Object.keys(categoryFiles).map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            className={category === cat ? "active" : ""}
          >
            {cat}
          </button>
        ))}
      </div>
      <div className="top-info-bar">
        <div>{(hovered || selected)?.title || ":)"}</div>
        <div>{(hovered || selected)?.company || ""}</div>
        <div>{(hovered || selected)?.price || ""}</div>
        <div>
          {selected ? (
            <a
              href={(hovered || selected).link}
              target="_blank"
              rel="noopener noreferrer"
            >
              View Product
            </a>
          ) : null}
        </div>
      </div>
      {images.map((img) => (
        <img
          key={img.id}
          src={`data:image/png;base64,${img.images_upd}`}
          className="floating-img"
          style={{
            left: img.x,
            top: img.y,
            width: img.width,
            height: img.height,
            transform: `rotate(${img.rotation}deg)`,
          }}
          onClick={() => {
            setSelected(img);
            onSelectItem?.(img);
          }}
          onMouseEnter={() => setHovered(img)}
          // onMouseLeave={() => setHovered(null)}
          alt=""
        />
      ))}
    </div>
  );
}
