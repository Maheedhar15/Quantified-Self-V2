<template>
<body>
<div id="Home">
    <h1 class="header"> Welcome {{name}} </h1>
        <p></p>
  </div>    </body>  
</template>

<script>
import axios from 'axios';


export default {
Name: 'HomeView',
mounted() {
    axios.get('http://localhost:5000/')
    .then((resp ) => console.log(resp.data))
    .catch((err) => console.log(err.response))
},
data() {
    return {
        name: localStorage.name,
    }
},
};

</script>

<style scoped>

.header{    
    top: 0;
    padding: 0;
    margin: 0;
}

body{
    background-color: black;
}
#Home{
    margin-bottom: 250px;
    color: white;
    
}
</style>