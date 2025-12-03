import React from 'react';
import { Button, Typography, Box } from '@mui/material';

const FileInput = ({ onChange }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%',
        border: '2px dashed #1976d2',
        borderRadius: 1,
        padding: 2,
        backgroundColor: '#fafafa',
        textAlign: 'center',
        cursor: 'pointer',
        '&:hover': {
          backgroundColor: '#e3f2fd',
        },
      }}
      component="label"
    >
      <input
        type="file"
        accept=".pdf, .txt"
        onChange={onChange}
        style={{ display: 'none' }}
      />
      <Typography variant="body1">Choose a file (PDF or TXT)</Typography>
      <Button variant="contained" color="primary" sx={{ mt: 2 }}>
        Choose File
      </Button>
    </Box>
  );
};

export default FileInput;
