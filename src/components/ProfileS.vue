<template>
  <body>
    <header class="header-area header-sticky">
      <div class="container">
        <nav class="main-nav">
          <a href="/" class="logo">
            <h1>Scholar</h1>
          </a>
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
          <ul class="nav">
            <li>
              <span v-if="studentName" class="welcome-message">
                Welcome, {{ studentName }}
              </span>
            </li>
            <li>
              <img
                class="avatar"
                src="/assets/images/boy.png"
                alt="Profile avatar"
              />
            </li>
            <li>
              <button @click="logout" class="logout-btn">Logout</button>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <section class="section courses" id="courses">
      <div class="container">
        <div class="section-heading text-center">
          <h6>Our Courses</h6>
          <h2>Explore Latest Courses</h2>
        </div>

        <ul class="event_filter">
          <li><a href="#" class="is_active">Show All</a></li>
          <li><a href="#">Webdesign</a></li>
          <li><a href="#">Development</a></li>
          <li><a href="#">Wordpress</a></li>
        </ul>
        <div class="rating_filter">
  <ul class="rating_filter_list">
    <li>
      <label for="ratingSelect" class="rating-label">Filter by Rating:</label>
    </li>
    <li>
      <select id="ratingSelect" @change="filterByRating($event.target.value)" class="rating-select">
        <option value="" selected>All Ratings</option>
        <option value="1">1 Star</option>
        <option value="2">2 Stars</option>
        <option value="3">3 Stars</option>
        <option value="4">4 Stars</option>
        <option value="5">5 Stars</option>
      </select>
    </li>
  </ul>
</div>



        <div class="course-grid">
          <div v-for="course in filteredCourses" :key="course.id" class="course-card">
            
            <div class="course-thumb">
              <img src="assets/images/cours.jpg" alt="Course Thumbnail" />
            </div>
            <div class="course-info">
              <h4>{{ course.name }}</h4>
              <p>{{ course.description }}</p>
              <span class="price"><strong>${{ course.price }}</strong></span>
              
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
              <div class="course-info" v-if="isEnrolled(course.id)">
                <label for="rating">Rate the course:</label>
                <div class="stars">
                  <span
                    v-for="n in 5"
                    :key="n"
                    class="star"
                    :class="{ selected: courseRatings[course.id] >= n }"
                    @click="setRating(course.id, n)"
                  >
                    ★
                  </span>
                </div>
                <p
                 v-if="ratingSubmitted[course.id]"
                  class="confirmation-text"
                >
                  Rating submitted successfully!
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </body>
</template>

<script>
import { ref, onMounted ,computed} from 'vue';

