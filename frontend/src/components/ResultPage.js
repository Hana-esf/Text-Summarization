import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container, Typography, Box, CircularProgress, Alert, Rating, CssBaseline, Paper
} from '@mui/material';
import Header from './Header'; // Assuming you have this component available

//const backendUrl = process.env.REACT_APP_BACKEND_URL;
const backendUrl = 'http://5.10.248.171:5000';
function ResultPage() {
  const { id } = useParams();
  const [rating, setRating] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const response = await fetch(`${backendUrl}/get_summary/${id}`);
        if (!response.ok) {
          throw new Error('Summary not found');
        }
        const data = await response.json();
        setResult(data);
        setRating(data.score || 0);  // Set initial rating if already rated
      } catch (error) {
        console.error('Error fetching result:', error);
        setError('Failed to fetch the summary.');
      }
    };

    fetchResult();
  }, [id]);

  const handleRating = async (newRating) => {
    if (result && result.score !== null) {
      setError('This summary has already been rated.');
      return;
    }

    setRating(newRating);

    try {
      const response = await fetch(`${backendUrl}/rate_summary/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ score: newRating }),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Failed to rate the summary.');
        return;
      }

      const data = await response.json();
      setResult((prevResult) => ({ ...prevResult, score: data.score }));
      setError(null);
    } catch (error) {
      console.error('Error submitting rating:', error);
      setError('Failed to submit the rating.');
    }
  };

  return (
    <Container component="main" maxWidth="md">
      <CssBaseline />
      <Header title="Summary Result" />
      <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Result for Request ID: {id}
        </Typography>
        {error && <Alert severity="error">{error}</Alert>}
        {result ? (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6">Original Text:</Typography>
            <Typography variant="body1" paragraph>{result.original_text}</Typography>
            {/* {result.is_file && result.file_path && (
              <Typography variant="body1">
                <strong>File Path:</strong> <a href={`/${result.file_path}`} target="_blank" rel="noopener noreferrer">{result.file_path}</a>
              </Typography>
            )} */}
            <Typography variant="h6" sx={{ mt: 2 }}>Summarized Text:</Typography>
            <Typography variant="body1" paragraph>{result.summarized}</Typography>
            {/* <Typography variant="h6">Score:</Typography>
            <Typography variant="body1">
              {result.score !== null ? result.score : 'Not rated yet'}
            </Typography> */}
            {/* <Typography variant="h6">Created Date:</Typography>
            <Typography variant="body1" paragraph>
              {new Date(result.created_date).toLocaleString()}
            </Typography> */}
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6">Rate this result:</Typography>
              <Rating
                name="summary-rating"
                value={rating}
                onChange={(event, newValue) => handleRating(newValue)}
                max={10}
              />
            </Box>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default ResultPage;
