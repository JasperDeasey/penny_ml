import React, { useState, useEffect } from 'react';
import './FlowchartSlideshow.css';
import slide1 from '../../data/FlowChartSlideShow/Slide1.SVG';
import slide2 from '../../data/FlowChartSlideShow/Slide2.SVG';
import slide3 from '../../data/FlowChartSlideShow/Slide3.SVG';
import slide4 from '../../data/FlowChartSlideShow/Slide4.SVG';
import slide5 from '../../data/FlowChartSlideShow/Slide5.SVG';
import slide6 from '../../data/FlowChartSlideShow/Slide6.SVG';

const FlowchartSlideshow = () => {
  const images = [slide1, slide2, slide3, slide4, slide5, slide6];
  const [index, setIndex] = useState(0);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    if (paused) return;

    const timer = setTimeout(() => {
      setIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 5000); // Change image every 4 seconds

    return () => clearTimeout(timer);
  }, [index, paused]);

  const nextImage = () => setIndex((index + 1) % images.length);
  const prevImage = () => setIndex((index - 1 + images.length) % images.length);
  const togglePause = () => setPaused(!paused);

  return (
    <div className="slideshow-container">
      <img src={images[index]} alt="Slideshow" className="slideshow-image" />
      <div className="controls">
        <button onClick={prevImage} className="control-btn">←</button>
        <button onClick={togglePause} className="control-btn">
          {paused ? '▶' : '| |'}
        </button>
        <button onClick={nextImage} className="control-btn">→</button>
      </div>
      <div className="dots-container">
        {images.map((_, idx) => (
          <span
            key={idx}
            className={`dot ${idx === index ? 'active' : ''}`}
            onClick={() => setIndex(idx)}
          ></span>
        ))}
      </div>
    </div>
  );
};

export default FlowchartSlideshow;
