import jwt from 'jsonwebtoken';

const auth = async (req, res, next) => {
    try {
        const token = req.headers.authorization.split(' ')[1];
        const isCustomAuth = token.length < 500; // check if its not from googleAuth

        let decodedData;
        
        if(token && isCustomAuth) {
            decodedData = jwt.verify(token, 'test') // test=secret

            req.userId = decodedData?.id;
        } else { // case of GoogleAuth
            decodedData = jwt.decode(token);

            req.userId = decodedData?.sub;
        }

        next();
    } catch (error) {
        console.log(error);
    }
}

export default auth;