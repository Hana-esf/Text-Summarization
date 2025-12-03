import React, { useState } from 'react';
import {
  Container, TextField, Button, Box, Typography, Slider, CssBaseline, Switch, FormControlLabel
} from '@mui/material';
import Header from './Header'; // Import the Header component
import FileInput from './FileInput'; // Import the custom FileInput component

const backendUrl = 'http://5.10.248.171:5000';

const SummarizePage = () => {
  const [inputText, setInputText] = useState('');
  const [minSize, setMinSize] = useState(30);
  const [maxSize, setMaxSize] = useState(75);
  const [isFileInput, setIsFileInput] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleMinSizeChange = (event, newValue) => {
    setMinSize(newValue);
  };

  const handleMaxSizeChange = (event, newValue) => {
    setMaxSize(newValue);
  };

  const handleToggleChange = (event) => {
    setIsFileInput(event.target.checked);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && (file.type === 'application/pdf' || file.type === 'text/plain')) {
      setSelectedFile(file);
      console.log('Selected file:', file);
    } else {
      alert('Please select a PDF or TXT file.');
    }
  };

  const handleSubmit = () => {
    const url = isFileInput && selectedFile ? `${backendUrl}/process_file` : `${backendUrl}/process_text`;

    const requestBody = {
      is_file: isFileInput,
      minsize: minSize,
      maxsize: maxSize,
    };

    if (isFileInput && selectedFile) {
      // Convert the file to a base64 string
      const reader = new FileReader();
      reader.onloadend = () => {
        requestBody.file = reader.result.split(',')[1]; // Base64 encoded file
        sendRequest(requestBody, url);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      requestBody.text = inputText;
      sendRequest(requestBody, url);
    }
  };

  const sendRequest = (body, url) => {
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }
        return response.json();
      })
      .then((data) => {
        console.log('Response Data:', data);
        const { id } = data;
        if (id) {
          // Store the result ID in local storage
          const storedIds = JSON.parse(localStorage.getItem('resultIds')) || [];
          storedIds.push(id);
          localStorage.setItem('resultIds', JSON.stringify(storedIds));

          // Redirect to the result page
          window.location.href = `/result/${id}`;
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please check the console for details.');
      });
  };

  return (
    <Container
      component="main"
      maxWidth="sm"
      sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}
    >
      <CssBaseline />
      <Header title="Summarize"/> {/* Use the Header component */}
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
        <FormControlLabel
          control={<Switch checked={isFileInput} onChange={handleToggleChange} />}
          label={isFileInput ? 'Switch to Text Input' : 'Switch to File Input'}
        />

        {!isFileInput ? (
          <TextField
            label="Input Text"
            multiline
            rows={4}
            variant="outlined"
            fullWidth
            value={inputText}
            onChange={handleInputChange}
            sx={{ mb: 2 }}
          />
        ) : (
          <FileInput onChange={handleFileChange} />
        )}

        <Box mb={2} sx={{ width: '100%' }}>
          <Typography variant="h6">Min Size</Typography>
          <Slider
            value={minSize}
            onChange={handleMinSizeChange}
            aria-labelledby="min-size-slider"
            min={30}
            max={100}
            valueLabelDisplay="auto"
            sx={{ mb: 2 }}
          />
          <Typography variant="body1">Min Size Value: {minSize}</Typography>
        </Box>
        
        <Box mb={2} sx={{ width: '100%' }}>
          <Typography variant="h6">Max Size</Typography>
          <Slider
            value={maxSize}
            onChange={handleMaxSizeChange}
            aria-labelledby="max-size-slider"
            min={30}
            max={150}
            valueLabelDisplay="auto"
            sx={{ mb: 2 }}
          />
          <Typography variant="body1">Max Size Value: {maxSize}</Typography>
        </Box>

        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Send Request
        </Button>
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

export default SummarizePage;
