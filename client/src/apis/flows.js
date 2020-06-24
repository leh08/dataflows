import axios from 'axios';

export default axios.create({
    baseURL: "https://dataflows-server.herokuapp.com"
});