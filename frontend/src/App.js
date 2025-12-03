import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SummarizePage from './components/SummarizePage';
import ResultPage from './components/ResultPage';
import RequestHistory from './components/RequestHistory';
import AboutUs from './components/AboutUs';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SummarizePage />} />
        <Route path="/result/:id" element={<ResultPage />} />
        <Route path="/history" element={<RequestHistory />} />
        <Route path="/about" element={<AboutUs />} />
      </Routes>
    </Router>
  );
}

export default App;
