import axios from "axios";

let jwl = localStorage.getItem('jwl');

var headers = {
  "Content-type": "application/json",
}

if (jwl) headers['x-access-token'] = jwl;

export default axios.create({
  headers: headers 
});