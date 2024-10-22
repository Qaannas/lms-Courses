<template>
  <body>
    <!-- Header Area -->
    <header class="header-area header-sticky">
      <div class="container">
        <nav class="main-nav">
          <!-- Logo -->
          <a href="/" class="logo">
            <h1>Scholar</h1>
          </a>
          <!-- Search Bar -->
          <div class="search-input">
            <form id="search" action="#">
              <input
                type="text"
                placeholder="Search courses..."
                id="searchText"
                name="searchKeyword"
              />
              <i class="fa fa-search"></i>
            </form>
          </div>
          <!-- Navigation Menu -->

          <ul class="nav">
            <li>
              <span v-if="studentName" class="welcome-message"
                >Welcome, {{ studentName }}</span
              >
            </li>
            <li>
              <img
                class="avatar"
                src="/assets/images/boy.png"
                alt="Profile avatar"
              />
            </li>
            <li><button @click="logout" class="logout-btn">Logout</button></li>
          </ul>
        </nav>
      </div>
    </header>

    <!-- Course Section -->
    <section class="section courses" id="courses">
      <div class="container">
        <div class="section-heading text-center">
          <h6>Our Courses</h6>
          <h2>Explore Latest Courses</h2>
        </div>

        <!-- Filters -->
        <ul class="event_filter">
          <li><a href="#" class="is_active">Show All</a></li>
          <li><a href="#">Webdesign</a></li>
          <li><a href="#">Development</a></li>
          <li><a href="#">Wordpress</a></li>
        </ul>

        <!-- Course Grid -->
        <div class="course-grid">
          <div v-for="course in courses" :key="course.id" class="course-card">
            <div class="course-thumb">
              <img src="assets/images/cours.jpg" alt="Course Thumbnail" />
            </div>
            <div class="course-info">
              <h4>{{ course.name }}</h4>
              <p>{{ course.description }}</p>
              <span class="price"><strong>$450</strong></span>
              <button
                :disabled="isEnrolled(course.id)"
                @click="enrollInCourse(course.id)"
                class="enroll-btn"
              >
                Enroll
              </button>
              <p v-if="isEnrolled(course.id)" class="enrolled-text">
                Enrolled in this course
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </body>
</template>

<script>
export default {
  name: "ProfileS",
  data() {
    return {
      studentName: "",
      courses: [],
      enrolledCourses: [],
    };
  },
  mounted() {
    this.enrolledCourses =
      JSON.parse(localStorage.getItem("enrolledCourses")) || [];
    this.studentName = localStorage.getItem("studentName");
  },
  created() {
    this.fetchCourses();
    this.fetchEnrolledCourses();
  },
  methods: {
    logout() {
      localStorage.removeItem("studentName");
      localStorage.removeItem("studentId");
      this.$router.push("/");
    },
    async fetchCourses() {
      try {
        const response = await fetch("http://localhost:8000/api/courses/");
        if (response.ok) {
          this.courses = await response.json();
        } else {
          console.error("Failed to fetch courses");
        }
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    },
    async fetchEnrolledCourses() {
      try {
        const studentId = localStorage.getItem("studentId");
        const response = await fetch(
          `http://localhost:8000/api/enrolled-courses/${studentId}/`
        );
        if (response.ok) {
          this.enrolledCourses = await response.json();
        } else {
          console.error("Failed to fetch enrolled courses");
        }
      } catch (error) {
        console.error("Error fetching enrolled courses:", error);
      }
    },
    async enrollInCourse(courseId) {
      try {
        const studentId = localStorage.getItem("studentId");
        const enrolledCourses =
          JSON.parse(localStorage.getItem("enrolledCourses")) || [];

        if (enrolledCourses.includes(courseId)) {
          alert("You are already enrolled in this course.");
          return;
        }

        const response = await fetch("http://localhost:8000/api/enroll/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ studentId, courseId }),
        });

        if (response.ok) {
          enrolledCourses.push(courseId);
          localStorage.setItem(
            "enrolledCourses",
            JSON.stringify(enrolledCourses)
          );
          this.enrolledCourses = enrolledCourses;
          alert("Successfully enrolled in the course!");
        } else {
          const errorData = await response.json();
          console.error("Failed to enroll in course:", errorData);
          alert(errorData.error || "Enrollment failed.");
        }
      } catch (error) {
        console.error("Error enrolling in course:", error);
      }
    },
    isEnrolled(courseId) {
      const enrolledCourses =
        JSON.parse(localStorage.getItem("enrolledCourses")) || [];
      return enrolledCourses.includes(courseId);
    },
  },
};
</script>

<style scoped>
.avatar {
  width: 40px; /* Adjust size */
  height: 40px; /* Ensure it's square */
  border-radius: 50%; /* Makes it circular */
  padding: 2px;
  border: 2px solid #ccc; /* Adds a border around it */
  object-fit: cover; /* Ensures image covers the space without stretching */
}

/* General Layout and Styling */
body {
  margin: 0;
  font-family: "Poppins", sans-serif;
  background-color: #f4f4f9;
  overflow-x: hidden;
}

/* Header Styling */
.header-area {
  background-color: #7a6ad8;
  padding: 10px 0;
  color: white;
  position: sticky;
  top: 0;
  z-index: 100;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav {
  display: flex;
  align-items: center;
  list-style: none;
}

.nav li {
  margin-left: 20px;
}

.logo h1 {
  font-size: 24px;
  color: #fff;
  font-weight: bold;
}

.search-input input {
  padding: 10px;
  border-radius: 25px;
  border: none;
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

.logout-btn {
  background-color: #ff4b2b;
  border: none;
  padding: 5px 15px;
  color: white;
  border-radius: 25px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #ff1c1c;
}

/* Course Section Styling */
.section {
  margin-top: 40px;
}

.section-heading h6 {
  font-size: 14px;
  color: #7a6ad8;
  text-transform: uppercase;
  font-weight: 600;
}

.section-heading h2 {
  font-size: 36px;
  color: #1e1e1e;
  margin-top: 10px;
}

.event_filter {
  background-color: #f1f0fe;
  padding: 15px 30px;
  border-radius: 50px;
  text-align: center;
  list-style: none;
}

.event_filter li {
  display: inline-block;
  margin: 0 15px;
}

.event_filter li a {
  font-size: 14px;
  font-weight: 500;
  color: #1e1e1e;
  transition: all 0.3s ease;
}

.event_filter li a.is_active,
.event_filter li a:hover {
  color: #7a6ad8;
}

/* Course Card Layout */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.course-card {
  background-color: #fff;
  border-radius: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.course-card:hover {
  transform: scale(1.05);
}

.course-thumb img {
  width: 100%;
  border-bottom: 2px solid #7a6ad8;
}

.course-info {
  padding: 20px;
  text-align: center;
}

.course-info h4 {
  font-size: 20px;
  color: #1e1e1e;
  margin-bottom: 10px;
}

.course-info p {
  color: #4a4a4a;
  font-size: 14px;
  margin-bottom: 20px;
}

.price {
  font-size: 18px;
  font-weight: bold;
  color: #7a6ad8;
  margin-bottom: 15px;
}

.enroll-btn {
  background-color: #7a6ad8;
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  width: 100%;
}

.enroll-btn:disabled {
  background-color: #ccc;
}

.enrolled-text {
  margin-top: 10px;
  color: green;
  font-weight: bold;
}
</style>
