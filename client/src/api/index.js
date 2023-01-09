import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000' });

API.interceptors.request.use((req) => {
    // server must know if user is logged in
    if(localStorage.getItem('profile')) {
        req.headers.Authorization = `Bearer ${JSON.parse(localStorage.getItem('profile')).token}`;
    }

    return req;
});

export const fetchBeers = (page) => API.get(`/beers?page=${page}`);
export const fetchBeersBySearch = (searchQuery) => API.get(`/beers/search?searchQuery=${searchQuery.search || 'none'}&categories=${searchQuery.categories}`);
export const createBeer = (newBeer) => API.post('/beers', newBeer);
export const updateBeer = (id, updatedBeer) => API.patch(`${'/beers'}/${id}`, updatedBeer);
export const deleteBeer = (id) => API.delete(`${'/beers'}/${id}`);
export const likeBeer = (id) => API.patch(`${'/beers'}/${id}/likeBeer`);

export const createReview = (newReview) => API.post('/reviews', newReview);
export const getReviews = () => API.get('/reviews');

export const signIn = (formData) => API.post('/users/signin', formData);
export const signUp = (formData) => API.post('/users/signup', formData);