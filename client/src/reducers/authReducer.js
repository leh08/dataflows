import { SIGN_IN, SIGN_OUT, AUTH_USER, AUTH_ERROR } from '../actions/types';

const INITIAL_STATE = {
    accessToken: null,
    refreshToken: null,
    isSignedIn: null,
    userId: null,
    errorMessage: null
};

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        // case SIGN_IN:
        //     return { ...state, isSignedIn: true, userId: action.payload };

        // case SIGN_OUT:
        //     return { ...state, isSignedIn: false, userId: null };

        case AUTH_USER:
            return { ...state, ...action.payload }

        case AUTH_ERROR:
            return { ...state, errorMessage: action.payload };

        default:
            return state
    }
};