import mongoose from "mongoose";
import Beer from "../models/beer.js";

export const getBeers = async (req, res) => {
    const { page } = req.query;

    try {
        const LIMIT = 8;
        const startIndex = (Number(page) -1)*LIMIT; // startIndex of every page
        const total = await Beer.countDocuments({});

        const beers = await Beer.find().sort({ _id: -1 }).limit(LIMIT).skip(startIndex);

        res.status(200).json({ data: beers, currentPage: Number(page), numberOfPages: Math.ceil(total/LIMIT) });
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
}

export const getBeersBySearch = async (req, res) => {
    const { searchQuery, categories } = req.query

    try {
        const title = new RegExp(searchQuery, 'i'); // ignore size of letters (Test=TEST=TeST)

        const beers = await Beer.find({ $or: [ { title }, { categories:{ $in: categories.split(',')} }] });

        res.json({ data: beers });
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
}

export const createBeer = async (req, res) => {
    const beer = req.body;
    console.log(beer)

    const newBeer = new Beer({ ...beer, creator: req.userId, createdAt: new Date().toISOString() });
    try {
        await newBeer.save();

        res.status(201).json(newBeer);
    } catch (error) {
        res.status(409).json({message: error.message });
    }
}

export const updateBeer = async (req, res) => {
    const { id: _id } = req.params;
    const beer = req.body;

    if(!mongoose.Types.ObjectId.isValid(_id)) return res.status(404).send('No beer with that id');

    const updatedBeer = await Beer.findByIdAndUpdate(_id, { ...beer, _id }, { new: true });
    
    res.json(updatedBeer);
}

export const deleteBeer = async (req, res) => {
    const { id } = req.params;

    if(!mongoose.Types.ObjectId.isValid(id)) return res.status(404).send('No beer with that id');

    await Beer.findByIdAndDelete(id);

    res.json({ message: 'beer deleted successfully' });
}

export const likeBeer = async (req, res) => {
    const { id } = req.params;

    if(!req.userId) return res.json({ message: "Unauthenticated" });

    if(!mongoose.Types.ObjectId.isValid(id)) return res.status(404).send('No beer with that id');

    const beer = await Beer.findById(id);

    const index = beer.likes.findIndex((id) => id === String(req.userId));

    if(index === -1) {
        //like
        beer.likes.push(req.userId);
    } else {
        // alreadey liked, dislike
        beer.likes = beer.likes.filter((id) => !(id === String(req.userId)));
    }

    const updatedBeer = await Beer.findByIdAndUpdate(id, beer, { new: true });

    res.json(updatedBeer);
}