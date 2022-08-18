import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

/*
* function to all tweets 
* Input : empty tweet container
* output : return all the tweets using ajax response
*/
function loadTweets(callback)
{
    // Ajax Request
    const xhr = new XMLHttpRequest()
    const method = "GET"
    const url = "http://127.0.0.1:8000/api/tweets/"
    const responseType = "json"
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With","XMLHttpRequest")
    xhr.onload = function() {
        callback(xhr.response, xhr.status)
    }
    xhr.onerror = function(e)  {
      callback({"message": "there is an error"}, 400)
    }
    xhr.send()
}

function App() {
  const [tweets, setTweets] = useState([])

  useEffect(()=>{
    const myCallback = (response, status) => {
        if(status === 200){
          setTweets(response)
        } else{
          alert("There is an error")
        } 
    }
    loadTweets(myCallback)
  },[])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {tweets.map((tweet, index) =>{
            return <li>{tweet.content}</li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
