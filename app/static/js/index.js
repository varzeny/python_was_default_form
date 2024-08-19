// index.js

document.addEventListener("DOMContentLoaded", init);

async function init() {

    // definition
    const inputEmail = document.getElementById("input-email");
    const inputPassword = document.getElementById("input-password");

    // event
    document.getElementById("btn-login").addEventListener("click", async()=>{
        console.log("login 버튼 눌림");
        const reqData = {
            email_:inputEmail.value,
            password_:inputPassword.value
        }
        const resp = await fetch("/guest/login",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify( reqData )
        }); 
        if(resp.ok){
            const respData = await resp.json();
            if(respData.role_=="user"){ window.location.href = "/user/" }
            else if(respData.role_=="admin"){ window.location.href = "/admin/" }
            else { alert("error"); return }
        }else{
            alert("login fail")
        }
    });

    document.getElementById("btn-signup").addEventListener("click", async()=>{
        console.log("signup 버튼 눌림");
        window.location.href="/guest/signup";

    });



    console.log("load complete !");
}