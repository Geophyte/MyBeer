import express from 'express';

import { getBeersBySearch, getBeers, createBeer, updateBeer, deleteBeer, likeBeer } from '../controllers/beers.js';
import auth from '../middleware/auth.js';

const router = express.Router();

router.get('/search', getBeersBySearch);
router.get('/', getBeers);
router.post('/', auth, createBeer);
router.patch('/:id', auth, updateBeer);
router.delete('/:id', auth, deleteBeer);
router.patch('/:id/likeBeer', auth, likeBeer);

export default router;