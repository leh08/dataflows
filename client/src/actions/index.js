import flows from '../apis/flows';
import history from '../history';
import { 
    AUTH_USER,
    AUTH_ERROR,
    CREATE_FLOW,
    FETCH_FLOWS,
    FETCH_FLOW,
    DELETE_FLOW,
    EDIT_FLOW,
} from './types';

export const signUp = (formProps) => async dispatch => {
    try {
        await flows.post('/signup', formProps);
        history.push("/flows");
    } catch (e) {
        dispatch({ type: AUTH_ERROR, payload: "Email in use" });
    }
};

export const logOut = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem('isSignedIn', false)

    return {
        type: AUTH_USER,
        payload: {
            accessToken: '',
            refreshToken: '',
            isSignedIn: false,
            userId: ''
        }
    };
};

export const logIn = (formProps) => async dispatch => {
    try {
        const response =  await flows.post('/login', formProps);
        const { access_token, refresh_token, user } = response.data

        dispatch({ type: AUTH_USER, payload: {
             accessToken: access_token,
             refreshToken: refresh_token,
             isSignedIn: true,
             userId: user.id
        } });
        
        localStorage.setItem('accessToken', access_token)
        localStorage.setItem('refreshToken', refresh_token)
        localStorage.setItem('isSignedIn', true)
        history.push("/flows");
    } catch (e) {
        dispatch({ type: AUTH_ERROR, payload: "Invalid login credentials" });
    }
};

export const createFlow = (formValues) => async (dispatch, getState) => {
    const { accessToken } = getState().auth;
    const response = await flows.post('/flows', { ...formValues }, { headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    } });
    console.log(response)
    dispatch({ type: CREATE_FLOW, payload: response.data });
    history.push("/flows");
};

export const fetchFlows = () => async (dispatch) => {
    const response = await flows.get('/flows');

    dispatch({ type: FETCH_FLOWS, payload: response.data });
};

export const fetchFlow = (id) => async (dispatch) => {
    const response = await flows.get(`/flows/${id}`);

    dispatch({ type: FETCH_FLOW, payload: response.data });
};

export const editFlow = (id, formValues) => async (dispatch) => {
    const response = await flows.patch(`/flows/${id}`, formValues);

    dispatch({ type: EDIT_FLOW, payload: response.data });
    history.push("/flows");
};

export const deleteFlow = (id) => async (dispatch) => {
    await flows.delete(`/flows/${id}`);

    dispatch({ type: DELETE_FLOW, payload: id });
    history.push("/flows");
};