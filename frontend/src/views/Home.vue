<template>
  <div class="home">
    <particles />
    <div class="login-form">
      <form @submit.prevent>
        <div class="avatar">
          <img src="../assets/logo.png" alt="Avatar" />
        </div>
        <h2 v-if="login_form" class="text-center">Member Login</h2>
        <h2 v-else class="text-center">Create Account</h2>
        <div v-if="errors.length != 0" class="warning">
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </div>
        <div class="form-group">
          <input
            v-model="user.email"
            type="email"
            class="form-control"
            name="email"
            placeholder="Email"
            required="required"
          />
        </div>
        <div v-if="!login_form" class="form-group">
          <input
            v-model="user.name"
            type="text"
            class="form-control"
            name="username"
            placeholder="Username"
            required="required"
          />
        </div>
        <div class="form-group">
          <input
            v-model="user.password"
            type="password"
            class="form-control"
            name="password"
            placeholder="Password"
            required="required"
          />
        </div>
        <div v-if="!login_form" class="form-group">
          <input
            v-model="user.password_2"
            type="password"
            class="form-control"
            name="password"
            placeholder="Re-enter Password"
            required="required"
          />
        </div>
        <div class="form-group">
          <button
            @click="
              if (login_form) login();
              else signup();
            "
            type="submit"
            class="btn btn-primary btn-lg btn-block"
          >
            <div v-if="!login_form">Sign in</div>
            <div v-else>Log In</div>
          </button>
        </div>
        <div class="bottom-action clearfix">
          <p v-if="login_form" class="text-center link">
            Don't have an account?
            <a @click="toggle()">Sign up here!</a>
          </p>
          <p v-else class="text-center link">
            Already have an account?
            <a @click="toggle()">Log in here!</a>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import Particles from "../components/Particles.vue";

export default {
  name: "Home",
  components: {
    Particles,
  },
  data() {
    return {
      login_form: true,
      msg: "",
      user: { email: "", name: "", password: "", password_2: "" },
      errors: [],
    };
  },
  methods: {
    toggle() {
      this.login_form = !this.login_form;
    },
    inputIsCorrect() {
      this.errors = [];
      if (
        !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(
          this.user.email
        )
      ) {
        this.errors.push("Email is not valid");
      }
      if (
        !/^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/.test(
          this.user.password
        )
      ) {
        this.errors.push(
          "Password must be at least 8 characters long and must contain at least one capital letter and a special character."
        );
      }
      if (
        this.login_form == false &&
        this.user.password != this.user.password_2
      ) {
        this.errors.push("Passwords do not match");
      }
      return this.errors.length == 0;
    },

    login() {
      if (!this.inputIsCorrect()) {
        return 0;
      }

      console.log("login!!", {
          email: this.user.email,
          name: this.user.name,
          password: this.user.password,
        });

  
      this.$axios
        .post("http://127.0.0.1:5000/login",
        {
          email: this.user.email,
          name: this.user.name,
          password: this.user.password,
        }
        )
        .then((res) => {
          this.msg = res.data;
          console.log(res.data)
          this.$store.setToken(res.data);
          this.$axios.defaults.headers.common["Authorization"] =
            "token " + res.data.token;

          this.$store.user = res.data.user;
          this.$store.state = res.data.state;
          this.$router.push("upload");
        })
        .catch(() => this.errors.push("Login was unsuccessful")); //wrong credentials
    },


    signup() {
      if (!this.inputIsCorrect()) {
        return 0;
      }

      console.log("signup!!");
      this.$axios
        .post("http://127.0.0.1:5000/signin", {
          email: this.user.email,
          name: this.user.name,
          password: this.user.password,
          password_2: this.user.password_2,
        })
        .then((res) => {
          this.msg = res.data;
          this.$store.setToken(res.data.token);
          this.$axios.defaults.headers.common["Authorization"] =
            "token " + res.data.token;

          this.$store.user = this.user.name;
          this.$router.push("upload");
        })
        .catch(() => (this.error = "Username already exists")); 
    },
  },
};
</script>

<style scoped>
.home {
  color: #fff;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-content: center;
}
.form-control {
  min-height: 41px;
  background: #fff;
  box-shadow: none !important;
  border-color: #e3e3e3;
}
.form-control:focus {
  border-color: var(--secondary-bg-color);
}
.form-control,
.btn {
  border-radius: 10px;
}
.login-form {
  width: 350px;
  margin: auto;
}
.login-form form {
  color: #7a7a7a;
  border-radius: 10px;
  margin-bottom: 15px;
  font-size: 13px;
  background: var(--space-bg-color);
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  padding: 30px;
  position: relative;
}
.login-form h2 {
  font-size: 22px;
  margin: 35px 0 25px;
  height: 100%;
}
.login-form .avatar {
  position: absolute;
  margin: 0 auto;
  left: 0;
  right: 0;
  top: -50px;
  width: 95px;
  height: 95px;
  border-radius: 50%;
  z-index: 9;
  background: var(--secondary-bg-color);
  padding: 15px;
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.1);
}
.login-form .avatar img {
  width: 100%;
}
.login-form input[type="checkbox"] {
  position: relative;
}
.login-form .btn,
.login-form .btn:active {
  font-size: 16px;
  font-weight: bold;
  background: var(--secondary-bg-color) !important;
  border: none;
  margin-bottom: 20px;
}
.login-form .btn:hover,
.login-form .btn:focus {
  background: var(--main-bg-color) !important;
}
.login-form a {
  color: green;
  cursor: pointer;
  text-decoration: underline;
}
.login-form a:hover {
  text-decoration: none;
}
.login-form form a {
  color: var(--main-bg-color);
  text-decoration: none;
}
.login-form form a:hover {
  text-decoration: underline;
}
.login-form .bottom-action {
  font-size: 14px;
  height: 100%;
}
.warning {
  font-size: 14px;
  text-align: left;
  background-color: lightsalmon;
  padding: 3px;
  margin: 10px auto;
  border-radius: 10px;
  color: darkslategray;
  border: 1px solid #dd4343;
}
li {
  margin-left: 10px;
}
</style>