import React from 'react';
import { Field, reduxForm } from 'redux-form';


class FlowForm extends React.Component {
    renderError({ error, touched }) {
        if (touched && error) {
            return (
                <div className="ui error message">
                    <div className="header">{error}</div>
                </div>
            );
        }
    }

    renderInput = ({ input, label, meta }) => {
        const className = `field ${meta.error && meta.touched ? 'error': ''}`
        return (
            <div className={className}>
                <label>{label}</label>
                <input {...input} autoComplete="off"/>
                {this.renderError(meta)}
            </div>
        );
    }

    onSubmit = (formValues) => {
        this.props.onSubmit(formValues);
    }

    render() {
        return (
            <form onSubmit={this.props.handleSubmit(this.onSubmit)} className="ui form error">
                <Field name="name" component={this.renderInput} label="Enter Name" />
                <Field name="report" component={this.renderInput} label="Enter Report" />
                <Field name="profile" component={this.renderInput} label="Enter Profile" />
                <Field name="parser_name" component={this.renderInput} label="Enter Parser" />
                <Field name="store_name" component={this.renderInput} label="Enter Store" />
                <Field name="is_model" component={this.renderInput} label="Enter Model" />
                <Field name="schema" component={this.renderInput} label="Enter Schema" />
                <Field name="load_mode" component={this.renderInput} label="Enter Load Mode" />
                <Field name="frequency" component={this.renderInput} label="Enter Frequency" />
                <Field name="day_unit" component={this.renderInput} label="Enter Day" />
                <Field name="time_unit" component={this.renderInput} label="Enter Time" />
                <Field name="sql_script" component={this.renderInput} label="Enter SQL URI" />
                <Field name="source_id" component={this.renderInput} label="Enter Source" />
                <Field name="authorization_id" component={this.renderInput} label="Enter Authorization" />
                <button className="ui button primary">Submit</button>
            </form>
        );
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

export default reduxForm({
    form: 'flowForm',
    validate
})(FlowForm);