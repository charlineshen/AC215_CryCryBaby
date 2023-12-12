import React, { useEffect, useRef, useState } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import GlobalStyles from '@mui/material/GlobalStyles';
import Container from '@mui/material/Container';
import DataService from '../services/DataService';
import CircularProgress from '@mui/material/CircularProgress';


function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://github.com/charlineshen/AC215_CryCryBaby">
        CCB Team
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}



const defaultTheme = createTheme({
  palette: {
    primary: {
      main: '#9BCDD2', // A soft, warm color for primary elements
    },
    background: {
      default: '#FFFBEB', // A light, warm background color
      paper: '#faeee2', // A warmer shade for paper components
      toolbar: '#f5d5c0',
      cardheader: '#fadbd7',
    },
    // You can also adjust other color aspects of the theme as needed
  },
  // Include any other theme customizations here
});

export default function Display() {

  const inputFile = useRef(null);
  // Component States
  const [audio, setAudio] = useState(null);
  const [prediction, setPrediction] = useState({'cry': 0, 'label': ':)', 'prob': 0}); 
  const [testUpload, setTestUpload] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // <-- New state for loading
  const [error, setError] = useState(null); // New state for error message

  const noAudioUploadedPlaceholder = "No audio uploaded";
  const noCryDetectedPlaceholder = "Audio uploaded but no cry detected";

  // Setup Component
  useEffect(() => {
  }, []);
  
  const handleFileUploadAndPrediction = (file) => {
    const formData = new FormData();
    formData.append("file", file);

    setIsLoading(true);
    setError(null);

    DataService.TestUpload(formData)
      .then(response => {
        console.log("TestUpload Response:", response.data);
        setTestUpload(response.data);
      });

    DataService.Predict(formData)
      .then(response => {
        console.log("Prediction Response:", response.data);
        setPrediction(response.data);
      })
      .catch(error => {
        console.error("Error during prediction:", error);
        alert("Error occurred: " + error.message);
        setError("Error during prediction: " + error.message);
      })
      .finally(() => setIsLoading(false));
  };

  const tiers = [
    {
      title: 'Audio Upload',
      pre_description: [
        'Let me hear the baby cry',
        '.',
        'Upload filepath: ' + testUpload,
      ],
      prob: '',
      post_description:[],
      buttonText: 'Upload',
      buttonVariant: 'outlined',
    },
    {
      title: 'Cry Detection',
      pre_description: [
        audio ? 'Analyzing audio...' : noAudioUploadedPlaceholder,
      ],
      // Directly display the probability if audio is uploaded and prediction exists
      prob: audio ? `${prediction.cry}%` : '---', // Changed from prediction['cry'] to prediction.cry for consistency
      post_description: [
        audio ? 'Chance is a cry' : '',
      ],
    },
    {
      title: 'Needs classification',
      // Simplified the logic to check if audio is uploaded and the cry probability is more than 50
      pre_description: [
        audio && prediction.cry > 50 ? 'Analyzing needs...' : noCryDetectedPlaceholder,
      ],
      // Display the label if conditions are met
      prob: audio && prediction.cry > 50 ? prediction.label : '---',
      post_description: [
        audio && prediction.cry > 50 ? 'Based on our model' : '',
      ],
    },
  ];
  
  return (
    <ThemeProvider theme={defaultTheme}>
      <GlobalStyles styles={{ ul: { margin: 0, padding: 0, listStyle: 'none' } }} />
      <CssBaseline />
      <AppBar
        position="static"
        color="default"
        elevation={0}
        sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}
      >
        <Toolbar sx={{ bgcolor: 'background.toolbar', flexWrap: 'wrap' }}>
          <Typography variant="h6" color="inherit" noWrap sx={{ flexGrow: 1, fontFamily: 'fantasy', fontWeight: 'bold'}}>
            Cry Cry Baby
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Hero unit */}
      <Container disableGutters maxWidth="sm" component="main" sx={{ pt: 8, pb: 6 }}>
        <Typography
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
          sx={{ flexGrow: 1, fontFamily: 'fantasy', fontWeight: 'bold'}}
        >
          Cry Cry Baby 🍼
        </Typography>
        <Typography variant="h5" align="center" color="text.secondary" component="p" sx={{ fontFamily: 'cursive'}}>
          Empowering Parenthood: Decoding Baby Cry Through AI Guidance
        </Typography>
      </Container>
      {/* End hero unit */}

      {/* Loading indicator section */}
      {isLoading && (
        <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Waiting for model prediction
          </Typography>
          <CircularProgress color='secondary'/>
        </Box>
      )}

      {/* Error Message Display */}
      {error && (
        <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', p: 2 }}>
          <Typography variant="h6" color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        </Box>
      )}

      <Container maxWidth="md" component="main">
        <Grid container spacing={5} alignItems="flex-end">
          {tiers.map((tier) => (
            // Enterprise card is full width at sm breakpoint
            <Grid
              item
              key={tier.title}
              xs={12}
              sm={tier.title === 'Enterprise' ? 12 : 6}
              md={4}
            >
              <Card>
                <CardHeader
                  title={tier.title}
                  subheader={tier.subheader}
                  titleTypographyProps={{ align: 'center' }}
                  // action={tier.title === 'Pro' ? <StarIcon /> : null}
                  subheaderTypographyProps={{
                    align: 'center',
                  }}
                  sx={{
                    bgcolor: 'background.cardheader',
                  }}
                />
                <CardContent>
                <ul>
                    {tier.pre_description.map((line) => (
                      <Typography
                        component="li"
                        variant="subtitle1"
                        align="center"
                        key={line}
                      >
                        {line}
                      </Typography>
                    ))}
                  </ul>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'baseline',
                      mb: 2,
                    }}
                  >
                    <Typography component="h2" variant="h3" color="text.primary">
                      {tier.prob}
                    </Typography>
                    <Typography variant="h6" color="text.secondary">
                    </Typography>
                  </Box>
                  <ul>
                    {tier.post_description.map((line) => (
                      <Typography
                        component="li"
                        variant="subtitle1"
                        align="center"
                        key={line}
                      >
                        {line}
                      </Typography>
                    ))}
                  </ul>
                </CardContent>
                <CardActions>
                <Button fullWidth variant={tier.buttonVariant} color="secondary" onClick={() => handleImageUploadClick() }>
                    {tier.buttonText}
                    <input
                      type="file"
                      accept=".wav"
                      capture="camera"
                      autoComplete="off"
                      tabIndex="-1"
                      style={{ display: 'none' }}
                      ref={inputFile}
                      onChange={(event) => handleOnChange(event)}
                    />
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
      
      <Container
        maxWidth="md"
        component="footer"
        sx={{
          borderTop: (theme) => `1px solid ${theme.palette.divider}`,
          mt: 8,
          py: [3, 6],
        }}
      >
        
        <Copyright sx={{ mt: 5 }} />
      </Container>
      
    </ThemeProvider>
  );
}
