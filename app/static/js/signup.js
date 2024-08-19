// signup.js

document.addEventListener("DOMContentLoaded", init);

async function init() {
    // definition
    const board_P = document.getElementById("board-P");
    const board_0 = document.getElementById("board-0");
    const board_1 = document.getElementById("board-1");
    const board_2 = document.getElementById("board-2");
    const board_E = document.getElementById("board-E");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const reqData = {
        step_:null,
        email_:null,
        code_:null,
        password_:null
    }


    // event
    document.getElementById("btn-send").addEventListener("click",async()=>{
        console.log("email");
        let val = document.getElementById("input-email").value;
        if( !emailRegex.test(val) ){
            alert("wrong e-mail, dude"); 
            return
        }

        board_0.style.display = "none";
        board_P.style.display = "block";

        reqData.step_=0;
        reqData.email_=val;
        resp = await post_sign(reqData);
        if(resp.ok){
            board_P.style.display = "none";
            board_1.style.display = "block";
        }else{
            alert("email error");
            board_P.style.display = "none";
            board_0.style.display = "block";
        }


    });

    document.getElementById("btn-check").addEventListener("click",async()=>{
        console.log("code");
        board_1.style.display = "none";
        board_P.style.display = "block";

        let val = document.getElementById("input-code").value;
        reqData.step_=1;
        reqData.code_=val;
        resp = await post_sign(reqData);
        if(resp.ok){
            board_P.style.display = "none";
            board_2.style.display = "block";
        }else{
            board_P.style.display = "none";
            board_1.style.display = "block";
        }

    });

    document.getElementById("btn-password").addEventListener("click",async()=>{
        console.log("password");
        board_2.style.display = "none";
        board_P.style.display = "block";

        let val = document.getElementById("input-password").value;
        reqData.step_=2;
        reqData.password_=val;
        resp = await post_sign(reqData);
        if(resp.ok){
            board_P.style.display = "none";
            board_E.style.display = "block";
            setTimeout( ()=>{window.location.href="/"}, 2000 );
        }else{
            board_P.style.display = "none";
            board_2.style.display = "block";
        }


    });


    // setup
    document.getElementById("board-0").style.display = "block";

    console.log("load complete");
}


// function
async function post_sign(reqData) {
    try{
        return await fetch("/guest/sign",{
            method:"POST",
            headers:{"Content-Type": "application/json"},
            body:JSON.stringify(reqData)
        });
    }catch(e){
        console.log("ERROR from post_sign : ", e);
        return new Response(null, { status: 500, statusText: "Fetch Error" });
    }
}