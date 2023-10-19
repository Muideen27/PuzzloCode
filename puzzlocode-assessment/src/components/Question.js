// Question.js
import React from 'react';

const Question = ({ questionData, onAnswer }) => {
  const { question, choices } = questionData;

  const handleAnswer = (choice) => {
    onAnswer(choice);
  };

  return (
    <div>
      <h2>{question}</h2>
      <ul>
        {choices.map((choice, index) => (
          <li key={index}>
            <button onClick={() => handleAnswer(choice)}>{choice}</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Question;
