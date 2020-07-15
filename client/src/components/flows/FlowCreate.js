import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { createFlow } from '../../actions';
import FlowForm from './FlowForm';

import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    root: {
        margin: "15px",
        width: '100%',
        maxWidth: 500,
    },
});


class FlowCreate extends React.Component {
    onSubmit = (formValues) => {
        this.props.createFlow(formValues);
    }

    render() {
        const { classes } = this.props;

        return (
            <div className={classes.root}>
                <Typography variant="h5" gutterBottom>
                    Create a Flow
                </Typography>
                <FlowForm onSubmit={this.onSubmit} />
            </div>
        );
    }
}

export default compose(
    connect(
        null,
        { createFlow }
    ),
    withStyles(useStyles)
)(FlowCreate);