import React from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

export default function ComboBox({ sources, handleChoose }) {
    return (
        <Autocomplete
            id="source_name"
            options={sources}
            getOptionLabel={(option) => option.name}
            renderInput={(params) => {
                handleChoose(params.inputProps.value)
                return <TextField {...params} label="Enter Source" />
            }}
        />
    );
}