import React from 'react';
import { useDrag } from 'react-dnd';

const DraggableSquare = ({ id, color }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'SQUARE',
    item: { id, color },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <div
      ref={drag}
      style={{
        width: '100px',
        height: '100px',
        backgroundColor: color,
        opacity: isDragging ? 0.5 : 1,
        cursor: 'move',
        margin: '10px',
      }}
    />
  );
};

export default DraggableSquare;
