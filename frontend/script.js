/* =========================================================
   UPSC AI — INTERACTIONS
   ========================================================= */


/* =========================================================
   SCROLL REVEAL
   ========================================================= */

const revealElements =
    document.querySelectorAll(".reveal");


const revealObserver =
    new IntersectionObserver(

        (entries) => {

            entries.forEach(
                (entry) => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "visible"
                        );

                        revealObserver.unobserve(
                            entry.target
                        );

                    }

                }
            );

        },

        {
            threshold: 0.12
        }

    );


revealElements.forEach(
    (element) => {

        revealObserver.observe(element);

    }
);


/* =========================================================
   LAUNCH BUTTON
   ========================================================= */

const launchButton =
    document.getElementById(
        "launchButton"
    );


if (launchButton) {

    launchButton.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            /*
             * IMPORTANT:
             * Replace this URL later with your
             * deployed Streamlit application URL.
             */

            const streamlitURL =
                "https://YOUR-STREAMLIT-APP.streamlit.app";

            window.open(
                streamlitURL,
                "_blank"
            );

        }
    );

}


/* =========================================================
   EASTER EGG
   ========================================================= */

let keys = [];

const konamiCode = [

    "ArrowUp",
    "ArrowUp",

    "ArrowDown",
    "ArrowDown",

    "ArrowLeft",
    "ArrowRight",

    "ArrowLeft",
    "ArrowRight",

    "b",
    "a"

];


document.addEventListener(
    "keydown",
    function (event) {

        keys.push(event.key);

        keys =
            keys.slice(
                -konamiCode.length
            );


        if (
            keys.join(",") ===
            konamiCode.join(",")
        ) {

            document.body.style.transition =
                "transform 0.5s ease";

            document.body.style.transform =
                "rotate(1deg)";

            setTimeout(
                () => {

                    document.body.style.transform =
                        "rotate(0deg)";

                },
                500
            );

        }

    }
);