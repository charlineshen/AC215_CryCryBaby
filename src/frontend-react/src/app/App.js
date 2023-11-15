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


function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const tiers = [
  {
    title: 'Audio upload',
    price: '',
    pre_description: [
      'Let me hear the baby cry',
      '.',
      '.',
    ],
    post_description:[],
    buttonText: 'Upload',
    buttonVariant: 'outlined',
  },
  {
    title: 'Cry Detection',
    // subheader: 'Most popular',
    pre_description: [
      'This is',
    ],
    price: '15%',
    post_description: [
      'chance is a cry',
    ],
    // buttonText: 'Get started',
    // buttonVariant: 'contained',
  },
  {
    title: 'Needs classification',
    pre_description: [
      'Your baby seems',
      // '30 GB of storage',
      // 'Help center access',
      // 'Phone & email support',
    ],
    price: 'Hungry',
    post_description: [
      'based on our model',
    ],
    // buttonText: 'Contact us',
    // buttonVariant: 'outlined',
  },
];

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function Pricing() {

  const inputFile = useRef(null);
  // Component States
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);

  // Setup Component
  useEffect(() => {
  }, []);
  // Handlers
  const handleImageUploadClick = () => {
    inputFile.current.click();
  }
  const handleOnChange = (event) => {
    console.log(event.target.files);
    setImage(URL.createObjectURL(event.target.files[0]));

    var formData = new FormData();
    formData.append("file", event.target.files[0]);
    DataService.Predict(formData)
        .then(function (response) {
            console.log(response.data);
            setPrediction(response.data);
        })
  }
  
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
        <Toolbar sx={{ flexWrap: 'wrap' }}>
          <Typography variant="h6" color="inherit" noWrap sx={{ flexGrow: 1 }}>
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
        >
          Cry Cry Baby
        </Typography>
        <Typography variant="h5" align="center" color="text.secondary" component="p">
          Empowering Parenthood: Decoding Baby Cry Through AI Guidance
        </Typography>
      </Container>
      {/* End hero unit */}
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
                    backgroundColor: (theme) =>
                      theme.palette.mode === 'light'
                        ? theme.palette.grey[200]
                        : theme.palette.grey[700],
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
                      {tier.price}
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
                  <Button fullWidth variant={tier.buttonVariant} onClick={() => handleImageUploadClick()}>
                    {tier.buttonText}
                    <input
                      type="file"
                      accept="image/*"
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
