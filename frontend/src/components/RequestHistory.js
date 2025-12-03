import React, { useEffect, useState } from 'react';
import {
  Container, Box, Typography, CssBaseline, List, ListItem, Link
} from '@mui/material';
import Header from '../components/Header'; // Import the Header component

const backendUrl = 'http://5.10.248.171:5000'; // Your backend URL

const RequestHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Retrieve history from local storage
    const savedHistory = JSON.parse(localStorage.getItem('resultIds')) || [];
    setHistory(savedHistory);
  }, []);

  return (
    <Container
      component="main"
      maxWidth="md"
      sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}
    >
      <CssBaseline />
      <Header title="History" /> {/* Use the Header component */}
      <Box
        sx={{
          mt: 8,
          p: 3,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          boxShadow: 3,
          borderRadius: 2,
          backgroundColor: '#fff',
          flex: 1,
        }}
      >
        <Typography variant="h4" gutterBottom>
          Request History
        </Typography>
        <List>
          {history.length > 0 ? (
            history.map((id, index) => (
              <ListItem key={index}>
                <Link href={`${backendUrl}/get_summary/${id}`} target="_blank" rel="noopener noreferrer">
                  View Summary for Request ID: {id}
                </Link>
              </ListItem>
            ))
          ) : (
            <Typography variant="body1">No history available.</Typography>
          )}
        </List>
      </Box>
      <footer
        style={{
          padding: '1rem',
          marginTop: 'auto',
          textAlign: 'center',
          backgroundColor: '#f5f5f5',
          margin: '1rem 0',
        }}
      >
        <Typography variant="body2" color="textSecondary">
          &copy; 2024 My Company. All rights reserved.
        </Typography>
      </footer>
    </Container>
  );
};

export default RequestHistory;
