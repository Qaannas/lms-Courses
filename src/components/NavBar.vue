<template>
    <nav class="navbar">
      <div class="navbar-container">
        <h1 class="navbar-title">Course Enrollment</h1>
        <div class="navbar-right">
          <span v-if="studentName">Welcome, {{ studentName }}</span>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    data() {
      return {
        studentName: ''
      };
    },
    mounted() {
      // Retrieve the student's name from localStorage
      this.studentName = localStorage.getItem('studentName');
    },
    methods: {
      logout() {
        // Clear localStorage and redirect to home
        localStorage.removeItem('studentName');
        localStorage.removeItem('studentId'); // Clear student ID if necessary
        this.$router.push('/'); // Redirect to home page
      }
    }
  };
  </script>
  
  <style scoped>
  .navbar {
    background-color: #4CAF50; /* Green background */
    padding: 1rem;
    color: white;
  }
  
  .navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .navbar-title {
    font-size: 1.5rem;
  }
  
  .navbar-right {
    display: flex;
    align-items: center;
  }
  
  .logout-btn {
    padding: 0.5rem 1rem;
    background-color: #ff6b6b;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 1rem;
  }
  
  .logout-btn:hover {
    background-color: #ff4f4f;
  }
  </style>
  