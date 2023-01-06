import { FETCH_ALL, FETCH_BY_SEARCH, CREATE, UPDATE, DELETE, START_LOADING, END_LOADING } from '../constants/actionTypes';
import * as api from '../api';

//Action Creators
export const getBeers = (page) => async (dispatch) => {
    try {
        dispatch({ type: START_LOADING });
        const { data } = await api.fetchBeers(page);

        dispatch({ type: FETCH_ALL, payload: data });
        dispatch({ type: END_LOADING });
    } catch (error) {
        console.log(error.message);
    }
}

export const getBeersBySearch = (searchQuery) => async (dispatch) => {
    try {
        dispatch({ type: START_LOADING });
        const { data: { data } } = await api.fetchBeersBySearch(searchQuery);

        dispatch({ type: FETCH_BY_SEARCH, payload: data });
        dispatch({ type: END_LOADING });
    } catch (error) {
        console.log(error.message);
    }
}

export const createBeer = (beer) => async (dispatch) => {
    try {
        dispatch({ type: START_LOADING });
        const { data } = await api.createBeer(beer);
        dispatch({ type: CREATE, payload: data });
        dispatch({ type: END_LOADING });
    } catch (error) {
        console.log(error);
    }
}

export const updateBeer = (id, beer) => async (dispatch) => {
    try {
        const { data } = await api.updateBeer(id, beer);

        dispatch({ type: UPDATE, payload: data });
    } catch (error) {
        console.log(error);
    }
}

export const deleteBeer = (id) => async (dispatch) => {
    try {
        await api.deleteBeer(id);

        dispatch({ type: DELETE, payload: id });
    } catch (error) {
        console.log(error);
    }
}

export const likeBeer = (id) => async (dispatch) => {
    try {
        const { data } = await api.likeBeer(id);

        dispatch({ type: UPDATE, payload: data });
    } catch (error) {
        console.log(error)
    }
}