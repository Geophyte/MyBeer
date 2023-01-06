import mongoose from "mongoose";
import PostMessage from "../models/postMessage.js";

export const getBeers = async (req, res) => {
    const { page } = req.query;

    try {
        const LIMIT = 8;
        const startIndex = (Number(page) -1)*LIMIT; // startIndex of every page
        const total = await PostMessage.countDocuments({});

        const posts = await PostMessage.find().sort({ _id: -1 }).limit(LIMIT).skip(startIndex);

        res.status(200).json({ data: posts, currentPage: Number(page), numberOfPages: Math.ceil(total/LIMIT) });
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
}

export const getBeersBySearch = async (req, res) => {
    const { searchQuery, tags } = req.query

    try {
        const title = new RegExp(searchQuery, 'i'); // ignore size of letters (Test=TEST=TeST)

        const posts = await PostMessage.find({ $or: [ { title }, { tags:{ $in: tags.split(',')} }] });

        res.json({ data: posts });
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
}

export const createBeer = async (req, res) => {
    const post = req.body;

    const newPost = new PostMessage({ ...post, creator: req.userId, createdAt: new Date().toISOString() });
    try {
        await newPost.save();

        res.status(201).json(newPost);
    } catch (error) {
        res.status(409).json({message: error.message });
    }
}

export const updateBeer = async (req, res) => {
    const { id: _id } = req.params;
    const post = req.body;

    if(!mongoose.Types.ObjectId.isValid(_id)) return res.status(404).send('No post with that id');

    const updatedPost = await PostMessage.findByIdAndUpdate(_id, { ...post, _id }, { new: true });
    
    res.json(updatedPost);
}

export const deleteBeer = async (req, res) => {
    const { id } = req.params;

    if(!mongoose.Types.ObjectId.isValid(id)) return res.status(404).send('No post with that id');

    await PostMessage.findByIdAndDelete(id);

    res.json({ message: 'Post deleted successfully' });
}

export const likeBeer = async (req, res) => {
    const { id } = req.params;

    if(!req.userId) return res.json({ message: "Unauthenticated" });

    if(!mongoose.Types.ObjectId.isValid(id)) return res.status(404).send('No post with that id');

    const post = await PostMessage.findById(id);

    const index = post.likes.findIndex((id) => id === String(req.userId));

    if(index === -1) {
        //like
        post.likes.push(req.userId);
    } else {
        // alreadey liked, dislike
        post.likes = post.likes.filter((id) => !(id === String(req.userId)));
    }

    const updatedPost = await PostMessage.findByIdAndUpdate(id, post, { new: true });

    res.json(updatedPost);
}