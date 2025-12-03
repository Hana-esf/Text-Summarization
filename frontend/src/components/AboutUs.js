import React from 'react';
import {
  Container, Box, Typography, CssBaseline
} from '@mui/material';
import Header from '../components/Header'; // Import the Header component

const AboutUs = () => {
  return (
    <Container
      component="main"
      maxWidth="md"
      sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}
    >
      <CssBaseline />
      <Header title="About Us"/> {/* Use the Header component */}
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
        {/* <Typography variant="h4" gutterBottom>
          About Us
        </Typography> */}
        <Typography variant="body1" paragraph>
          Welcome to our company! We are dedicated to providing the best services and solutions. Our team is composed of highly skilled professionals who are passionate about what they do. 
          Learn more about our mission, values, and history here.
        </Typography>
        {/* Add more content about your company here */}
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

export default AboutUs;
