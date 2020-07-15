import React from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

export default function ComboBox({ authorizations, source_name }) {
    if (source_name) {
        const authorization = authorizations[source_name];
        
        return (
            <Autocomplete
                id="authorization_id"
                options={authorization}
                getOptionLabel={(option) => option.name}
                renderInput={(params) => {
                    return <TextField {...params} label="Enter Authorization" />
                }}
            />
        );
    } else {
        return <TextField disabled value="" label="Enter Authorization" />
    }
}