export default {
  name: "ProfileS",
  setup() {
    const studentName = ref("");
    const studentId = ref("");
    const courses = ref([]);
    const enrolledCourses = ref([]);
    const courseRatings = ref({});
    const ratingSubmitted = ref({});
    const selectedRating = ref(null); // Track selected rating filter


    onMounted(() => {
      studentName.value = localStorage.getItem("studentName");
      studentId.value = localStorage.getItem("studentId");
      fetchCourses();
      loadEnrolledCoursesFromLocalStorage();
      loadCourseRatingsFromLocalStorage(); // Load ratings from local storage
      
    });

    const fetchCourses = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/courses/");
        if (response.ok) {
          courses.value = await response.json();
        } else {
          console.error("Failed to fetch courses");
        }
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };
    const filteredCourses = computed(() => {
      if (selectedRating.value === null) {
        return courses.value; // Return all courses if no filter is selected
      }
      return courses.value.filter(course => courseRatings.value[course.id] === selectedRating.value);
      });

    // Function to set the selected rating filter
    const filterByRating = (rating) => {
  selectedRating.value = rating ? Number(rating) : null; // Convert to number or set to null
};

        const loadEnrolledCoursesFromLocalStorage = () => {
      const enrolled = JSON.parse(localStorage.getItem("enrolledCourses")) || [];
      enrolledCourses.value = enrolled; // Initialize from local storage
    };


    const loadCourseRatingsFromLocalStorage = () => {
      const ratings = JSON.parse(localStorage.getItem("courseRatings")) || {};
      courseRatings.value = ratings; // Load ratings from local storage
    };
   

    const enrollInCourse = async (courseId) => {
  if (isEnrolled(courseId)) {
    alert("You are already enrolled in this course.");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/api/enroll/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ studentId: studentId.value, courseId }),
    });

    if (response.ok) {
      enrolledCourses.value.push(courseId); // Update the reactive array
      localStorage.setItem("enrolledCourses", JSON.stringify(enrolledCourses.value)); // Update local storage
      courseRatings.value[courseId] = null; // Initialize rating
      alert("Successfully enrolled in the course!");
    } else {
      const errorData = await response.json();
      console.error("Failed to enroll in course:", errorData);
      alert(errorData.error || "Enrollment failed.");
    }
  } catch (error) {
    console.error("Error enrolling in course:", error);
  }
};



    const isEnrolled = (courseId) => {
      return enrolledCourses.value.includes(courseId);    };

    const logout = () => {
      localStorage.removeItem("studentName");
      localStorage.removeItem("studentId");
      //localStorage.removeItem("enrolledCourses"); // Optionally clear enrolled courses
      //localStorage.removeItem("courseRatings"); // Optionally clear ratings
      window.location.href = "/"; // Redirect to homepage
    };

    const submitRating = async (courseId) => {
      const rating = courseRatings.value[courseId];

      try {
        const response = await fetch(`http://localhost:8000/api/enroll/${studentId.value}/${courseId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ rating: rating }),
        });

        const data = await response.json();
        if (data.success) {
          ratingSubmitted.value[courseId] = true; // Set submission status for this course
          // Save the rating in local storage
          localStorage.setItem("courseRatings", JSON.stringify(courseRatings.value)); 
          console.log('Rating submitted successfully!');
        } else {
          console.error('Failed to submit rating:', data.message);
        }
      } catch (error) {
        console.error('Error submitting rating:', error);
      }
    };

    const setRating = (courseId, rating) => {
      courseRatings.value[courseId] = rating; // Update the rating in local data
      ratingSubmitted.value[courseId] = false; // Reset the flag before submitting
      submitRating(courseId); // Automatically submit the rating after setting it
    };

    return {
      studentName,
      studentId,
      courses,
      enrolledCourses,
      courseRatings,
      ratingSubmitted,
      enrollInCourse,
      isEnrolled,
      logout,
      setRating,
      filteredCourses,
      filterByRating,
    };
  }
};
</script>





<style scoped>


.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  padding: 2px;
  border: 2px solid #ccc;
  object-fit: cover;
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
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin: 40px 0;
  width: 100%;
  padding: 0;
}

.course-card {
  background-color: #fff;
  border-radius: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.course-thumb {
  position: relative;
  padding-top: 56.25%; /* 16:9 aspect ratio */
  overflow: hidden;
}

.course-thumb img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-bottom: 2px solid #7a6ad8;
}

.course-info {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.course-info h4 {
  font-size: 20px;
  color: #1e1e1e;
  margin: 0 0 10px 0;
}

.course-info p {
  color: #4a4a4a;
  font-size: 14px;
  margin: 0 0 20px 0;
  flex-grow: 1;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .course-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .course-grid {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
  }
  
  .container {
    padding: 0 16px;
  }
}

@media (max-width: 480px) {
  .course-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

/* Filter sections alignment */
.event_filter,
.rating_filter {
  margin: 20px auto;
  max-width: 100%;
  padding: 15px 20px;
}

.rating_filter_list {
  padding: 0;
  margin: 0;
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

.course-info select {
  margin-right: 10px;
}
.stars {
  cursor: pointer;
}

.star {
  font-size: 24px;
  color: gray;
}

.star.selected {
  color: gold;
}

.confirmation-text {
  color: green;
  font-weight: bold;
}

.rating_filter {
  background-color: #f1f0fe;
  padding: 15px 30px;
  border-radius: 50px;
  text-align: center;
  margin: 20px 0;
}

.rating_filter_list {
  display: flex;
  justify-content: center;
  align-items: center;
  list-style: none;
}

.rating_filter_list li {
  margin: 0 15px;
}

.rating-label {
  font-size: 14px;
  font-weight: 500;
  color: #1e1e1e;
}

.rating-select {
  padding: 10px;
  border-radius: 25px;
  border: 1px solid #ccc;
  background-color: #fff; /* Light background for contrast */
  font-size: 14px;
  color: #1e1e1e;
  cursor: pointer;
  transition: border 0.3s ease;
}

.rating-select:hover {
  border-color: #7a6ad8; /* Change border color on hover */
}

.rating-select:focus {
  outline: none;
  border-color: #7a6ad8; /* Highlight on focus */
}

</style>
