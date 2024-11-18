import React from 'react';
import { useDrop } from 'react-dnd';
import DraggableSquare from './DraggableSquare';

const DropZone = ({ droppedItems, onDrop, onRemove }) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: 'SQUARE',
    drop: (item) => onDrop(item),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  }));

  const handleSquareClick = (id) => {
    // Remove the square when clicked
    onRemove(id);
  };

  const handleDragLeave = (item) => {
    // Remove the item when dragged outside
    onRemove(item.id);
  };

  return (
    <div
      ref={drop}
      onDragLeave={() => handleDragLeave(droppedItems)}
      style={{
        width: '300px',
        height: '300px',
        backgroundColor: isOver ? 'rgba(0, 255, 0, 0.3)' : '#ddd',
        border: '2px dashed #333',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexWrap: 'wrap',
        margin: '20px',
        position: 'relative',
      }}
    >
      {droppedItems.map((item) => (
        <div
          key={item.id}
          style={{
            position: 'relative',
            cursor: 'move',
          }}
          onClick={() => handleSquareClick(item.id)} // Add click event to remove item
        >
          <DraggableSquare
            id={item.id}
            color={item.color}
          />
        </div>
      ))}
    </div>
  );
};

export default DropZone;
