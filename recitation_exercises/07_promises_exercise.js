// run by opening 07_promises_exercise.html in the chrome browser
/*
The purpose of this exercise is to get you familiarized with promises.
*/


/*
1) 
Write a promise that resolves after waiting for 2 seconds
You can verify this by printing something to the console
after waiting for 2 seconds. Look into setTimeout function.
*/

// function resolveAfter2Seconds(x){
//     return new Promise( (resolve) => {
//         setTimeout( () => {
//             resolve(x)
//         }, 2000 )
//     });
// }

// async function f1(){
//     const x = await resolveAfter2Seconds(10);
//     console.log(x);
// }

// f1();

new Promise( (resolve) => { //resolve is a given by promise constructor and transitions to fulfilled state (the then state)

    setTimeout(resolve, 2000);

}
).then( () => {

    console.log("2 seconds later");

}
);

function resolveAfterMilliseconds(milliseconds) {
    return new Promise( (resolve) => setTimeout(resolve, milliseconds) );
}

/*
2) 
Imagine you're programming a two player game. For this
purpose we need to write a promise that resolves when
both the players join the game. Your task is to write
a promise that resolves when the number of players is 2
otherwise it rejects. For now, you can declare a variable
that holds the number of players. Again you can print
stuff to the console to verify your implementation works
*/
players = 2;

new Promise( (resolve, reject) => {

    players == 2 ? resolve("game ready 0") : reject("insufficient players 0");

}
).then( (text) => {
    console.log(text);
}
).catch( (text) => {
    console.log(text);
});

/*
3) 
Now we will try to chain promises together. Notice
that a promise when resolved can return a value or
another promise object. Imagine that you have to
fetch two files from the internet and then merge
the files together. Here we wont be doing any
fetching rather we'll try to emulate this by
setting timeouts. Assume it takes 3 seconds to
fetch the first file and 4 to fecth the second.
Again you can print stuff to the console to verify
your implementation works and use timeouts.
*/

// resolveAfterMilliseconds(3000).then(() => resolveAfterMilliseconds(4000)).then(() => console.log("two files snatched"));
resolveAfterMilliseconds(3000)
    .then((resolve) => {
        return new Promise( (resolve) => setTimeout(resolve, 4000))
    }).then(() => console.log("two files snatched")
);


/*
After implementing the above promises. Look at the console output see if it makes sense.
Some promises might have resolved before others even though they were declared afterwards.
*/


