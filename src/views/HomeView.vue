<script setup>
import { ref } from "vue";
let message = ref("Drift Dater")

</script>

<template>
    <div class="container">
      <div class="text-center">
        <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        <h1>{{ message }}</h1>
        <p>Your one stop for a good match</p> <!--Optional: From hello to forever—start here.-->
      </div>
      <section>
        <div class="ft">
          <img src="/assets/Recommended.jpg" alt="Recommended match" class="WebDetails">
          <h2 class="subject">Get recommended your perfect match</h2>
          <p class="text">Our smart matching system learns your preferences, interests, and vibe to connect you 
            with people who feel naturally compatible. Spend less time searching and more time meeting 
            meaningful connections that just make sense.</p>
        </div>
        <div class="ft">
          <img src="/assets/Choose.jpg" alt="Recommended match" class="WebDetails">
          <h2 class="subject">Choose what feels right</h2>
          <p class="text">Make your choice with confidence using simple actions like: like, dislike, or pass. 
            Each swipe helps refine your preferences, allowing the app to better understand your type and 
            improve future match suggestions. It&#x2019;s an easy, intuitive way to stay in control while quickly 
            discovering people who truly fit your vibe.</p>
        </div>
        <div class="ft">
          <img src="/assets/Messaging.jpg" alt="Chat comfortably" class="WebDetails">
          <h2 class="subject">Smooth messaging</h2>
          <p class="text">Start conversations naturally and without pressure. Our chat experience is designed to 
            feel smooth, friendly, and effortless so you can focus on getting to know your match. 
            Whether it&#x2019;s a quick hello or a deep conversation, connecting has never been 
            simpler or more comfortable.</p>
        </div>
        <div class="ft">
          <img src="/assets/Search.jpg" alt="Search with filters" class="WebDetails">
          <h2 class="subject">Still not finding the one?</h2>
          <p class="text">Use our advanced search tools to refine your preferences and discover more compatible 
            matches. Filter by what matters most to you and take control of your dating experience 
            to find someone who truly fits your vibe.</p>
        </div>
        <div class="ft">
          <img src="/assets/RightOne.jpg" alt="Find your match" class="WebDetails">
          <h2 class="subject">Find the right one for you</h2>
          <p class="text">Find the right one for you with a dating experience designed around your preferences, 
            personality, and pace. From smart recommendations to easy conversations and advanced 
            search tools, everything is built to help you connect with people who truly match your 
            vibe. Your next meaningful connection is just a moment away.</p>
          </div>
      </section>
    </div>
</template>

<style scoped>
/*Area to showcase all the websites features*/ 
section{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background: #bfa6bf;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 15px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/*Individual feature styling*/
.ft{
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  grid-template-areas: 
  "image title"
  "image text";

  gap: 5px;
  background-color: #bfa6bf;
  padding: 5px;
}

.WebDetails{
  grid-area: image;
  width: 80px;
  height: 80px;
  border-radius: 10px;
  object-fit: cover;
}
.subject{
  grid-area: title;
}

.text{
  grid-area: text;
}
</style>