// AppRouter.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import QuestionLayout from './QuestionLayout'; // Import your QuestionLayout component

function AppRouter() {
  return (
    <Router>
      <Switch>
        {/* Define your routes here */}
        <Route path="/html-assessment-questions" component={QuestionLayout} />
        {/* Add more routes as needed */}
      </Switch>
    </Router>
  );
}

export default AppRouter;
