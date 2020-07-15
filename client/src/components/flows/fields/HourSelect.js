import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
  formControl: {
        margin: theme.spacing(1.25),
        width: 450,
  },
}));

export default function SimpleSelect() {
    const classes = useStyles();
    const [hour, setHour] = React.useState("");

    const handleChange = (event) => {
        setHour(event.target.value);
    };

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Choose Hour</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={hour}
                onChange={handleChange}
            >
                <MenuItem value="">None</MenuItem>
                <MenuItem value={0}>00</MenuItem>
                <MenuItem value={1}>01</MenuItem>
                <MenuItem value={2}>02</MenuItem>
                <MenuItem value={3}>03</MenuItem>
                <MenuItem value={4}>04</MenuItem>
                <MenuItem value={5}>05</MenuItem>
                <MenuItem value={6}>06</MenuItem>
                <MenuItem value={7}>07</MenuItem>
                <MenuItem value={8}>08</MenuItem>
                <MenuItem value={9}>09</MenuItem>
                <MenuItem value={10}>10</MenuItem>
                <MenuItem value={11}>11</MenuItem>
                <MenuItem value={12}>12</MenuItem>
                <MenuItem value={13}>13</MenuItem>
                <MenuItem value={14}>14</MenuItem>
                <MenuItem value={15}>15</MenuItem>
                <MenuItem value={16}>16</MenuItem>
                <MenuItem value={17}>17</MenuItem>
                <MenuItem value={18}>18</MenuItem>
                <MenuItem value={19}>19</MenuItem>
                <MenuItem value={20}>20</MenuItem>
                <MenuItem value={21}>21</MenuItem>
                <MenuItem value={22}>22</MenuItem>
                <MenuItem value={23}>23</MenuItem>
            </Select>
        </FormControl>
    );
};
  