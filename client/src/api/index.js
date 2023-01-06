import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000' });

API.interceptors.request.use((req) => {
    // server must know if user is logged in
    if(localStorage.getItem('profile')) {
        req.headers.Authorization = `Bearer ${JSON.parse(localStorage.getItem('profile')).token}`;
    }

    return req;
});

export const fetchBeers = (page) => API.get(`/posts?page=${page}`);
export const fetchBeersBySearch = (searchQuery) => API.get(`/posts/search?searchQuery=${searchQuery.search || 'none'}&tags=${searchQuery.tags}`);
export const createBeer = (newPost) => API.post('/posts', newPost);
export const updateBeer = (id, updatedPost) => API.patch(`${'/posts'}/${id}`, updatedPost);
export const deleteBeer = (id) => API.delete(`${'/posts'}/${id}`);
export const likeBeer = (id) => API.patch(`${'/posts'}/${id}/likePost`);

export const signIn = (formData) => API.post('/users/signin', formData);
export const signUp = (formData) => API.post('/users/signup', formData);