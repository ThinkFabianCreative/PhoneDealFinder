import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme, CssBaseline, Container, Grid, Box, CircularProgress, Alert } from '@mui/material';
import Header from './components/Header';
import PriceCard from './components/PriceCard';
import PriceChart from './components/PriceChart';

// Material 3 theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#9c27b0',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
  shape: {
    borderRadius: 12,
  },
});

const MODELS = ['iPhone 15 Pro Max', 'iPhone 16 Pro Max', 'iPhone 17 Pro Max'];

function App() {
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPrices();
    // Refresh every 5 minutes
    const interval = setInterval(fetchPrices, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const fetchPrices = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/prices');
      if (!response.ok) {
        throw new Error('Failed to fetch prices');
      }
      const data = await response.json();
      setPrices(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching prices:', err);
    } finally {
      setLoading(false);
    }
  };

  const getLatestPrice = (model) => {
    const modelPrices = prices.filter(p => p.model === model);
    if (modelPrices.length === 0) return null;
    modelPrices.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    return modelPrices[0];
  };

  const getPreviousPrice = (model) => {
    const modelPrices = prices.filter(p => p.model === model);
    if (modelPrices.length < 2) return null;
    modelPrices.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    return modelPrices[1];
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              {MODELS.map((model) => {
                const latest = getLatestPrice(model);
                const previous = getPreviousPrice(model);
                return (
                  <Grid item xs={12} sm={6} md={4} key={model}>
                    <PriceCard
                      model={model}
                      currentPrice={latest?.price || null}
                      previousPrice={previous?.price || null}
                      source={latest?.source || 'unknown'}
                      url={latest?.url || null}
                      imageUrl={latest?.image_url || null}
                    />
                  </Grid>
                );
              })}
            </Grid>

            <Grid container spacing={3}>
              {MODELS.map((model) => (
                <Grid item xs={12} key={model}>
                  <PriceChart prices={prices} model={model} />
                </Grid>
              ))}
            </Grid>
          </>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;

