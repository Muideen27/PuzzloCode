import React, { useState, useEffect } from 'react';

function QuestionLayout() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  // Function to fetch questions from the Flask backend
  const fetchQuestions = async (count = 1) => {
    try {
      const response = await fetch(`/api/questions?count=${count}`);
      if (response.ok) {
        const data = await response.json();
        setQuestions(data);
      } else {
        console.error('Error fetching questions:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  useEffect(() => {
    fetchQuestions();  // Fetch the first question when the component mounts.
  }, []);

  // Rest of your component code...

  return (
    <div>
      {/* Render questions and controls here */}
    </div>
  );
}

export default QuestionLayout;