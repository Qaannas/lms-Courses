<template>
<body >
	
	<header class="header-area header-sticky">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <nav class="main-nav">
                    <!-- ***** Logo Start ***** -->
                    <a href="index.html" class="logo">
                        <h1>Scholar</h1>
                    </a>
                    <!-- ***** Logo End ***** -->
                    <!-- ***** Serach Start ***** -->
                    <div class="search-input">
                      <form id="search" action="#">
                        <input class="search"  type="text" placeholder="Type Something" id='searchText' name="searchKeyword" onkeypress="handle" />
                        <i class="fa fa-search"></i>
                      </form>
                    </div>
                    <!-- ***** Serach Start ***** -->
                    <!-- ***** Menu Start ***** -->
                    <ul class="nav">
                      <li class="scroll-to-section"><a href="/" class="active">Home</a></li>
                      
                      <li><a href="#contact" @click.prevent="redirectToSignup">Register Now!</a></li>
                  </ul>   
                    <a class='menu-trigger'>
                        <span>Menu</span>
                    </a>
                    <!-- ***** Menu End ***** -->
                </nav>
            </div>
        </div>
    </div>
  </header>
<div class="main">
	<input type="checkbox" id="chk" aria-hidden="true" />

	<div class="signup">
	<form @submit.prevent="register">
		<label for="chk" aria-hidden="true">Sign up</label>
		<input v-model="form.name" type="text" name="txt" placeholder="Name" required />
		<input v-model="form.email" type="email" id="email" placeholder="Email" required />
		<input v-model="form.password" type="password" id="password" placeholder="Password" required />
		<input v-model="form.password2" type="password" placeholder="Repeat Password" required />
		<button type="submit">Sign up</button>
	</form>
	<p v-if="error">{{ error }}</p>
	<p v-if="success">{{ success }}</p>
	</div>

	<div class="login">
	<form @submit.prevent="login">
		<label for="chk" aria-hidden="true">Login</label>
		<input v-model="form.name" id="name" type="text" placeholder="Name" required />
		<input v-model="form.password" type="password" placeholder="Password" required />
		<button type="submit">Login</button>
	</form>
	<p v-if="error" class="error">{{ error }}</p>
	</div>
</div>
</body>	
</template>
  
 
<script>
export default {
	name: "SignUp",

data() {
	return {
	form: {
		name: '',
		email: '',
		password: '',
		password2: '',
	},
	error: '',
	success: '',
	};
},
methods: {
	async register() {
  if (this.form.password !== this.form.password2) {
    this.error = "Passwords don't match";
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(this.form),
    });

    if (response.ok) {
      this.success = 'Registration successful';
      this.error = '';
    } else {
      const data = await response.json();
      this.error = data.error || 'Registration failed';
    }
  } catch (error) {
    this.error = 'Error: ' + error;
  }
},
async login() {
  this.error = '';
  this.success = '';

  try {
    const response = await fetch('http://localhost:8000/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: this.form.name,
        password: this.form.password,
      }),
    });

    const data = await response.json();
    console.log('Login API Response:', data);

    if (response.ok) {
      localStorage.setItem('studentName', data.name);
      localStorage.setItem('studentId', data.studentId); // Store the studentId
      localStorage.setItem('token', data.token); // Store the authentication token
      localStorage.setItem('enrolledCourses', JSON.stringify(data.enrolledCourses));
      this.$router.push({ name: 'ProfileS' });
    } else {
      this.error = data.error || 'Login failed.';
    }
  } catch (err) {
    console.error('Login Request Failed:', err);
    this.error = 'Error logging in. Please try again.';
  }
}

},
}
</script>
  




<style scoped>

.search{
	margin-top: -1px;

}
body{
	margin: 0;
	padding: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	min-height: 100vh;
	font-family: 'Jost', sans-serif;
	background: #7a6ad8;
	
}
.main{
	width: 350px;
	height: 500px;
	background: red;
	overflow: hidden;
	background: url("https://doc-08-2c-docs.googleusercontent.com/docs/securesc/68c90smiglihng9534mvqmq1946dmis5/fo0picsp1nhiucmc0l25s29respgpr4j/1631524275000/03522360960922298374/03522360960922298374/1Sx0jhdpEpnNIydS4rnN4kHSJtU1EyWka?e=view&authuser=0&nonce=gcrocepgbb17m&user=03522360960922298374&hash=tfhgbs86ka6divo3llbvp93mg4csvb38") no-repeat center/ cover;
	border-radius: 10px;
	box-shadow: 5px 20px 50px #000;
}
#chk{
	display: none;
}
.signup{
	position: relative;
	width:100%;
	height: 100%;
}

label{
	color: #eee;
	font-size: 2.3em;
	justify-content: center;
	display: flex;
	margin: 50px;
	font-weight: bold;
	cursor: pointer;
	transition: .5s ease-in-out;
}
input{
	width: 60%;
	height: 25px;
	background: #e0dede;
	justify-content: center;
	display: flex;
	margin: 20px auto;
	padding: 12px;
	border: none;
	outline: none;
	border-radius: 5px;
}
button{
	width: 60%;
	height: 40px;
	margin: 10px auto;
	justify-content: center;
	display: block;
	color: #fff;
	background: #573b8a;
	font-size: 1em;
	font-weight: bold;
	margin-top: 30px;
	outline: none;
	border: none;
	border-radius: 5px;
	transition: .2s ease-in;
	cursor: pointer;
}
button:hover{
	background: #7a6ad8;
}
.login{
	height: 460px;
	background: #eee;
	border-radius: 60% / 10%;
	transform: translateY(-180px);
	transition: .8s ease-in-out;
}
.login label{
	color: #7a6ad8;
	transform: scale(.6);
}

#chk:checked ~ .login{
	transform: translateY(-500px);
}
#chk:checked ~ .login label{
	transform: scale(1);	
}
#chk:checked ~ .signup label{
	transform: scale(.6);
}


</style>