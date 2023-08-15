import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
 
// Initialize Firebase
const app = initializeApp ({
       apiKey: "AIzaSyBycwJKZ1iKNQeVBZdl40cosXZ8FQNkAg8",
    authDomain: "cipher-media-e414c.firebaseapp.com",
    projectId: "cipher-media-e414c",
    storageBucket: "cipher-media-e414c.appspot.com",
    messagingSenderId: "737707024550",
    appId: "1:737707024550:web:ab37d3e1c03dec51005467"
});
 
// Firebase storage reference
const storage = getStorage(app);
export default storage;