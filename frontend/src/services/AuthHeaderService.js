export default function authHeader() {
    let jwl = localStorage.getItem('jwl');
  
    if (jwl) {
      return { };
    } else {
      return {};
    }
  }