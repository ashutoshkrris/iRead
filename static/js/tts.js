// Initialize new SpeechSynthesisUtterance object
let speech = new SpeechSynthesisUtterance();

// Set Speech Language
speech.lang = "en";

// Get List of Voices
let voices = window.speechSynthesis.getVoices(); // global array of available voices

window.speechSynthesis.onvoiceschanged = () => {
  
  // Initially set the First Voice in the Array.
  speech.voice = voices[0];

  // Set rate property of the SpeechSynthesisUtterance instance
  speech.rate = 1;

  // Set volume property of the SpeechSynthesisUtterance instance
  speech.volume = 1;

  // Set pitch property of the SpeechSynthesisUtterance instance
  speech.pitch = 1;

  // Set the Voice Select List. (Set the Index as the value, which we'll use later when the user updates the Voice using the Select Menu.)
  let voiceSelect = document.querySelector("#voices");
  voices.forEach(
    (voice, i) => (voiceSelect.options[i] = new Option(voice.name, i))
  );
};

document.querySelector("#voices").addEventListener("change", () => {
  // On Voice change, use the value of the select menu (which is the index of the voice in the global voice array)
  speech.voice = voices[document.querySelector("#voices").value];
});

document.querySelector("#start").addEventListener("click", () => {
  // Set the text property with the value of the textarea
  speech.text = document.querySelector("#post-toc").innerText;

  // Start Speaking
  window.speechSynthesis.speak(speech);
});

document.querySelector("#pause").addEventListener("click", () => {
  // Pause the speechSynthesis instance
  window.speechSynthesis.pause();
});

document.querySelector("#resume").addEventListener("click", () => {
  // Resume the paused speechSynthesis instance
  window.speechSynthesis.resume();
});

document.querySelector("#cancel").addEventListener("click", () => {
  // Cancel the speechSynthesis instance
  window.speechSynthesis.cancel();
});
