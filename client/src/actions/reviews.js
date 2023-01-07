import { FETCH_ALL, FETCH_BY_SEARCH, CREATE, UPDATE, DELETE, START_LOADING, END_LOADING } from '../constants/actionTypes';
import * as api from '../api';


export const createReview = (review) => async (dispatch) => {
    try {
        /* dispatch({ type: START_LOADING }); */
        const { data } = await api.createReview(review);
        dispatch({ type: CREATE, payload: data });
        /* dispatch({ type: END_LOADING }); */
    } catch (error) {
        console.log(error);
    }
}