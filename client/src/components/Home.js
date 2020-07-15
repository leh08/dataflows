import React from 'react';
import { Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  root: {
    margin: "15px",
    width: '100%',
    maxWidth: 500,
  },
});

export default () => {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Typography variant="h5" gutterBottom>
                Welcome to home page
            </Typography>
        </div>
    );
};