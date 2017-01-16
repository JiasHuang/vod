
function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "cmn-Hant-TW";
        recognition.start();

        recognition.onstart = function() {
            document.getElementById("ximage").src="listen.gif";
        };

        recognition.onend = function() {
            document.getElementById("ximage").src="mic.png";
        };

        recognition.onresult = function(event) {
            document.getElementById('xinput').value = event.results[0][0].transcript;
            recognition.stop();
            document.getElementById('xform').submit();
        };

        recognition.onerror = function(event) {
            console.log(event.error);
            recognition.stop();
        };

    }
}

