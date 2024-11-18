import React, { useState } from 'react';
import Navbar from './Navbar';
import DraggableSquare from './DraggableSquare';
import DropZone from './DropZone';

function App() {
  const [droppedItems, setDroppedItems] = useState([]);

  const handleDrop = (item) => {
    // Add the dropped item to the list
    setDroppedItems((prevItems) => [...prevItems, item]);
  };

  const handleRemove = (id) => {
    // Remove the item with the given ID
    setDroppedItems((prevItems) => prevItems.filter(item => item.id !== id));
  };

  return (
    <div className="App">
      <Navbar />
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
        {/* Draggable squares */}
        <div>
          <h3>Draggable Squares</h3>
          <DraggableSquare id="1" color="red" />
          <DraggableSquare id="2" color="blue" />
          <DraggableSquare id="3" color="green" />
          <DraggableSquare id="4" color="yellow" />
        </div>

        {/* Drop target */}
        <DropZone
          droppedItems={droppedItems}
          onDrop={handleDrop}
          onRemove={handleRemove}
        />
      </div>
    </div>
  );
}

export default App;
