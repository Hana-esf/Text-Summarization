import React, { useState } from 'react';
import {
  AppBar, Toolbar, IconButton, Typography, Box, Menu, MenuItem
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link as RouterLink } from 'react-router-dom';

const Header = ({ title }) => {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static">
      <Toolbar
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: { xs: '8px 16px', sm: '8px 24px' },
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenuOpen}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleMenuClose} component={RouterLink} to="/">
              Home
            </MenuItem>
            <MenuItem onClick={handleMenuClose} component={RouterLink} to="/about">
              About Us
            </MenuItem>
            <MenuItem onClick={handleMenuClose} component={RouterLink} to="/history">
              History
            </MenuItem>
          </Menu>
        </Box>

        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center', fontSize: { xs: '1rem', sm: '1.25rem' } }}>
          {title}
        </Typography>

        <Box sx={{ minWidth: '64px' }} /> {/* Space placeholder for centering */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
