import _ from 'lodash';
import React from 'react';
import { compose } from 'redux';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { fetchSources } from '../../actions';

import { 
    TextField,
    Button,
} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

import SourceAutocomplete from './fields/SourceAutocomplete';
import AuthorizationAutocomplete from './fields/AuthorizationAutocomplete';
import ParserSelect from './fields/ParserSelect';
import StoreSelect from './fields/StoreSelect';
import LoadSelect from './fields/LoadSelect';
import FrequencySelect from './fields/FrequencySelect';
import ModelSelect from './fields/ModelSelect';
import DaySelect from './fields/DaySelect';
import HourSelect from './fields/HourSelect';


const useStyles = theme => ({
    root: {
        '& .MuiTextField-root': {
          margin: theme.spacing(1.25),
          width: 450,
        },
    },
});


class FlowForm extends React.Component {
    state = { source_name: null }

    componentDidMount() {
        this.props.fetchSources()
    }

    renderInput = ({ input, label, meta }) => {
        if (meta.error && meta.touched) {
            return (
                <div>
                    <TextField error helperText={meta.error} id="standard-error-helper-text" label={label} {...input} />
                </div>
            );
        } else {
            return (
                <div>
                    <TextField id="standard-basic" label={label} {...input} />
                </div>
            );
        }
    }

    handleChoose = (value) => {
        this.setState(
            { source_name: value }
        )
    }

    onSubmit = (formValues) => {
        this.props.onSubmit(formValues);
    }

    render() {
        const { classes } = this.props;

        if (this.props.sources) {
            return (
                <form onSubmit={this.props.handleSubmit(this.onSubmit)} className={classes.root} noValidate autoComplete="off">
                    <Field name="source_name" component={SourceAutocomplete} sources={this.props.sources} handleChoose={this.handleChoose} />
                    <Field name="authorization_id" component={AuthorizationAutocomplete} authorizations={this.props.authorizations} source_name={this.state.source_name} />
                    <Field name="name" component={this.renderInput} label="Enter Name" />
                    <Field name="report" component={this.renderInput} label="Enter Report" />
                    <Field name="profile" component={this.renderInput} label="Enter Profile" />
                    <Field name="parser_name" component={ParserSelect} />
                    <Field name="store_name" component={StoreSelect} />
                    <Field name="is_model" component={ModelSelect} />
                    <Field name="location" component={this.renderInput} label="Enter Location" />
                    <Field name="load_mode" component={LoadSelect} />
                    <Field name="frequency" component={FrequencySelect} />
                    <Field name="hour" component={HourSelect} />
                    <Field name="day" component={DaySelect} />
                    <Field name="sql_script" component={this.renderInput} label="Enter SQL URI" />
                    <Button type="submit" variant="contained" size="large" color="primary">
                        Submit
                    </Button>
                </form>
            );
        }
    }
}

const validate = (formValues) => {
    const errors = {};
    if (!formValues.name) {
        errors.name = "You must enter a name"
    }
    
    if (!formValues.report) {
        errors.report = "You must enter a report"
    }

    return errors
};

const mapStateToProps = (state) => {
    return { 
        sources: Object.values(state.sources),
        authorizations: _.chain(state.sources)
            .keyBy('name')
            .mapValues('authorizations')
            .value()
    };
};

export default compose(
    connect(
        mapStateToProps,
        { fetchSources }
    ),
    reduxForm({ 
        form: 'flowForm',
        validate 
    }),
    withStyles(useStyles)
)(FlowForm);