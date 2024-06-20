document.addEventListener("DOMContentLoaded" , () => {
    const form = document.getElementById(".form-box.login")
    console.log("next")

    // form.addEventListener('click' , (event => {
    //         console.log("hello")
    //         event.preventDefault();
    //         console.log("after prevent")
    //         const email = document.getElementById("login_email").value;
    //         const password = document.getElementById("login_password").value;


    //         console.log(email)
    //         console.log(password)
        
    // }));
});

let data = {}
async function login(){
    const email = document.getElementById('login_email').value;
    const password = document.getElementById('login_password').value;
    console.log(`email: `,{email});
    console.log(`Password: `,{password});
    data = {email , password}
    console.log("before fetch in login")
    try{
        const response = await fetch("http://localhost:8000/login" , {
            method: "POST", 
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(data)
        })
        if(response.ok)
        {
            console.log("successfuly login")
            alert("already registered")
        }
        else{
            const check = await response.json();
            console.log(check)
            console.error("Error:" , check)
            
            // throw new Error(check.detail);

            
            alert("Account Not Found !!")
        }
    }   
    catch(error){
        console.error(error)
    }

}

async function register(){
    const username = document.getElementById('register_username').value;
    const email = document.getElementById('register_email').value;
    const password = document.getElementById('register_password').value;
    console.log(`Register-Data:`,{username , email , password});
    data = {username , email , password};
    console.log("before fetch")
    try{
        const response = await fetch("http://localhost:8000/register" , {
            method: "POST",
            headers:{"Content-Type":"application/json",
            // 'Access-Control-Allow-Origin' :'http://localhost:5500',
            },
            body: JSON.stringify(data),
        })
        if(response.ok){
            alert("Registered")
            console.log("Registerd Successfully")
        } 
        else{
            alert("errro", response.status)
            console.error("Error : ", response.status)
        }   
    }
    catch (error){
        console.error(error)
    }
}



// console.log(data)

function RegisterForm(){
    document.querySelector('#login_info').style.display = 'none';
    document.querySelector('#register').style.display = 'block';

}

function LoginForm(){
    document.querySelector('#login_info').style.display = 'block';
    document.querySelector('#register').style.display = 'none';
}

let login_button = document.querySelector('.submit')
login_button.onclick = login;

let reg_button = document.querySelector('.registration')
reg_button.onclick = register;


let reg_form = document.querySelector('#show_login_pg')
reg_form.onclick = LoginForm;


let login_form = document.querySelector('#show_register_pg')
login_form.onclick = RegisterForm;


// console.log(data)
async function register_data(){
    const response = await fetch("/register" , {
        method: "POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify(data),
    });
}












// document.querySelector('form').onsubmit = function(){
//     let email = document.querySelector('#email').value
//     let psw = document.querySelector('#psw').value
//     alert(`Hello... , ${emai} , ${psw}`)
//     console.log(email ,psw)

// }
       
       
    
       
       // const loginData = {
        //     email, 
        //     psw
        // };

        // let info = document.getElementById("submit_btn").innerText
        // console.log(info)

        // async function psw_data(){
        //     let psw = await fetch("/api/server/login",{method:"POST"})
        //     console.log("hello")
        //     console.log(psw)
        // }
        // async function login_data(){
        //     let response = await fetch("/api/server/login",{
        //         method: "POST"})
        //     console.log(response)
        
        // if (response != 200)
        // {
        //     alert("Something Went Wrong !!")
        //     return
        // }

        // let t = await response.json()
        // console.log(t)

    
        // }

        // fetch("/login", {
        // method: "POST", 
        // headers: { "Content-Type": "application/json" },
        // body: JSON.stringify(loginData)
        // })
        // .then(response => response.json())  
        // .then(data => {
        // console.log(data);
        // })
        // .catch(error => {

        // console.error(error);
        // });
