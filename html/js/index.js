async function handleSubmit(event) {
    event.preventDefault(); 
    const form = event.target;
    const formData = new FormData(form);

    const overlay = document.createElement('div');
    overlay.id = 'overlay';
    document.body.appendChild(overlay);

    const loader = document.createElement('div');
    loader.classList.add('loader');
    document.body.appendChild(loader);
    overlay.style.display = 'block';
    
    try{
        
        const response = await fetch('http://0.0.0.0:5566/api-async/submit-task/', {
            method: 'POST',
            headers: {'Accept': 'application/json'},
            body: formData
        });

        const { task_id } = await response.json();

        const socket = new WebSocket(`ws://0.0.0.0:5566/api-async/ws/${task_id}`);
        socket.onmessage = function(event) {
            console.log("job fin:", event.data); 
            showResult(event.data)
            socket.close();
            document.body.removeChild(loader);
            document.body.removeChild(overlay);
        };

    } catch (error) {
        showMessage(error, "error"); 
    } 

}


function showResult(data) {
    const messageDiv = document.getElementById('responseResult');
    messageDiv.innerHTML= data;
    messageDiv.style.display = 'flex';
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('responseMessage');
    messageDiv.innerHTML= message;
    messageDiv.className = 'response-message ' + type;
    messageDiv.style.display = 'flex';
    setTimeout(function() {
    		messageDiv.style.display = 'none';
	}, 5000);
}

function showCustomConfirm(message) {
    const modal = document.getElementById('custom-confirm');
    const confirmBtn = document.getElementById('confirm-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const messageElement = document.getElementById('custom-confirm-message');

    messageElement.innerHTML = message;

    modal.style.display = 'flex';

    return new Promise((resolve, reject) => {
        confirmBtn.onclick = function() {
            modal.style.display = 'none';
            resolve(true);
        };

        cancelBtn.onclick = function() {
            modal.style.display = 'none';
            resolve(false);
        };
    });
}

function showLoading() {
      document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
      document.getElementById('loading').style.display = 'none';
}
