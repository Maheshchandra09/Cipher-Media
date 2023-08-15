import React , { useState,useEffect } from 'react';
import './App.css';
import storage from "./firebaseConfig.js"
import {ref,uploadBytesResumable 
  } from "firebase/storage";
function App() {
  const [selectedFile,setSelectedFile]=useState();
  const [isFilePicked,setIsFilePicked] = useState(false);
  const[message,setMessage]=useState(' ');
  const[output,setOutput]=useState(' ');

  const msghandler= event =>{
    setMessage(event.target.value);
    console.log(event.target.value);
  }


  const changeHandler = (event)=>{
    setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  }
    const encrypt =()=>{
      setOutput(" ");
      try{
      const val=fetch(`http://localhost:5000/encrypt?msg=${message}&img=${selectedFile.name}`,{
        mode: 'no-cors',
      })
      console.log(val)
      setOutput("successfully encrypted")
      }
      catch(error){
        console.log(error)
        setOutput("failed encrypting");
      }
    }
//     uploadTask.on(
//         "state_changed",
//         (snapshot) => {
//             const percent = Math.round(
//                 (snapshot.bytesTransferred / snapshot.totalBytes) * 100
//             );
//  
//             // update progress
//             setPercent(percent);
//         },
//         (err) => console.log(err),
//         () => {
//           // download url
//             getDownloadURL(uploadTask.snapshot.ref).then((url) => {
//                 console.log(url);
//             });
//         }
//     ); 
  const handlesubmission=()=>{
    const storageRef = ref(storage, '/'+selectedFile.name)
    const uploadTask = uploadBytesResumable(storageRef, selectedFile);
  }
  return (
    <div className='App'>
      <div className="Head">
        <h1>Welcome to Cipher Application</h1>
        <div className="Info">
        <p>Encrypt and encode your data safely into your pictures to give it best protection</p>
        </div>
      </div>
      <div className='select'>
          <input type="file" name="file" onChange={changeHandler}></input>
          {isFilePicked ? (
            <div>
                <p>Selected Image is {selectedFile.name}</p>
                <p>Filetype is {selectedFile.type}</p>
                <p>Size of image {selectedFile.size}B</p>
              </div>
          )
          : (
            <div>
              <p></p>
            </div>
          )
          }
          <div>
            <button className='file' onClick={handlesubmission}>Upload file</button>
          </div>
          </div>
          <div className='msg'>
              <input type='text' onChange={msghandler} className='text' placeholder='Enter the message to be protected' ></input>
          <button onClick={encrypt}> Encode the message into your file </button>
          <p>{output}</p>
          </div>
        </div>
  );
}

export default App;
