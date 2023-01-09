import { FETCH_ALL, FETCH_BY_SEARCH, CREATE, UPDATE, DELETE, START_LOADING, END_LOADING, FETCH_REVIEWS } from '../constants/actionTypes';
import * as api from '../api';


export const createReview = (review) => async (dispatch) => {
    try {
        /* dispatch({ type: START_LOADING }); */
        const { data } = await api.createReview(review);
        return (data);
        //dispatch({ type: CREATE, payload: data });
        /* dispatch({ type: END_LOADING }); */
    } catch (error) {
        console.log(error);
    }
}

export const getReviews = () => async (dispatch) => {
    try {
        dispatch({ type: START_LOADING });
        const { data } = await api.getReviews();

        dispatch({ type: FETCH_REVIEWS, payload: data });
        dispatch({ type: END_LOADING });
        return data
    } catch (error) {
        console.log(error.message);
    }
}