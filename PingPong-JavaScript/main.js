const PADDLE_HEIGHT = 120;
const PADDLE_WIDTH = 10;
const PADDLE_DISTANCE = 5;
const BALL_RADIUS = 10;

const INITIAL_BALL_VEL_X = 6;
const INITIAL_BALL_VEL_Y = 3;

var canvas;
var canvasContext;
var fps = 60;

var ballX;
var ballY;
var velBallX = INITIAL_BALL_VEL_X;
var velBallY = INITIAL_BALL_VEL_Y;
var paddleLeftY;
var paddleRightY;

var frameCounter = 0;
var frameThreshold = 90;
var leftWins = 0;
var rightWins = 0;


window.onload = function() {
    canvas = document.getElementById("canv");
    canvasContext = canvas.getContext("2d");

    // fill the first variables with content
    ballX = canvas.width / 2;
    ballY = canvas.height / 2;
    paddleLeftY = canvas.height / 2 - PADDLE_HEIGHT / 2;
    paddleRightY = paddleLeftY;

    // set the game loop
    setInterval(function () {
        update();
        draw();
    }, 1000 / fps);

    // set the left paddle to the mouse position
    canvas.addEventListener("mousemove", function(evnt) {
        var mousePos = getMousePos(evnt);
        paddleLeftY = mousePos.y - PADDLE_HEIGHT / 2;
    });
}


function getMousePos(evt) {
    // this function returns the mouse position inside the canvas
    var rect = canvas.getBoundingClientRect();
    var mouseX = evt.clientX - rect.left;
    var mouseY = evt.clientY - rect.top;

    return {
        x: mouseX,
        y: mouseY
    };
}


function draw() {
    // draw the black baground recktangle
    canvasContext.fillStyle = "black";
    canvasContext.fillRect(0, 0, canvas.width, canvas.height);

    // draw the red ball
    canvasContext.fillStyle = "red";
    canvasContext.beginPath();
    canvasContext.arc(ballX, ballY, BALL_RADIUS, 0, Math.PI * 2, true);
    canvasContext.fill();

    // draw the left player (paddle)
    canvasContext.fillStyle = "white";
    canvasContext.fillRect(PADDLE_DISTANCE, paddleLeftY, PADDLE_WIDTH, PADDLE_HEIGHT);

    // draw the right player (paddle)
    canvasContext.fillStyle = "white";
    canvasContext.fillRect(canvas.width - PADDLE_DISTANCE - PADDLE_WIDTH, paddleRightY, PADDLE_WIDTH, PADDLE_HEIGHT);

    // draw the scores
    canvasContext.font = "24px Arial";
    canvasContext.fillText(leftWins, canvas.width / 4, canvas.height / 4);
    canvasContext.fillText(rightWins, canvas.width - (canvas.width / 4), canvas.height / 4);
}


function update() {
    // increase the frame counter as well as the speed of the ball
    frameCounter++;
    increaseBallSpeed();
    moveRightPaddle();

    // check if any player gets a point and rebounce the ball if the user blocks them
    if (ballX <= PADDLE_DISTANCE + PADDLE_WIDTH && velBallX < 0) {
        if (ballY > paddleLeftY - BALL_RADIUS && ballY < paddleLeftY + PADDLE_HEIGHT + BALL_RADIUS) {
            // the user has blocked the ball
            rebounceBall(paddleLeftY);
        } else {
            // the ball is behind the left paddle, and the user has not blocked it, so the right player gets a point
            rightWins++;
            resetBallPosition();
        }
    } else if (ballX >= canvas.width - PADDLE_DISTANCE - PADDLE_WIDTH && velBallX > 0) {
        if (ballY > paddleRightY - BALL_RADIUS && ballY < paddleRightY + PADDLE_HEIGHT + BALL_RADIUS) {
            // the user has blocked the ball
            // invert the direction of the ball and influence the y direction from where the ball hits the paddle
            rebounceBall(paddleRightY);
        } else {
            // the ball is behind the left paddle, and the user has not blocked it, so the right player gets a point
            leftWins++;
            resetBallPosition();
        }
    }

    // check if somebody has 5 points
    checkWinner();

    // bounce the ball of the bottom and of the top
    if (ballY <= BALL_RADIUS || ballY >= canvas.height - BALL_RADIUS) {
        velBallY = -velBallY;
    }

    // move the ball
    ballX += velBallX;
    ballY += velBallY;
}


function checkWinner() {
    if (leftWins >= 5) {
        alert("Du hast gewonnen!\nHerzlichen Glückwunsch!");
        leftWins = 0;
        rightWins = 0;
    } else if (rightWins >= 5) {
        alert("Du hast leider verloren!\nDer Computer hat gerade seinen fünften Punkt gemacht!");
        leftWins = 0;
        rightWins = 0;
    }
}


function rebounceBall(paddleY) {
    // invert the direction of the ball and influence the y direction from where the ball hits the paddle
    // calculate the old velocity
    var old_vel = Math.sqrt(velBallX * velBallX + velBallY * velBallY);
    var distanceFromMiddle = ballY - (paddleY + PADDLE_HEIGHT / 2);
    // map the value to a rage between -6 and 6
    distanceFromMiddle = mapValue(distanceFromMiddle, -PADDLE_HEIGHT / 2, PADDLE_HEIGHT / 2, -6, 6);

    velBallY = distanceFromMiddle;
    var velBallXPos = Math.sqrt(old_vel * old_vel - velBallY * velBallY);

    // change the direction
    if (velBallX < 0) {
        velBallX = velBallXPos;
    } else {
        velBallX = -velBallXPos;
    }
}


function mapValue(value, min_old, max_old, min_new, max_new) {
    // standard algorithm (mapping a value into another range)
    return (value - min_old) * (max_new - min_new) / (max_old - min_old) + min_new;
}


function moveRightPaddle() {
    // if the ball is moving to the right and is in the right half of the gamefield move the paddle
    if (velBallX > 0 && ballX > 2 * canvas.width / 5) {
        // the following line would be a perfect player
        //paddleRightY = ballY - PADDLE_HEIGHT / 2;

        // the ball should be within the middle-third of the paddle
        if (ballY < paddleRightY + PADDLE_HEIGHT / 3) {
            paddleRightY -= 8;
        } else if (ballY > paddleRightY + PADDLE_HEIGHT - PADDLE_HEIGHT / 3) {
            paddleRightY += 8;
        }
    }
}


function increaseBallSpeed() {
    // every time a defined amount of frames where rendered, increase the speed of the ball
    if (frameCounter >= frameThreshold) {
        var inc = 0.3

        if (velBallX < 0) {
            velBallX -= inc;
        } else {
            velBallX += inc;
        }
        if (velBallY < 0) {
            velBallY -= inc;
        } else if (velBallY > 0) {
            velBallY += inc;
        }

        frameCounter = 0;
    }
}


function resetBallPosition() {
    // flip the direction every score
    if (velBallX < 0) {
        velBallX = INITIAL_BALL_VEL_X;
    } else {
        velBallX = -INITIAL_BALL_VEL_X;
    }
    if (velBallY < 0) {
        velBallY = INITIAL_BALL_VEL_Y;
    } else {
        velBallY = -INITIAL_BALL_VEL_Y;
    }
    ballX = canvas.width / 2 - BALL_RADIUS;
    ballY = canvas.height / 2 - BALL_RADIUS;
}