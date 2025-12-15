import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import PhoneIcon from '@mui/icons-material/Phone';

const Header = () => {
  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <PhoneIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          iPhone Price Monitor
        </Typography>
        <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
          <Typography variant="body2">
            Tracking iPhone 15/16/17 Pro Max (256GB)
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

