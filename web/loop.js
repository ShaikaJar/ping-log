function Sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

async function waitForQuery(query) {

    while (true) {
        let button = document.querySelector(query)
        if (button != null)
            return button
        await Sleep(1000);
        
        window.dispatchEvent(new Event('mousemove',{offsetX:Math.random()-0.5, offsetY:Math.random()-0.5 }))
    }
}

async function waitForDisappearance(query){
    while (true) {
        let button = document.querySelector(query)
        if (button == null)
            return
        await Sleep(1000);
    }
}

let loopRunning = true;
async function voteLoop() {
    while (loopRunning) {
        let voteAgain = await waitForQuery('button#voteAgainButton:not(.disabled)');
        voteAgain.click();


        let captcha = await waitForQuery('button.frc-button');

        let contaienr = document.querySelectorAll('main>.l-container.l-container--content')[1]

        let deltaT = 1500
        let stepSize = 2

        for (let index = 0; index < deltaT/stepSize; index++) {
            await Sleep(stepSize);
            contaienr.dispatchEvent(new Event('mousemove',{offsetX:Math.random()-0.5, offsetY:Math.random()-0.5 }));
        }
 
        captcha.dispatchEvent(new Event('click',{offsetX:Math.random()-0.5, offsetY:Math.random()-0.5 }));

        while (document.querySelector('.frc-progress')!=null) {
            await Sleep(stepSize);
            contaienr.dispatchEvent(new Event('mousemove',{offsetX:Math.random()-0.5, offsetY:Math.random()-0.5 }));
        }
        console.log('Jiggle-Finish')
        //captcha.click();

        await Sleep(500);


        let vote = await waitForQuery('button#votingButton');
        vote.click();
    }
} 
